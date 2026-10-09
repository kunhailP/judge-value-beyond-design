#!/usr/bin/env python3
"""Exploratory (pre-submission): the 30-decision summary under variations of the audit's fixed parameters, from the
per-cell outputs of 125_exclusion.py (results/EXCLUSION_cells<_tag>.csv, results/EXCLUSION<_tag>.csv):
  paper   pilot 50, 300 draws, 3 dissimilarity bins, 34 evaluators (31 metric variants + COMET-22 + 2 GEMBA judges)
  p25/p10 pilot 25 / 10 segments            (same decisions, eps, rules; evaluators = those available on the machine)
  b4      four quartile bins in the weighted design
  n2000   2,000 simulated audits per cell (Monte-Carlo precision)
Per variant: informative cells, design saving (median), mean evaluator HES (median over cells; all / top-10 by system-level
Pearson), share of cells where the design saves more, share of (cell, evaluator) pairs whose one-sided 95% upper bound
rules out a 5% / 10% saving, pilot share of the cost. Writes results/VARIANTS.md.
usage: 126_variants.py [tags...]   (default: '' p25 p10 b4 n2000; missing files are skipped)
"""
import os, sys
import numpy as np, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
LAB = {"": "paper (P=50, 300 draws, 3 bins)", "p25": "pilot 25", "p10": "pilot 10", "b4": "four bins", "n2000": "2,000 draws"}


def row(tag):
    sfx = f"_{tag}" if tag else ""
    fc, fe = f"{R}/EXCLUSION_cells{sfx}.csv", f"{R}/EXCLUSION{sfx}.csv"
    if not (os.path.exists(fc) and os.path.exists(fe)):
        return None
    C = pd.read_csv(fc); E = pd.read_csv(fe)
    Ci = C[C.informative]; Ei = E[E.informative]
    n_ev = Ei.groupby(["lp", "pair", "eps", "mode"]).judge.nunique().median()
    r = dict(variant=LAB.get(tag, tag), cells=len(Ci), en_de=int((Ci.lp == "ende").sum()), zh_en=int((Ci.lp == "zhen").sum()),
             evaluators=int(n_ev), pilot_share_median=float((1 - Ci.post_share).median()), design_median=Ci.save.median(), design_lo_gt0=(Ci.save_lo > 0).mean())
    for m in ("pilot", "refit", "xfit"):
        r[f"mean_eval_{m}"] = Ci[f"mean_{m}_all"].median(); r[f"design_wins_{m}"] = (Ci.save > Ci[f"mean_{m}_all"]).mean()
        r[f"mean_eval_{m}_top10"] = Ci[f"mean_{m}_top10"].median(); r[f"design_wins_{m}_top10"] = (Ci.save > Ci[f"mean_{m}_top10"]).mean()
        r[f"best_{m}"] = Ci[f"best_{m}_all"].median()
        s = Ei[Ei["mode"] == m]; t = s[s.top10]
        r[f"excl5_{m}"] = s["excl_0.05"].mean(); r[f"excl10_{m}"] = s["excl_0.1"].mean()
        r[f"excl5_{m}_top10"] = t["excl_0.05"].mean(); r[f"excl10_{m}_top10"] = t["excl_0.1"].mean()
        r[f"halfwidth_{m}"] = ((s.hes_hi - s.hes_lo) / 2).median()
        r[f"cell_ub_lt5_{m}"] = (Ci[f"mean_{m}_all_ub95"] < 0.05).mean(); r[f"cell_ub_lt10_{m}"] = (Ci[f"mean_{m}_all_ub95"] < 0.10).mean()
    return r


def main():
    tags = sys.argv[1:] or ["", "p25", "p10", "b4", "n2000"]
    T = pd.DataFrame([r for r in map(row, tags) if r])
    pct = [c for c in T if c not in ("variant", "cells", "en_de", "zh_en", "evaluators")]
    T[pct] = (100 * T[pct]).round(1)
    md = ["# The 30-decision summary under variations of the audit (exploratory, pre-submission)", "",
          "Percent. Informative cells: post-pilot share of uniform-sampling cost >= 0.3. mean_eval: median over cells of the mean evaluator HES over the matched best fixed judge-free base; "
          "design_wins: share of cells where the design's saving over uniform exceeds that mean; excl5/excl10: share of (cell, evaluator) pairs whose one-sided 95% bootstrap upper bound of HES "
          "is below 5% / 10%; cell_ub_lt5: share of cells where the upper bound of the MEAN evaluator is below 5%; halfwidth: median half-width of the 95% interval of a single evaluator's HES.", ""]
    md += ["## Headline", "", T[["variant", "cells", "en_de", "zh_en", "evaluators", "pilot_share_median", "design_median", "mean_eval_pilot", "mean_eval_refit", "mean_eval_xfit",
                                 "design_wins_pilot", "design_wins_refit", "design_wins_xfit", "best_refit"]].to_markdown(index=False), ""]
    md += ["## Ten evaluators with the highest system-level Pearson", "", T[["variant", "mean_eval_pilot_top10", "mean_eval_refit_top10", "mean_eval_xfit_top10", "design_wins_pilot_top10", "design_wins_refit_top10", "design_wins_xfit_top10"]].to_markdown(index=False), ""]
    md += ["## What the intervals rule out", "", T[["variant", "halfwidth_refit", "excl5_pilot", "excl10_pilot", "excl5_refit", "excl10_refit", "excl5_xfit", "excl10_xfit",
                                                   "excl5_refit_top10", "excl10_refit_top10", "cell_ub_lt5_refit", "cell_ub_lt10_refit"]].to_markdown(index=False), ""]
    open(f"{R}/VARIANTS.md", "w").write("\n".join(md)); print("\n".join(md))


if __name__ == "__main__":
    main()
