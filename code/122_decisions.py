#!/usr/bin/env python3
"""Exploratory (post-lock): the 30 two-system MT decisions (top-6 systems per language pair, 15 pairs x 2 LPs) with the
31 WMT22 metric variants, COMET-22 and the two GEMBA judges (code/RUN_PAIRS_MTME.sh).

Per decision and eps (paired bootstrap over the 300 simulated audits, B = 200):
  * J50 of uniform / dedup / weighted, the best fixed judge-free design (by point J50) and its saving over uniform;
  * for every evaluator, HES over that matched base with the coefficient pilot-fixed (cvl), refitted (cvq),
    cross-fitted (cvu) and, on the weighted base, population-optimal (cvo);
  * pilot cost and whether the decision is informative (post-pilot share 1 - P/J50(uniform) >= 0.3, the dilution
    factor of the cost law; otherwise the pilot alone nearly settles it and no evaluator can save much);
and, over all decisions, the simultaneous one-sided coverage of the true mean difference by each estimator's upper bound
(nominal 0.90) at every budget. Writes results/DECISIONS.csv, results/DECISIONS_coverage.csv and results/DECISIONS.md.
"""
import glob, json, os, re
import numpy as np, pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
B = 200
MODES = {"pilot": "cvl", "refit": "cvq", "xfit": "cvu", "oracle": "cvo"}


