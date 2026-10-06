#!/usr/bin/env python3
"""Exploratory: semi-synthetic judges with a set decision-level rho (syn0.1..syn0.9, see 110_unit_audit._synthetic) against
the cost law with an estimation tax, HES_pred = [rho^2 - (1-rho^2)/P_eff](1 - P/J) and its ceiling rho^2(1 - P/J).
Reads results/{mt,arena}/*_syn_summary.csv; writes results/RHO_DIAL.csv."""
import glob, json, os
import numpy as np, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = []
for f in sorted(glob.glob(f"{R}/mt/*_syn_summary.csv")) + sorted(glob.glob(f"{R}/arena/*_syn_summary.csv")):
    s = pd.read_csv(f); info = json.load(open(f.replace("_summary.csv", "_info.json"))); pred = pd.read_parquet(f.replace("_summary.csv", "_pred.parquet"))
    mt = "/mt/" in f; base, arm = ("weighted", "weighted_cvl") if mt else ("uniform", "uniform_cvl")
    for eps, g in s.groupby("eps"):
        J = g[g.metric == "J50"].set_index("design").value; P = pred[pred.eps == eps].pilot_cost.median()
        share = 1 - P / J[base]; Peff = info["cfg"]["pilot"] * (0.5 if mt else 0.75)   # share of non-zero paired differences
        for r in np.round(np.arange(.1, 1, .1), 1):
            k = f"{arm}:syn{r}"
            if k in J:
                rows.append(dict(run=os.path.basename(f)[:-12], eps=eps, rho=r, real=1 - J[k] / J[base], ceil=r * r * share,
                                 pred=(r * r - (1 - r * r) / Peff) * share, share=share))
T = pd.DataFrame(rows); T.to_csv(f"{R}/RHO_DIAL.csv", index=False)
print("corr(pred,real)=%.3f MAE=%.3f corr(ceil,real)=%.3f n=%d" % (np.corrcoef(T.pred, T.real)[0, 1], (T.pred - T.real).abs().mean(),
      np.corrcoef(T.ceil, T.real)[0, 1], len(T)))
print(T.groupby("rho")[["pred", "ceil", "real"]].mean().round(3).T.to_string())
