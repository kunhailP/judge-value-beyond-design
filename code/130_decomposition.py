#!/usr/bin/env python3
"""Same-condition decomposition of the saving over uniform sampling (refitted coefficient, main; frozen, secondary):
  A uniform, no evaluator       B uniform + evaluator
  C dedup, no evaluator         D dedup + evaluator
on the same audits, menus, pilot and eps. Shares of uniform-sampling labels: s_D = 1 - C/A (design), h = 1 - D/C (HES over
the design), s_total = 1 - D/A = s_D + (1 - s_D) h, and s_B = 1 - B/A (evaluator on uniform sampling).
Evaluators: the mean over the submitted metrics, the pre-fixed COMET-22, the strongest evaluator of the year by pilot rho
(reference), and the post-hoc best (reference). Writes a CSV and figures/F6_decomposition.pdf.
usage: 130_decomposition.py --glob22 'results/mt/mt_*_m2_p50_pairmtme??' --glob23 'results/mt/mt_*23_m2_p50_pair23??' --out results/strategies/DECOMPOSITION
"""
import argparse, glob, importlib.util, os, re
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("st", os.path.join(HERE, "128_strategies.py")); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
FIXED = {"22": "mtme_COMET-22-refA", "23": "mtme_COMET-refA"}
STRONG = {"22": "mtme_metricx_xxl_MQM_2020-refA", "23": "mtme_XCOMET-XXL-refA"}


def run(globpat, year, mode, inf=0.3):
    rows = []
    for stem in sorted(f[:-len("_draws.parquet")] for f in glob.glob(globpat + "_draws.parquet")):
        cell = st.Cell(stem); lp = re.search(r"mt_(\w+?)_m2", os.path.basename(stem)).group(1); pair = stem[-2:]; n = len(cell.dr)
        J = lambda d, e: cell.j50(e, np.full(n, cell.col[d]))[0]
        for e in cell.eps:
            A, C = J("uniform", e), J("dedup", e); P = cell.pilot_cost.mean()
            informative = bool(1 - P / A >= inf) if np.isfinite(A) else False
            B = {f: J(f"uniform_{mode}:{f}", e) for f in cell.judges}; D = {f: J(f"dedup_{mode}:{f}", e) for f in cell.judges}
            rho = {f: float(np.nanmedian(cell.M[f"rho:{f}"])) for f in cell.judges}
            best = min(D, key=lambda f: D[f] if np.isfinite(D[f]) else np.inf)
            for name, f in (("mean", None), ("COMET-22", FIXED[year]), ("strongest", STRONG[year]), ("best post hoc", best)):
                b = np.nanmean(list(B.values())) if f is None else B[f]; d = np.nanmean(list(D.values())) if f is None else D[f]
                rows.append(dict(year=year, lp=lp, pair=pair, eps=e, informative=informative, evaluator=name, judge=f or "", rho=np.nan if f is None else rho[f],
                                 A=A, B=b, C=C, D=d, s_D=1 - C / A, s_B=1 - b / A, h=1 - d / C, s_total=1 - d / A, labels_design=A - C, labels_judge=C - d))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--glob22", required=True); ap.add_argument("--glob23", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    T = pd.concat([run(a.glob22, "22", m).assign(mode=m) for m in ("cvq", "cvl")] + [run(a.glob23, "23", m).assign(mode=m) for m in ("cvq", "cvl")])
    T.to_csv(a.out + ".csv", index=False)
    T["comp"] = (1 - T.s_D) * T.h; Ti = T[T.informative]
    g = Ti.groupby(["mode", "year", "evaluator"]).agg(cells=("s_D", "size"), s_D=("s_D", "median"), s_B=("s_B", "median"), h=("h", "median"), s_total=("s_total", "median"),
                                                     s_D_mean=("s_D", "mean"), h_mean=("h", "mean"), comp_mean=("comp", "mean"), s_total_mean=("s_total", "mean"), design_gt_judge=("labels_design", lambda x: np.nan)).reset_index()
    g["design_gt_judge"] = [((Ti[(Ti["mode"] == r["mode"]) & (Ti.year == r.year) & (Ti.evaluator == r.evaluator)].labels_design > Ti[(Ti["mode"] == r["mode"]) & (Ti.year == r.year) & (Ti.evaluator == r.evaluator)].labels_judge).mean()) for _, r in g.iterrows()]
    g.to_csv(a.out + "_summary.csv", index=False)
    md = ["# Same-condition decomposition (informative cells; medians of shares of uniform-sampling labels)", "",
          "s_D = design saving (A→C); s_B = evaluator on uniform (A→B); h = HES over dedup (C→D); s_total = 1 − D/A = s_D + (1 − s_D)h; comp_mean = mean over cells of the evaluator's component (1 − s_D)h, so s_D_mean + comp_mean = s_total_mean exactly (the figure stacks these means; medians do not add); design_gt_judge = share of cells in which the design saves more labels than the evaluator adds on dedup.", "",
          g.round(3).to_markdown(index=False)]
    open(a.out + ".md", "w").write("\n".join(md)); print("\n".join(md))
    # figure: refit, both years; per cell the saving splits exactly as s_total = s_D + (1 - s_D) h; the bars stack the MEANS over cells of
    # the two components (so the bar height is the mean of s_total), the dashed line is the mean s_D, dots are the cells' s_total
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
    order = ["mean", "COMET-22", "strongest", "best post hoc"]; lab = {y: f"WMT{y} ({int(g[(g.year.astype(str) == y) & (g['mode'] == 'cvq')].cells.iloc[0])} cells)" for y in ("22", "23")}
    for ax, year in zip(axes, ("22", "23")):
        X = Ti[(Ti["mode"] == "cvq") & (Ti.year == year)]
        sD = X.s_D.mean(); ax.axhline(sD, color="0.3", lw=1, ls="--")
        for k, ev in enumerate(order):
            Y = X[X.evaluator == ev]; comp = (1 - Y.s_D) * Y.h                       # the evaluator's component per cell; s_D + comp == s_total
            ax.bar(k, Y.s_D.mean(), color="#9ecae1", width=0.6)
            ax.bar(k, comp.mean(), bottom=Y.s_D.mean(), color="#3182bd" if ev in ("mean", "COMET-22") else "#fd8d3c", width=0.6)
            ax.scatter(np.full(len(Y), k) + np.random.default_rng(0).uniform(-0.18, 0.18, len(Y)), Y.s_total, s=6, color="0.2", alpha=0.5, zorder=3)
            ax.text(k, max(Y.s_total.mean(), Y.s_total.quantile(0.9)) + 0.012, f"+{100*comp.mean():.1f}", ha="center", fontsize=7)
        ax.set_xticks(range(4)); ax.set_xticklabels(["mean\nevaluator", "COMET-22\n(fixed)", "strongest\n(reference)", "post-hoc best\n(reference)"], fontsize=7)
        ax.set_title(lab[year], fontsize=9); ax.set_ylim(-0.05, 0.45); ax.tick_params(axis="y", labelsize=7); ax.axhline(0, color="k", lw=0.5)
    axes[0].set_ylabel("share of uniform-sampling labels saved", fontsize=8)
    fig.text(0.5, -0.02, "means over cells; light bars and dashed line: judge-free dedup design alone (A→C); dark: evaluator added on the same design with a refitted coefficient (C→D); dots: cells", ha="center", fontsize=7)
    fig.tight_layout(); fig.savefig(os.path.join(HERE, "..", "paper", "figures", "F6_decomposition.pdf"), bbox_inches="tight"); fig.savefig(os.path.join(HERE, "..", "paper", "figures", "F6_decomposition.png"), dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()