def j50(x, y, tau=0.5):
    """vectorised j_tau of 111_summarize.py; x, y: [..., budget, design] -> [..., design]."""
    ok = y >= tau
    first = ok.argmax(-2)
    has = ok.any(-2)
    i = np.maximum(first, 1)
    take = lambda a, k: np.take_along_axis(a, k[..., None, :], -2)[..., 0, :]
    x1, y1, x0, y0 = take(x, i), take(y, i), take(x, i - 1), take(y, i - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        interp = x0 + (tau - y0) * (x1 - x0) / (y1 - y0)
    out = np.where(first == 0, take(x, np.zeros_like(first)), interp)
    return np.where(has, out, np.nan)


def main():
    sysr = pd.read_csv(f"{R}/MTME_TABLE.csv").set_index(["lp", "metric"]).sys_pearson
    rows, cov, sel, covj = [], [], [], []
    files = sorted(glob.glob(f"{R}/mt/mt_*_m2_p50_pairmtme*_draws.parquet")) + sorted(glob.glob(f"{R}/arena/arena_1[0-5]_m2_p50_robust2_draws.parquet"))
    for f in files:
        stem = f[:-len("_draws.parquet")]
        if "/arena/" in f:
            lp = "chat"; pair = re.search(r"arena_(\d+)_m2", f).group(1)
        else:
            lp = re.search(r"mt_(\w+?)_m2", f).group(1); pair = stem[-2:]
        D = pd.read_parquet(f)
        if "cover" not in D:
            D["cover"] = np.nan
        M = pd.read_parquet(stem + "_meta.parquet"); info = json.load(open(stem + "_info.json"))
        judges = info["judges"]
        des = D.design.astype("category"); dcat = list(des.cat.categories); dcode = des.cat.codes.to_numpy()
        mode_of = np.array([(re.search(r"_(cv\w):", d).group(1) if re.search(r"_(cv\w):", d) else "human") for d in dcat])
        cv = pd.DataFrame(dict(mode=mode_of[dcode], budget=D.budget.to_numpy(), cover=D.cover.to_numpy()))
        cov.append(cv.groupby(["mode", "budget"]).cover.mean().reset_index().assign(lp=lp, pair=pair))
        pilot_cost = float(M.pilot_cost.mean())
        bud = np.sort(D.budget.unique()); dr = np.sort(D.draw.unique()); epss = np.sort(D.eps.unique())
        bi = np.searchsorted(bud, D.budget.to_numpy()); di = np.searchsorted(dr, D.draw.to_numpy())
        ei = np.searchsorted(epss, D.eps.to_numpy())
        ACT = np.full((len(epss), len(bud), len(dr), len(dcat)), np.nan); CST = ACT.copy()
        ACT[ei, bi, di, dcode] = D.act.to_numpy(); CST[ei, bi, di, dcode] = D.cost.to_numpy()
        COV = np.full((len(epss), len(bud), len(dr), len(dcat)), np.nan); COV[ei, bi, di, dcode] = D.cover.to_numpy()
        rng = np.random.default_rng(0)
        idx = np.vstack([np.arange(len(dr))] + [rng.integers(0, len(dr), len(dr)) for _ in range(B)])   # row 0 = point
        Wt = np.zeros((B + 1, len(dr))); np.add.at(Wt, (np.repeat(np.arange(B + 1), len(dr)), idx.ravel()), 1.0 / len(dr))
        for e_, eps in enumerate(epss):
            human = [d for d in ("uniform", "dedup", "weighted") if d in dcat]
            bases = [d for d in ("dedup", "weighted") if d in dcat] or ["uniform"]
            obase = "weighted" if "weighted" in dcat else "uniform"
            want = human + [f"{b}_{s}:{j}" for j in judges for b in bases for s in ("cvl", "cvq", "cvu")] + [f"{obase}_cvo:{j}" for j in judges]
            want = list(dict.fromkeys(want))
            want = [w for w in want if w in dcat]
            wi = [dcat.index(w) for w in want]
            A = ACT[e_][:, :, wi]; C = CST[e_][:, :, wi]
            Ab = np.einsum("kd,bdj->kbj", Wt, A); Cb = np.einsum("kd,bdj->kbj", Wt, C)   # bootstrap means over draws
            J = j50(Cb, Ab)                                                                 # [B+1, design]
            col = {w: k for k, w in enumerate(want)}
            h = {d: J[:, col[d]] for d in human}
            base = min(bases, key=lambda d: h[d][0] if np.isfinite(h[d][0]) else np.inf)
            best = min(human, key=lambda d: h[d][0] if np.isfinite(h[d][0]) else np.inf)
            save = 1 - h[best] / h["uniform"]
            q = lambda v: (v[0], *np.nanpercentile(v[1:], [2.5, 97.5])) if np.isfinite(v[0]) else (np.nan, np.nan, np.nan)
            common = dict(lp=lp, pair=pair, menu=" vs ".join(info["menu"]), eps=eps, pilot_cost=pilot_cost,
                          J_uniform=h["uniform"][0], J_best=h[best][0], best_fixed=best, base=base,
                          post_share=1 - pilot_cost / h["uniform"][0], informative=bool(1 - pilot_cost / h["uniform"][0] >= 0.3))
            common.update(zip(["save", "save_lo", "save_hi"], q(save)))
            for j in judges:
                r = dict(common, judge=j, rho=float(M[f"rho:{j}"].median()),
                         sys_r=sysr.get((lp, j[5:]), np.nan) if j.startswith("mtme_") else np.nan)
                for m, s in MODES.items():
                    b = base if s != "cvo" else obase
                    k = f"{b}_{s}:{j}"
                    if k in col:
                        v = 1 - J[:, col[k]] / h[b]
                        r[m], r[m + "_lo"], r[m + "_hi"] = q(v)
                rows.append(r)
            # coverage at the budget whose mean cost is nearest each design's J50 (where the certification decision is made)
            for k, w in enumerate(want):
                if np.isfinite(J[0, k]):
                    mc = np.nanmean(CST[e_][:, :, wi[k]], 1); bn = int(np.nanargmin(np.abs(mc - J[0, k])))
                    covj.append(dict(lp=lp, pair=pair, eps=eps, design=w, mode=mode_of[wi[k]], cover=float(np.nanmean(COV[e_][bn, :, wi[k]]))))
            # is the post-hoc best evaluator distinguishable from selection noise? null: all evaluators share their mean;
            # bootstrap deviations (correlated across evaluators through common random numbers) give max - mean under it
            for m, s in (("pilot", "cvl"), ("refit", "cvq"), ("xfit", "cvu")):
                ks = [f"{base}_{s}:{j}" for j in judges if f"{base}_{s}:{j}" in col]
                V = np.stack([1 - J[:, col[k]] / h[base] for k in ks], 1)
                ok = np.isfinite(V).all(1)
                if ok[0] and ok[1:].sum() > 20:
                    obs = V[0].max() - V[0].mean(); E = V[1:][ok[1:]] - V[0]
                    null = E.max(1) - E.mean(1)
                    sel.append(dict(lp=lp, pair=pair, eps=eps, mode=m, gap=obs, null_med=np.median(null), p=float((null >= obs).mean())))
    T = pd.DataFrame(rows); T.to_csv(f"{R}/DECISIONS.csv", index=False)
    C = pd.concat(cov); C.to_csv(f"{R}/DECISIONS_coverage.csv", index=False)
    S = pd.DataFrame(sel); S.to_csv(f"{R}/DECISIONS_selection_noise.csv", index=False)
    pd.DataFrame(covj).to_csv(f"{R}/DECISIONS_coverage_at_J50.csv", index=False)
    report(T, C, S)


def report(T, C, S):
    lab = {"human": "human-only", "cvl": "pilot", "cvq": "refit", "cvu": "xfit", "cvr": "refit_HT", "cvx": "xfit_HT", "cvo": "oracle"}
    md = ["# Thirty two-system MT decisions (exploratory, post-lock)", ""]
    cells = T.drop_duplicates(["lp", "pair", "eps"])
    inf = cells[cells.informative]
    md += [f"Decisions x eps: {len(cells)}; informative (1 - P/J50_uniform >= 0.3): {len(inf)} "
           f"(en-de {int((inf.lp == 'ende').sum())}, zh-en {int((inf.lp == 'zhen').sum())}).", ""]
    Ti = T[T.informative]
    g = Ti.groupby(["lp", "pair", "eps"])
    per = pd.DataFrame({
        "save": g.save.first(), "save_lo": g.save_lo.first(),
        "mean_pilot": g.pilot.mean(), "mean_refit": g.refit.mean(), "mean_xfit": g.xfit.mean(),
        "best_pilot": g.pilot.max(), "best_refit": g.refit.max(), "best_xfit": g.xfit.max(),
        "n_sig_pilot": g.apply(lambda x: int((x.pilot_lo > 0).sum())), "n_sig_refit": g.apply(lambda x: int((x.refit_lo > 0).sum())),
        "n_sig_xfit": g.apply(lambda x: int((x.xfit_lo > 0).sum())), "n_judges": g.size()})
    md += ["## Per informative decision (HES over the matched best fixed judge-free base; mean / best over evaluators)", "",
           (per * 1).round(3).to_markdown(), ""]
    s = lambda c: f"{(per.save > per[c]).mean():.2f}"
    md += ["## Summary over informative decisions", "",
           f"* design saving > mean evaluator HES: pilot {s('mean_pilot')}, refit {s('mean_refit')}, xfit {s('mean_xfit')}",
           f"* design saving > best evaluator HES (post hoc): pilot {s('best_pilot')}, refit {s('best_refit')}, xfit {s('best_xfit')}",
           f"* median design saving {per.save.median():.3f}; median of mean evaluator HES: pilot {per.mean_pilot.median():.3f}, "
           f"refit {per.mean_refit.median():.3f}, xfit {per.mean_xfit.median():.3f}",
           f"* share of (decision, evaluator) with HES interval above 0: pilot {(Ti.pilot_lo > 0).mean():.3f}, "
           f"refit {(Ti.refit_lo > 0).mean():.3f}, xfit {(Ti.xfit_lo > 0).mean():.3f}; below 0: pilot {(Ti.pilot_hi < 0).mean():.3f}", ""]
    per = per.reset_index()
    dom = per.groupby("lp").apply(lambda x: pd.Series(dict(
        cells=len(x), save_median=x.save.median(), mean_pilot=x.mean_pilot.median(), mean_refit=x.mean_refit.median(),
        mean_xfit=x.mean_xfit.median(), design_gt_mean_refit=(x.save > x.mean_refit).mean(), design_gt_best_refit=(x.save > x.best_refit).mean())))
    md += ["## By domain (medians over informative decision x eps cells)", "", dom.round(3).to_markdown(), ""]
    # which evaluator-level quantity ranks HES
    from scipy.stats import spearmanr
    mt = Ti[Ti.judge.str.startswith("mtme_")]
    for m in ("pilot", "refit", "oracle"):
        a = spearmanr(mt.rho, mt[m], nan_policy="omit")[0]; b = spearmanr(mt.sys_r, mt[m], nan_policy="omit")[0]
        md.append(f"* Spearman over (decision, metric): HES_{m} vs pilot rho {a:.3f}, vs system-level Pearson {b:.3f}")
    Smt = S[S.lp != "chat"].merge(T.drop_duplicates(["lp", "pair", "eps"])[["lp", "pair", "eps", "informative"]], on=["lp", "pair", "eps"])
    Smt = Smt[Smt.informative]
    md += ["", "## Post-hoc best evaluator vs selection noise (MT informative decisions only)", "",
           Smt.groupby("mode").agg(cells=("p", "size"), gap_median=("gap", "median"), null_median=("null_med", "median"),
                                   share_p_below_05=("p", lambda x: (x < .05).mean())).round(3).to_markdown()]
    Si = S.merge(T.drop_duplicates(["lp", "pair", "eps"])[["lp", "pair", "eps", "informative"]], on=["lp", "pair", "eps"])
    Si = Si[Si.informative]
    md += ["", "## Post-hoc best evaluator vs selection noise (informative decisions)", "",
           Si.groupby("mode").agg(cells=("p", "size"), gap_median=("gap", "median"), null_median=("null_med", "median"),
                                  share_p_below_05=("p", lambda x: (x < .05).mean())).round(3).to_markdown()]
    CJ = pd.read_csv(f"{R}/DECISIONS_coverage_at_J50.csv").dropna(subset=["cover"])
    CJ["mode"] = CJ["mode"].map(lab)
    md += ["", "## Coverage at the budget nearest each design's J50 (all decisions with a finite J50; nominal 0.90)", "",
           CJ.groupby("mode").cover.agg(["count", "mean", "median", lambda x: (x < 0.85).mean()]).rename(columns={"<lambda_0>": "share_below_0.85"}).round(3).to_markdown()]
    md += ["", "## Coverage of the true mean difference by the upper bound (nominal 0.90), over all 30 decisions", ""]
    C = C.assign(mode=C["mode"].map(lab))
    C["bq"] = pd.qcut(C.groupby(["lp", "pair"]).budget.rank(method="dense"), 3, labels=["small", "medium", "large"])
    tab = C.groupby(["mode", "bq"], observed=True).cover.agg(["mean", "min"]).unstack()
    md += [tab.round(3).to_markdown(), ""]
    open(f"{R}/DECISIONS.md", "w").write("\n".join(md)); print("\n".join(md))


if __name__ == "__main__":
    main()
