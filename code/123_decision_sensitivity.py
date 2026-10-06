#!/usr/bin/env python3
"""Exploratory (post-lock) sensitivity of the 30-decision summary (results/DECISIONS*.csv, code/122_decisions.py):
  * the informativeness threshold t on the post-pilot share 1 - P/J50(uniform) (paper: t = 0.3), t in {0, 0.2, ..., 0.6}; MT post-pilot shares have no value in (0.21, 0.47), so any t there selects the same 33 cells;
  * the evaluator set: all 34, or the ten with the highest system-level Pearson per language pair (chosen without
    looking at any decision), for which the mean HES is compared with the judge-free design;
  * the identical-string label (DECISIONS_pick.csv, if present: one random rating shared instead of the mean).
MT cells only. Writes results/DECISIONS_SENSITIVITY.md.
"""
import os
import numpy as np, pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
MODES = ["pilot", "refit", "xfit"]


def summarise(T, t, top10):
    c = T[(T.lp != "chat") & (T.post_share >= t)]
    if top10:
        c = c[c.top10]
    g = c.groupby(["lp", "pair", "eps"])
    cell = g.agg(save=("save", "first"), **{m: (m, "mean") for m in MODES}).reset_index()
    out = dict(cells=len(cell), en_de=int((cell.lp == "ende").sum()), zh_en=int((cell.lp == "zhen").sum()),
               design_median=cell.save.median())
    for m in MODES:
        out[f"mean_eval_{m}"] = cell[m].median()
        out[f"design_wins_{m}"] = (cell.save > cell[m]).mean()
    return out


def table(T, label):
    sysr_rank = T.drop_duplicates(["lp", "judge"]).copy()
    sysr_rank["top10"] = sysr_rank.groupby("lp").sys_r.rank(ascending=False, method="first") <= 10
    T = T.merge(sysr_rank[["lp", "judge", "top10"]], on=["lp", "judge"])
    rows = []
    for top10 in (False, True):
        for t in (0.0, 0.2, 0.3, 0.4, 0.5, 0.6):
            rows.append(dict(evaluators="top-10 by system r" if top10 else "all 34", t=t, **summarise(T, t, top10)))
    D = pd.DataFrame(rows)
    pct = [c for c in D if c.startswith(("design_median", "mean_eval"))]
    D[pct] = (100 * D[pct]).round(1)
    D[[c for c in D if c.startswith("design_wins")]] = (100 * D[[c for c in D if c.startswith("design_wins")]]).round(0)
    return [f"## {label}", "", "Percent; per cell the mean evaluator HES is the mean over the evaluator set, then the median over cells; "
            "design_wins = share of cells where the design's saving exceeds that mean.", "", D.to_markdown(index=False), ""]


def main():
    md = ["# Sensitivity of the 30-decision summary (exploratory)", ""]
    md += table(pd.read_csv(f"{R}/DECISIONS.csv"), "Identical strings share the mean of their ratings (paper)")
    if os.path.exists(f"{R}/DECISIONS_pick.csv"):
        md += table(pd.read_csv(f"{R}/DECISIONS_pick.csv"), "Identical strings share one random rating (IDENT=pick)")
    md += locked_cells()
    open(f"{R}/DECISIONS_SENSITIVITY.md", "w").write("\n".join(md)); print("\n".join(md))



def locked_cells():
    """Design savings over uniform in the four locked MT cells (menu top-4, pilot 50) with identical strings sharing
    their mean rating (the locked runs) and one random rating (tags _pick0.._pick2, 110_unit_audit.py --ident pick)."""
    import glob

    def j50(stem):
        D = pd.read_parquet(stem + "_draws.parquet")
        D = D[D.design.isin(["uniform", "dedup", "weighted"])]
        out = {}
        for (e, des), g in D.groupby(["eps", "design"]):
            c = g.groupby("budget").agg(act=("act", "mean"), cost=("cost", "mean")).sort_index()
            x, y = c.cost.to_numpy(), c.act.to_numpy()
            k = np.argmax(y >= 0.5) if (y >= 0.5).any() else None
            out[(e, des)] = np.nan if k is None else (x[0] if k == 0 else x[k-1] + (0.5 - y[k-1]) * (x[k] - x[k-1]) / (y[k] - y[k-1]))
        return out

    rows = []
    for lp in ("ende", "zhen"):
        for lab, stems in (("mean", [f"{R}/mt/mt_{lp}_m4_p50"]), ("pick", sorted(glob.glob(f"{R}/mt/mt_{lp}_m4_p50_pick[0-9]_draws.parquet")))):
            for s in stems:
                s = s.replace("_draws.parquet", "")
                J = j50(s)
                for e in (0.01, 0.02):
                    best = min(J[(e, "dedup")], J[(e, "weighted")])
                    rows.append(dict(lp=lp, eps=e, label=lab, run=os.path.basename(s), J_uniform=J[(e, "uniform")],
                                     dedup=1 - J[(e, "dedup")] / J[(e, "uniform")], weighted=1 - J[(e, "weighted")] / J[(e, "uniform")],
                                     best_fixed=1 - best / J[(e, "uniform")]))
    T = pd.DataFrame(rows)
    S = T.groupby(["lp", "eps", "label"])[["dedup", "weighted", "best_fixed"]].agg(["mean", "min", "max"])
    return ["## Locked cells: design saving over uniform (J50), mean vs one random rating per identical-string group", "",
            "(100 x fraction; pick: three seeds of the random rating, mean/min/max)", "", (100 * S).round(1).to_markdown(), ""]


if __name__ == "__main__":
    main()
