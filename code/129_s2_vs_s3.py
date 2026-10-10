#!/usr/bin/env python3
"""Direct, paired comparison of the pre-fixed evaluator (S2) with pilot selection (S3), and the coverage / error of every
strategy, on the records of 110_unit_audit.py (addendum to lock v1.2).

Per cell c: G_c = 1 - J50(S3, c) / J50(S2, c)  (> 0: selection cheaper), both strategies evaluated on the same audits.
Uncertainty: the audits of every cell share the random streams of 110_unit_audit.py (same seed, same draw index), so one
set of resampled draw indices is applied to every cell at once (paired over audits, joint over cells). Primary pooled
estimate: the mean of G_c over cells, with the Monte-Carlo interval from these joint draws (the benchmark is fixed; the
interval is simulation noise only). Sensitivity: decisions as clusters, point estimate the mean over decisions of the
within-decision mean, interval from a cluster bootstrap over decisions combined with the joint draws. Also D2_c =
1 - J50(S2)/J50(S1) and D3_c = 1 - J50(S3)/J50(S1), coverage of the chosen arm's upper bound at every budget and at the
budget nearest J50, the wrong-certificate rate by budget (boundary runs: type-I error, with the budget from which the
pooled rate is no longer significantly above alpha), and optionally a restricted protocol that certifies only from a
minimum budget on (--min_budget lp:budget ...; the same rule for every strategy).
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
    ap.add_argument("--out", required=True); ap.add_argument("--alpha", type=float, default=0.10)
    ap.add_argument("--min_budget", nargs="*", default=[], help="lp:budget; restricted protocol: no certificate below this post-pilot budget for any strategy")
    ap.add_argument("--cells_from", default=None, help="CSV of another run of this script whose 'informative' flags define the cell set (fixed cell set across protocols)")
    a = ap.parse_args()
    stems = sorted(f[:-len("_draws.parquet")] for f in glob.glob(a.glob + "_draws.parquet"))
    minb = {kv.split(":")[0]: float(kv.split(":")[1]) for kv in a.min_budget}
    ref = None
    if a.cells_from:
        R0 = pd.read_csv(a.cells_from); ref = {(r.lp, str(r.pair).zfill(2), round(float(r.eps), 6)): bool(r.informative) for r in R0.itertuples()}
    rng = np.random.default_rng(1); rows = []; covrows = []; wbrows = []; boots = None; wcurves = {}
    for stem in stems:
        cell = CellC(stem)
        lp = re.search(r"mt_(\w+?)_m2", os.path.basename(stem)).group(1); pair = stem[-2:]
        if lp in minb:                                         # restricted protocol: no certificate below the minimum budget
            cell.allow_from(minb[lp])                            # (J50 interpolated over the allowed budgets only)
        n = len(cell.dr)
        if boots is None:
            boots = [rng.integers(0, n, n) for _ in range(a.boot)]   # one resampling of draw indices, shared by every cell
        assert len(cell.dr) == len(boots[0]), "cells must have the same number of audits"
        for e in cell.eps:
            S = st.strategies(cell, e, a.design, a.fixed, a.mode, a.stat, a.r0, -1.0)
            uni = np.full(n, cell.col["uniform"]); Ju, _ = cell.j50(e, uni); P = cell.pilot_cost.mean()
            informative = bool(1 - P / Ju >= a.inf) if np.isfinite(Ju) else False
            if ref is not None:
                informative = ref.get((lp, pair, round(float(e), 6)), False)
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
                xa = np.where(cell.allowed, x, np.nan); bn = int(np.nanargmin(np.abs(xa - J[k]))) if np.isfinite(J[k]) else -1
                covrows.append(dict(lp=lp, pair=pair, eps=e, informative=informative, strategy=k, cover_all=float(np.nanmean(cv)), cover_min_budget=float(np.nanmin(np.nanmean(cv, 1))),
                                    cover_at_J50=float(np.nanmean(cv[bn])) if bn >= 0 else np.nan, wrong_at_J50=float(np.nanmean(w[bn])) if bn >= 0 else np.nan, wrong_max=float(np.nanmax(np.nanmean(w, 1))), wrong_mean=float(np.nanmean(w))))
                wm = np.nanmean(w, 1); cm = np.nanmean(c, 1); wcurves[(lp, pair, e, k)] = w
                wbrows += [dict(lp=lp, pair=pair, eps=e, strategy=k, budget=int(cell.bud[i]), cost=float(cm[i]), wrong=float(wm[i]),
                                n_wrong=int(np.nansum(w[i])), n_draws=int(np.isfinite(w[i]).sum())) for i in range(len(cell.bud))]
            print(f"{lp} {pair} eps={e} inf={informative} G={G:+.3f} [{r['G_lo']:+.3f},{r['G_hi']:+.3f}] D2={D2:+.3f} D3={D3:+.3f}", flush=True)
    T = pd.DataFrame(rows); C = pd.DataFrame(covrows); WB = pd.DataFrame(wbrows)
    T.drop(columns=["Gb", "D2b", "D3b"]).to_csv(a.out + ".csv", index=False); C.to_csv(a.out + "_coverage.csv", index=False); WB.to_csv(a.out + "_wrong_by_budget.csv", index=False)
    # pooled: cluster bootstrap over decisions (both eps together), combined with the within-cell paired bootstrap
    md = [f"# S2 (fixed {a.fixed}) vs S3 (pilot selection by {a.stat}), {a.mode}; {a.glob}", "",
          f"G = 1 - J50(S3)/J50(S2) per cell, paired over audits ({T.n_audits.iloc[0]} per cell, {a.boot} bootstrap draws); positive = selection cheaper. "
          f"Margin of practical equivalence: {a.margin:.0%} (lock v1.2 addendum).", ""]
    def pooled(X, col, bcol):
        M = np.stack(X[bcol].to_numpy())                                   # [cells, B]; draw b is the same resampling in every cell
        pt = float(np.nanmean(X[col])); mc = np.nanmean(M, 0)
        decs = X.drop_duplicates(["lp", "pair"])[["lp", "pair"]].to_numpy(); m = len(decs); B = M.shape[1]
        idx = [np.where((X.lp == d[0]).to_numpy() & (X.pair == d[1]).to_numpy())[0] for d in decs]
        Dm = np.stack([np.nanmean(M[i], 0) for i in idx]); ptd = float(np.nanmean([np.nanmean(X[col].to_numpy()[i]) for i in idx]))
        picks = rng.integers(0, m, (B, m)); vals = np.array([np.nanmean(Dm[picks[b], b]) for b in range(B)])
        return dict(mean=pt, lo=float(np.nanpercentile(mc, 2.5)), hi=float(np.nanpercentile(mc, 97.5)),
                    dmean=ptd, dlo=float(np.nanpercentile(vals, 2.5)), dhi=float(np.nanpercentile(vals, 97.5)))
    out = []
    for name, X in (("informative", T[T.informative]), ("all 60", T)):
        for lp, Y in [("pooled", X)] + list(X.groupby("lp")):
            if len(Y) == 0: continue
            g = pooled(Y, "G", "Gb"); d2 = pooled(Y, "D2", "D2b"); d3 = pooled(Y, "D3", "D3b")
            verdict = "S3 better" if g["lo"] > 0 else ("S2 as good (gain of the margin excluded)" if g["hi"] < a.margin else "undecided")
            out.append(dict(cells=name, lp=lp, n=len(Y), G_mean=g["mean"], G_lo=g["lo"], G_hi=g["hi"], share_G_pos=(Y.G > 0).mean(), D2_mean=d2["mean"], D2_lo=d2["lo"], D2_hi=d2["hi"], D3_mean=d3["mean"], D3_lo=d3["lo"], D3_hi=d3["hi"], verdict=verdict,
                            G_dec=g["dmean"], G_dec_lo=g["dlo"], G_dec_hi=g["dhi"], D2_dec=d2["dmean"], D2_dec_lo=d2["dlo"], D2_dec_hi=d2["dhi"], D3_dec=d3["dmean"], D3_dec_lo=d3["dlo"], D3_dec_hi=d3["dhi"]))
    O = pd.DataFrame(out); O.to_csv(a.out + "_pooled.csv", index=False)
    main_cols = ["cells", "lp", "n", "G_mean", "G_lo", "G_hi", "share_G_pos", "D2_mean", "D2_lo", "D2_hi", "D3_mean", "D3_lo", "D3_hi", "verdict"]
    dec_cols = ["cells", "lp", "n", "G_dec", "G_dec_lo", "G_dec_hi", "D2_dec", "D2_dec_lo", "D2_dec_hi", "D3_dec", "D3_dec_lo", "D3_dec_hi"]
    md += ["## Pooled, primary: mean over cells; 95% Monte-Carlo interval from the joint resampling of draw indices (fixed benchmark)", "", O[main_cols].round(4).to_markdown(index=False), "",
           "## Pooled, sensitivity: decisions as clusters (point = mean over decisions of the within-decision mean; cluster bootstrap over decisions x joint draws)", "", O[dec_cols].round(4).to_markdown(index=False), ""]
    if minb: md.insert(3, f"Restricted protocol: no certificate below post-pilot budget {minb} (same rule for every strategy).")
    Ti = T[T.informative]
    md += ["## Per-cell interval widths (informative cells, medians)", "",
           f"G: {np.median(Ti.G_hi - Ti.G_lo):.3f}; D2 (S2 vs S1): {np.median(Ti.D2_hi - Ti.D2_lo):.3f}; D3 (S3 vs S1): {np.median(Ti.D3_hi - Ti.D3_lo):.3f}",
           f"cells with G interval above 0: {(Ti.G_lo > 0).sum()}/{len(Ti)}; below 0: {(Ti.G_hi < 0).sum()}/{len(Ti)}; D2 above 0: {(Ti.D2_lo > 0).sum()}; D3 above 0: {(Ti.D3_lo > 0).sum()}", ""]
    Ci = C[C.informative]
    md += ["## Coverage of the chosen arm's upper bound (nominal 0.90) and wrong certificates, informative cells", "",
           Ci.groupby("strategy")[["cover_all", "cover_min_budget", "cover_at_J50", "wrong_at_J50", "wrong_max", "wrong_mean"]].agg(["mean", "min", "max"]).round(3).to_markdown(), ""]
    # wrong-certificate rate at every post-pilot budget, all cells (boundary runs: type-I error at nominal alpha = 0.10, since every certificate is wrong there)
    wb = WB.pivot_table(index="budget", columns="strategy", values="wrong", aggfunc="mean"); wmax = WB.groupby(["strategy", "lp", "pair", "eps"]).wrong.max().groupby("strategy").agg(["mean", "max"])
    md += [f"## Wrong-certificate rate by post-pilot budget, mean over all {len(T)} cells (boundary runs: type-I error, nominal {a.alpha})", "",
           "Budgets are expected sampled items (Poisson design); 'cost' is the realised mean number of human labels, pilot included.", "", wb.round(3).to_markdown(), "",
           "Per-cell maximum over budgets, mean / max over cells:", "", wmax.round(3).to_markdown(), ""]
    # per language pair, strategy and budget: mean over the pair's cells of the wrong-certificate rate, with a 95% Monte-Carlo interval
    # from the joint resampling of draw indices (the cells share random streams, so draws are not independent across cells and the
    # cells x draws are not pooled as independent trials); the range reported is the first budget from which the OBSERVED mean rate is
    # at or below alpha at every later budget (a description of this simulation, not a test that the rate is below alpha)
    rng_rows = []; cmp_rows = []
    for lp in sorted(set(k[0] for k in wcurves)):
        keys = [k for k in wcurves if k[0] == lp]; strategies_ = sorted(set(k[3] for k in keys)); buds = sorted(set(WB[WB.lp == lp].budget))
        for st_ in strategies_:
            W = np.stack([wcurves[k] for k in keys if k[3] == st_])            # [cells, budget, draw]
            rate = np.nanmean(np.nanmean(W, 2), 0)                              # mean over cells of the per-cell rate
            mcb = np.array([np.nanmean(np.nanmean(W[:, :, bb], 2), 0) for bb in boots])   # [B, budget]
            lo, hi = np.nanpercentile(mcb, 2.5, 0), np.nanpercentile(mcb, 97.5, 0)
            cost = WB[(WB.lp == lp) & (WB.strategy == st_)].groupby("budget").cost.mean().reindex(buds).to_numpy()
            ok = rate <= a.alpha; first = next((i for i in range(len(ok)) if ok[i:].all()), len(ok) - 1)
            for i, bud in enumerate(buds):
                rng_rows.append(dict(lp=lp, strategy=st_, budget=int(bud), cost=round(float(cost[i]), 1), rate=round(float(rate[i]), 3), mc_lo=round(float(lo[i]), 3), mc_hi=round(float(hi[i]), 3), from_here_on="*" if i == first else ""))
        S1 = WB[(WB.lp == lp) & (WB.strategy == "S1_design")].set_index(["pair", "eps", "budget"]).wrong
        for k in ("S2_fixed", "S3_select", "S4_select_or_abstain"):
            d = (WB[(WB.lp == lp) & (WB.strategy == k)].set_index(["pair", "eps", "budget"]).wrong - S1).dropna()
            cmp_rows.append(dict(lp=lp, strategy=k, cells_x_budgets=len(d), mean_diff_vs_S1=round(float(d.mean()), 4), share_above_S1=round(float((d > 0).mean()), 3), share_above_S1_by_2pts=round(float((d > 0.02).mean()), 3), max_diff=round(float(d.max()), 3)))
    R = pd.DataFrame(rng_rows)
    md += [f"### Mean rate per budget and language pair, 95% Monte-Carlo interval from the joint resampling of draw indices (* = from this budget on, the observed mean rate is at or below {a.alpha} at every later budget; an observation on this simulation, not a test)", "",
           R.to_markdown(index=False), "",
           "### Each strategy against S1 on the same cell and budget (difference of wrong-certificate rates)", "", pd.DataFrame(cmp_rows).to_markdown(index=False), ""]
    R.to_csv(a.out + "_certification_range.csv", index=False)
    md += [           "## Per cell", "", T.drop(columns=["Gb", "D2b", "D3b"]).round(3).to_markdown(index=False)]
    open(a.out + ".md", "w").write("\n".join(md)); print("\n".join(md[:12]))


if __name__ == "__main__":
    main()
