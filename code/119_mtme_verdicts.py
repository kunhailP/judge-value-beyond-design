#!/usr/bin/env python3
"""Lock v1.1 verdicts (H8–H11) and the per-metric table: all 31 WMT22 metrics as judges, MT top-4 menus, pilot 50.

Per metric and language pair: system-level Pearson with MQM (11 WMT submissions), top-4 Kendall, rho_bar (mean over the
menu's 6 pairs of the correlation of paired differences; rho_bar^2 = asymptotic PPSR-style saving), and per epsilon the
realised HES over uniform sampling (uniform_cvl vs uniform), over the best human design, and on the weighted design with
pilot and oracle lambda. Writes results/MTME_TABLE.csv and results/MTME_VERDICTS.md.
"""
import itertools, os, sys
import numpy as np, pandas as pd
from scipy.stats import kendalltau, pearsonr, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from paths import DATA
from mt_common import load_pool
R = os.path.join(HERE, "..", "results")
MBR = ("bleu_bestmbr", "bleurt_bestmbr", "comet_bestmbr", "chrf_bestmbr")
rng = np.random.default_rng(0)
rows, md = [], ["# Lock v1.1 verdicts (all WMT22 metrics as judges)", ""]
for lp in ("ende", "zhen"):
    metrics = open(f"{DATA}/mt/MTME_METRICS.txt").read().split("\n")
    metrics = [l.split("\t")[1].split() for l in metrics if l.startswith(lp)][0]
    d = load_pool(lp); d = d[~d.system.isin(MBR)].copy(); d["u"] = d.groupby(["seg_id", "hyp"]).u.transform("mean")
    sysu = d.groupby("system").u.mean(); menu = sysu.sort_values(ascending=False).index[:4].tolist()
    U = d.pivot(index="seg_id", columns="system", values="u")
    S = pd.read_csv(f"{R}/mt/mt_{lp}_m4_p50_mtme_summary.csv")
    for f in metrics:
        j = pd.read_parquet(f"{DATA}/mt/{lp}/judge_{f}.parquet"); j = j[~j.system.isin(MBR)]
        sysj = j.groupby("system").score.mean().loc[sysu.index]
        Jm = j.pivot(index="seg_id", columns="system", values="score").loc[U.index]
        rhos = [np.corrcoef(U[a] - U[b], Jm[a] - Jm[b])[0, 1] for a, b in itertools.combinations(menu, 2)]
        r = dict(lp=lp, metric=f[5:], sys_pearson=pearsonr(sysj, sysu)[0], top4_kendall=kendalltau(sysj[menu], sysu[menu])[0],
                 rho_bar=float(np.mean(rhos)), mean_rho2=float(np.mean(np.square(rhos))))   # (mean rho)^2 as locked; mean rho^2 = PPSR-style
        for eps in (0.01, 0.02):
            J = S[(S.metric == "J50") & (S.eps == eps)].set_index("design").value
            bh = S[(S.metric == "best_human") & (S.eps == eps)].design.iloc[0]
            r[f"hes_uniform_{eps}"] = 1 - J[f"uniform_cvl:{f}"] / J["uniform"]
            r[f"hes_best_{eps}"] = 1 - J[f"weighted_cvl:{f}"] / J[bh] if bh != "uniform" else r[f"hes_uniform_{eps}"]
            r[f"hes_w_pilot_{eps}"] = 1 - J[f"weighted_cvl:{f}"] / J["weighted"]
            r[f"hes_w_oracle_{eps}"] = 1 - J[f"weighted_cvo:{f}"] / J["weighted"]
            r[f"design_save_{eps}"] = 1 - J[bh] / J["uniform"]
        rows.append(r)
T = pd.DataFrame(rows); T.to_csv(f"{R}/MTME_TABLE.csv", index=False)

# H8
h8 = []
for lp in ("ende", "zhen"):
    g = T[T.lp == lp]
    for eps in (0.01, 0.02):
        best = g.loc[g[f"hes_best_{eps}"].idxmax()]
        h8.append(best[f"design_save_{eps}"] >= best[f"hes_best_{eps}"])
        md.append(f"- {lp} ε={eps}: best fixed judge-free baseline saves {best[f'design_save_{eps}']:+.3f} vs uniform; best metric {best.metric} HES over it {best[f'hes_best_{eps}']:+.3f}")
md += ["", f"**H8**: {sum(h8)}/4 cells → {'SUPPORTED' if sum(h8) >= 3 else 'NOT SUPPORTED'}", ""]
# H9 — bootstrap unit = metric (the two epsilon values of a metric are averaged first; they are not independent)
for lp in ("ende", "zhen"):
    g = T[T.lp == lp]
    tax = ((g["hes_w_oracle_0.01"] - g["hes_w_pilot_0.01"]) + (g["hes_w_oracle_0.02"] - g["hes_w_pilot_0.02"])).values / 2
    bs = [rng.choice(tax, len(tax)).mean() for _ in range(5000)]; lo, hi = np.percentile(bs, [2.5, 97.5])
    md.append(f"**H9 {lp}**: mean tax {tax.mean():+.3f} [{lo:+.3f}, {hi:+.3f}] (metric-level bootstrap, {len(tax)} metrics) → {'SUPPORTED' if lo > 0 else 'NOT SUPPORTED'}")
md.append("")
# H10 — as locked: (mean rho)^2. Post-lock robustness: mean of squared per-pair correlations (the PPSR definition).
for label, col in (("as locked, (mean ρ)²", "r2_locked"), ("post-lock robustness, mean ρ² (PPSR definition)", "mean_rho2")):
    ok_all = True
    for lp in ("ende", "zhen"):
        g = T[T.lp == lp].assign(r2_locked=lambda x: x.rho_bar ** 2).nlargest(5, col)
        for eps in (0.01, 0.02):
            ok = (g[f"hes_uniform_{eps}"] < g[col]).all(); ok_all &= ok
            md.append(f"- [{label}] {lp} ε={eps}: " + ", ".join(f"{m} {a:.3f}→{b:+.3f}" for m, a, b in zip(g.metric, g[col], g[f'hes_uniform_{eps}'])))
    md += ["", f"**H10 [{label}]** (realised HES over uniform < the correlation-based saving for all top-5 metrics in every cell) → {'SUPPORTED' if ok_all else 'NOT SUPPORTED'}", ""]
# H11 (as locked) + descriptive: local top-4 Kendall
for lp in ("ende", "zhen"):
    g = T[T.lp == lp]; y = np.concatenate([g[f"hes_best_{e}"] for e in (0.01, 0.02)])
    a = spearmanr(y, np.tile(g.rho_bar, 2))[0]; b = spearmanr(y, np.tile(g.sys_pearson, 2))[0]; c = spearmanr(y, np.tile(g.top4_kendall, 2))[0]
    md.append(f"**H11 {lp}**: Spearman(HES over best fixed judge-free baseline, ρ̄) = {a:.3f} vs system Pearson = {b:.3f} "
              f"(descriptive: top-4 Kendall = {c:.3f}) → {'SUPPORTED' if a > b else 'NOT SUPPORTED'}; neither predicts HES well among real metrics")
md += ["", "## Per-metric table (sorted by ρ̄)", "", T.sort_values(["lp", "rho_bar"], ascending=[True, False]).round(3).to_markdown(index=False)]
open(f"{R}/MTME_VERDICTS.md", "w").write("\n".join(md)); print("\n".join(md[:40]))
