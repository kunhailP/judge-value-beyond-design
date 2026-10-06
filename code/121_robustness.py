#!/usr/bin/env python3
"""Exploratory (post-lock) robustness of the estimation-tax and design-credit results.

For each evaluator, language pair and epsilon (MT, pilot 50; 8 strongest WMT22 metric variants by rho_bar + COMET-22,
Qwen3-8B, Mistral-7B) and for each Arena v0.9 pair, HES of the evaluator over its own judge-free base design under four
ways of setting the control-variate coefficient:
  pilot  (*_cvl)  fitted on the pilot and frozen (the paper's estimator)
  refit  (*_cvq)  refitted by unweighted least squares on the pilot plus every post-pilot label (same labels used for
                  estimation and inference, as in standard PPI++ / PPSR; its variance estimate ignores the coefficient's error)
  xfit   (*_cvu)  cross-fitted, unweighted: each unit's residual uses the coefficient fitted on the pilot and the other fold
  refit_ht, xfit_ht (*_cvr, *_cvx)  the same with 1/pi-weighted (design-consistent) least squares
  oracle (*_cvo)  population-optimal coefficient (not available to an auditor)
and the matched-base HES on dedup (the zh->en best fixed judge-free design). Also the J80 version. Writes
results/ROBUSTNESS.csv and results/ROBUSTNESS.md.
"""
import glob, os
import numpy as np, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = []
for f in sorted(glob.glob(f"{R}/mt/mt_*_m4_p50_robust2_summary.csv")) + sorted(glob.glob(f"{R}/arena/arena_1[0-5]_m2_p50_robust_summary.csv")):
    s = pd.read_csv(f); dom = "mt" if "/mt/" in f else "arena"; cell = os.path.basename(f).split("_m")[0]
    judges = sorted({d.split(":")[1] for d in s.design if ":" in d and not d.startswith("sel")})
    bases = ["weighted", "dedup"] if dom == "mt" else ["uniform"]
    for (eps, t), g in s[s.metric.isin(["J50", "J80"])].groupby(["eps", "metric"]):
        J = g.drop_duplicates("design").set_index("design").value
        bh = s[(s.metric == "best_human") & (s.eps == eps)].design.iloc[0]
        for j in judges:
            for b in bases:
                r = dict(domain=dom, cell=cell, eps=eps, level=t, judge=j, base=b, best_fixed=bh)
                for mode, suf in (("pilot", "cvl"), ("refit", "cvq"), ("xfit", "cvu"), ("refit_ht", "cvr"), ("xfit_ht", "cvx"), ("oracle", "cvo")):
                    k = f"{b}_{suf}:{j}"
                    r[mode] = 1 - J[k] / J[b] if k in J and b in J and np.isfinite(J[k]) and np.isfinite(J[b]) else np.nan
                rows.append(r)
T = pd.DataFrame(rows); T.to_csv(f"{R}/ROBUSTNESS.csv", index=False)
md = ["# Robustness of the estimation tax (exploratory, post-lock)", "",
      "HES of each evaluator over its own judge-free base design, by how the coefficient is set (mean over evaluators;",
      "MT: 8 strongest metric variants + COMET-22, Qwen3-8B, Mistral-7B; Arena: Qwen3-8B, Mistral-7B, longer).", ""]
for lev in ("J50", "J80"):
    sub = T[T.level == lev]
    tab = sub.groupby(["domain", "cell", "base"])[["pilot", "refit", "xfit", "refit_ht", "xfit_ht", "oracle"]].mean().round(3)
    md += [f"## {lev}", "", tab.to_markdown(), ""]
    # tax decomposition: oracle - pilot (total), oracle - xfit (remaining with valid cross-fitting), oracle - refit
    agg = sub.assign(tax_pilot=sub.oracle - sub.pilot, tax_xfit=sub.oracle - sub.xfit, tax_refit=sub.oracle - sub.refit)
    md += [agg.groupby(["domain", "cell"])[["tax_pilot", "tax_xfit", "tax_refit"]].mean().round(3).to_markdown(), ""]
# best evaluator on the matched best fixed base (J50)
mb = T[(T.level == "J50") & (T.base == T.best_fixed)]
md += ["## Best evaluator on the best fixed judge-free base (matched base, J50, pilot / xfit coefficient)", "",
       mb.groupby(["cell", "eps"]).agg(best_pilot=("pilot", "max"), best_refit=("refit", "max"), mean_refit=("refit", "mean"), best_xfit=("xfit", "max"), mean_xfit=("xfit", "mean")).round(3).to_markdown()]
open(f"{R}/ROBUSTNESS.md", "w").write("\n".join(md)); print("\n".join(md))
