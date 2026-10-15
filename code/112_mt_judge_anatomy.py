#!/usr/bin/env python3
"""Exploratory (post-lock) anatomy of the MT judges: three ways of scoring the same judge.

  system level   : Kendall tau / Pearson between judge mean score and human mean utility over the WMT submissions
                   (what WMT metrics tasks and JuStRank-style studies report);
  segment level  : pairwise accuracy of the judge on (segment, system pair) items with different human scores, and the
                   Pearson correlation of judge score with utility over all rated outputs;
  decision level : rho of the paired difference D_j = u_j - u_c over segments, for every pair among the top-6 systems
                   (what controls the variance reduction of the control variate), plus rho restricted to segments whose
                   outputs differ (identical outputs contribute D = Dhat = 0).
Output: results/mt/ANATOMY_<lp>.csv and a printed table.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
import os, sys, itertools
import numpy as np, pandas as pd
from scipy.stats import kendalltau, pearsonr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from mt_common import load_pool
MBR = ("bleu_bestmbr", "bleurt_bestmbr", "comet_bestmbr", "chrf_bestmbr")
JUDGES = ["comet22", "qwen3_8b", "mistral_7b", "chrf"]
OUT = os.path.join(HERE, "..", "results", "mt")

rows = []
for lp in ("ende", "zhen"):
    d = load_pool(lp); d = d[~d.system.isin(MBR)].copy()
    d["u"] = d.groupby(["seg_id", "hyp"]).u.transform("mean")
    for f in JUDGES:
        if f != "chrf":
            j = pd.read_parquet(f"{DATA}/mt/{lp}/judge_{f}.parquet").rename(columns={"score": f})
            d = d.merge(j, on=["seg_id", "system"], how="left")
    sysmean = d.groupby("system")[["u"] + JUDGES].mean()
    top6 = sysmean.u.sort_values(ascending=False).index[:6].tolist()
    U = d.pivot(index="seg_id", columns="system", values="u")
    H = d.pivot(index="seg_id", columns="system", values="hyp")
    for f in JUDGES:
        S = d.pivot(index="seg_id", columns="system", values=f)
        r = dict(lp=lp, judge=f,
                 sys_kendall=kendalltau(sysmean[f], sysmean.u)[0], sys_pearson=pearsonr(sysmean[f], sysmean.u)[0],
                 sys_kendall_top6=kendalltau(sysmean.loc[top6, f], sysmean.loc[top6, "u"])[0],
                 seg_pearson=pearsonr(d[f], d.u)[0])
        agree, tot, rhos, rhos_nz = 0, 0, [], []
        for a, b in itertools.combinations(top6, 2):
            Dh = U[a] - U[b]; Dj = S[a] - S[b]; nz = H[a] != H[b]
            m = Dh != 0
            agree += (np.sign(Dh[m]) == np.sign(Dj[m])).sum(); tot += m.sum()
            rhos.append(np.corrcoef(Dh, Dj)[0, 1]); rhos_nz.append(np.corrcoef(Dh[nz], Dj[nz])[0, 1])
        r.update(pair_acc_top6=agree / tot, rho_pair_median=np.median(rhos), rho_pair_min=np.min(rhos), rho_pair_max=np.max(rhos),
                 rho_pair_nz_median=np.median(rhos_nz), frac_D_zero=float(np.mean([(U[a] - U[b] == 0).mean() for a, b in itertools.combinations(top6, 2)])))
        rows.append(r)
out = pd.DataFrame(rows)
for lp, g in out.groupby("lp"):
    g.to_csv(os.path.join(OUT, f"ANATOMY_{lp}.csv"), index=False)
pd.set_option("display.width", 250); print(out.round(3).to_string(index=False))
