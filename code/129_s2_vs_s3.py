#!/usr/bin/env python3
"""Direct, paired comparison of the pre-fixed evaluator (S2) with pilot selection (S3), and the coverage / error of every
strategy, on the records of 110_unit_audit.py (addendum to lock v1.2).

Per cell c: G_c = 1 - J50(S3, c) / J50(S2, c)  (> 0: selection cheaper), both strategies evaluated on the same audits;
paired bootstrap over audits (B draws). Pooled: mean of G_c over cells with a cluster bootstrap over decisions (both eps
of a decision resampled together). Also D2_c = 1 - J50(S2)/J50(S1) and D3_c = 1 - J50(S3)/J50(S1) with the same bootstrap,
coverage of the chosen arm's upper bound at every budget and at the budget nearest J50, and the wrong-certificate rate
(boundary runs: type-I error).
usage: 129_s2_vs_s3.py --glob 'results/mt/mt_*23_m2_p50_pair23n??' --fixed mtme_COMET-refA [--mode cvq] [--boot 1000] --out results/strategies/S2_vs_S3_wmt23
"""
import argparse, glob, importlib.util, os, re
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("st", os.path.join(HERE, "128_strategies.py")); st = importlib.util.module_from_spec(spec); spec.loader.exec_module(st)


class CellC(st.Cell):
    def __init__(self, stem, judges_prefix="mtme_"):
        super().__init__(stem, judges_prefix)
        D = pd.read_parquet(stem + "_draws.parquet", columns=["draw", "design", "budget", "eps", "cover"])
        code = D.design.astype("category").cat.set_categories(self.dcat).cat.codes.to_numpy()
        bi = np.searchsorted(self.bud, D.budget.to_numpy()); di = np.searchsorted(self.dr, D.draw.to_numpy()); ei = np.searchsorted(self.eps, D.eps.to_numpy())
        self.COVER = np.full(self.ACT.shape, np.nan); self.COVER[ei, bi, di, code] = D.cover.to_numpy()

    def curve_cover(self, e, choice):
        ei = int(np.where(self.eps == e)[0][0]); idx = np.arange(len(self.dr))
        return self.COVER[ei][:, idx, choice]          # [budget, draw]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True); ap.add_argument("--design", default="dedup"); ap.add_argument("--fixed", required=True)
    ap.add_argument("--mode", default="cvq"); ap.add_argument("--stat", default="rho"); ap.add_argument("--r0", type=float, default=0.2)
    ap.add_argument("--boot", type=int, default=1000); ap.add_argument("--inf", type=float, default=0.3); ap.add_argument("--margin", type=float, default=0.02)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    stems = sorted(f[:-len("_draws.parquet")] for f in glob.glob(a.glob + "_draws.parquet"))
    rng = np.random.default_rng(1); rows = []; covrows = []; wbrows = []
    for stem in stems:
        cell = CellC(stem)
        lp = re.search(r"mt_(\w+?)_m2", os.path.basename(stem)).group(1); pair = stem[-2:]
        n = len(cell.dr); boots = [rng.integers(0, n, n) for _ in range(a.boot)]
        for e in cell.eps:
            S = st.strategies(cell, e, a.design, a.fixed, a.mode, a.stat, a.r0, -1.0)
            uni = np.full(n, cell.col["uniform"]); Ju, _ = cell.j50(e, uni); P = cell.pilot_cost.mean()
            informative = bool(1 - P / Ju >= a.inf) if np.isfinite(Ju) else False
            J = {k: cell.j50(e, S[k])[0] for k in ("S1_design", "S2_fixed", "S3_select", "S4_select_or_abstain")}
            Jb = {k: np.array([cell.j50(e, S[k], b)[0] for b in boots]) for k in ("S1_design", "S2_fixed", "S3_select")}
            G = 1 - J["S3_select"] / J["S2_fixed"]; Gb = 1 - Jb["S3_select"] / Jb["S2_fixed"]
            D2 = 1 - J["S2_fixed"] / J["S1_design"]; D2b = 1 - Jb["S2_fixed"] / Jb["S1_design"]
            D3 = 1 - J["S3_select"] / J["S1_design"]; D3b = 1 - Jb["S3_select"] / Jb["S1_design"]
            r = dict(lp=lp, pair=pair, eps=e, informative=informative, J_uniform=Ju, J_S1=J["S1_design"], J_S2=J["S2_fixed"], J_S3=J["S3_select"],
                     G=G, G_lo=np.nanpercentile(Gb, 2.5), G_hi=np.nanpercentile(Gb, 97.5), G_sd=np.nanstd(Gb),
                     D2=D2, D2_lo=np.nanpercentile(D2b, 2.5), D2_hi=np.nanpercentile(D2b, 97.5),
                     D3=D3, D3_lo=np.nanpercentile(D3b, 2.5), D3_hi=np.nanpercentile(D3b, 97.5), n_audits=n)
            r["Gb"] = Gb; r["D2b"] = D2b; r["D3b"] = D3b
            rows.append(r)
            # coverage of the chosen arm: at every budget (mean) and at the budget nearest J50; wrong rate at J50 and max
            for k in ("S1_design", "S2_fixed", "S3_select", "S4_select_or_abstain"):
                cv = cell.curve_cover(e, S[k]); c, act, w = cell.curve(e, S[k]); x = c.mean(1)
                bn = int(np.nanargmin(np.abs(x - J[k]))) if np.isfinite(J[k]) else -1
                covrows.append(dict(lp=lp, pair=pair, eps=e, informative=informative, strategy=k, cover_all=float(np.nanmean(cv)), cover_min_budget=float(np.nanmin(np.nanmean(cv, 1))),
                                    cover_at_J50=float(np.nanmean(cv[bn])) if bn >= 0 else np.nan, wrong_at_J50=float(np.nanmean(w[bn])) if bn >= 0 else np.nan, wrong_max=float(np.nanmax(np.nanmean(w, 1))), wrong_mean=float(np.nanmean(w))))
                wm = np.nanmean(w, 1)
                wbrows += [dict(lp=lp, pair=pair, eps=e, strategy=k, budget=int(cell.bud[i]), wrong=float(wm[i])) for i in range(len(cell.bud))]
            print(f"{lp} {pair} eps={e} inf={informative} G={G:+.3f} [{r['G_lo']:+.3f},{r['G_hi']:+.3f}] D2={D2:+.3f} D3={D3:+.3f}", flush=True)
    T = pd.DataFrame(rows); C = pd.DataFrame(covrows); WB = pd.DataFrame(wbrows)
    T.drop(columns=["Gb", "D2b", "D3b"]).to_csv(a.out + ".csv", index=False); C.to_csv(a.out + "_coverage.csv", index=False); WB.to_csv(a.out + "_wrong_by_budget.csv", index=False)
    # pooled: cluster bootstrap over decisions (both eps together), combined with the within-cell paired bootstrap
    md = [f"# S2 (fixed {a.fixed}) vs S3 (pilot selection by {a.stat}), {a.mode}; {a.glob}", "",
          f"G = 1 - J50(S3)/J50(S2) per cell, paired over audits ({T.n_audits.iloc[0]} per cell, {a.boot} bootstrap draws); positive = selection cheaper. "
          f"Margin of practical equivalence: {a.margin:.0%} (lock v1.2 addendum).", ""]
    def pooled(X, col, bcol):
        decs = X.drop_duplicates(["lp", "pair"])[["lp", "pair"]].to_numpy(); m = len(decs); B = len(X[bcol].iloc[0])
        groups = {tuple(d): X[(X.lp == d[0]) & (X.pair == d[1])] for d in decs}
        vals = []
        for b in range(B):
            pick = rng.integers(0, m, m)
            v = [groups[tuple(decs[i])][bcol].apply(lambda z: z[b]).mean() for i in pick]   # within-cell draw b, cells of resampled decisions
            vals.append(np.nanmean(v))
        return float(X[col].mean()), float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))
    out = []
    for name, X in (("informative", T[T.informative]), ("all 60", T)):
        for lp, Y in [("pooled", X)] + list(X.groupby("lp")):
            if len(Y) == 0: continue
            g = pooled(Y, "G", "Gb"); d2 = pooled(Y, "D2", "D2b"); d3 = pooled(Y, "D3", "D3b")
            verdict = "S3 better" if g[1] > 0 else ("S2 as good (margin excluded)" if g[2] < a.margin else "undecided")
            out.append(dict(cells=name, lp=lp, n=len(Y), G_mean=g[0], G_lo=g[1], G_hi=g[2], share_G_pos=(Y.G > 0).mean(), D2_mean=d2[0], D2_lo=d2[1], D2_hi=d2[2], D3_mean=d3[0], D3_lo=d3[1], D3_hi=d3[2], verdict=verdict))
    O = pd.DataFrame(out); O.to_csv(a.out + "_pooled.csv", index=False)
    md += ["## Pooled (mean over cells; cluster bootstrap over decisions)", "", O.round(4).to_markdown(index=False), ""]
    Ti = T[T.informative]
    md += ["## Per-cell interval widths (informative cells, medians)", "",
           f"G: {np.median(Ti.G_hi - Ti.G_lo):.3f}; D2 (S2 vs S1): {np.median(Ti.D2_hi - Ti.D2_lo):.3f}; D3 (S3 vs S1): {np.median(Ti.D3_hi - Ti.D3_lo):.3f}",
           f"cells with G interval above 0: {(Ti.G_lo > 0).sum()}/{len(Ti)}; below 0: {(Ti.G_hi < 0).sum()}/{len(Ti)}; D2 above 0: {(Ti.D2_lo > 0).sum()}; D3 above 0: {(Ti.D3_lo > 0).sum()}", ""]
    Ci = C[C.informative]
    md += ["## Coverage of the chosen arm's upper bound (nominal 0.90) and wrong certificates, informative cells", "",
           Ci.groupby("strategy")[["cover_all", "cover_min_budget", "cover_at_J50", "wrong_at_J50", "wrong_max", "wrong_mean"]].agg(["mean", "min", "max"]).round(3).to_markdown(), ""]
    # wrong-certificate rate at every post-pilot budget, all cells (boundary runs: type-I error at nominal alpha = 0.10, since every certificate is wrong there)
    wb = WB.pivot_table(index="budget", columns="strategy", values="wrong", aggfunc="mean"); wmax = WB.groupby(["strategy", "lp", "pair", "eps"]).wrong.max().groupby("strategy").agg(["mean", "max"])
    md += [f"## Wrong-certificate rate by post-pilot budget, mean over all {len(T)} cells (boundary runs: type-I error, nominal 0.10)", "", wb.round(3).to_markdown(), "",
           "Per-cell maximum over budgets, mean / max over cells:", "", wmax.round(3).to_markdown(), "",
           "## Per cell", "", T.drop(columns=["Gb", "D2b", "D3b"]).round(3).to_markdown(index=False)]
    open(a.out + ".md", "w").write("\n".join(md)); print("\n".join(md[:12]))


if __name__ == "__main__":
    main()
