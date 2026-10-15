#!/usr/bin/env python3
"""Exploratory (post-lock): how large an evaluator saving the 30 two-system MT decisions can rule out.

For every informative MT decision x eps cell (as in 122_decisions.py) and every evaluator, the paired bootstrap over the
simulated audits (B draws of the audit ids, common across arms) gives, for the HES over the matched best fixed judge-free
base with the refitted (cvq), pilot-fixed (cvl) and cross-fitted (cvu) coefficient:
  * the one-sided 95% upper bound of HES, and whether it lies below 5% and below 10% ("a saving of that size is ruled out");
  * the saving in human labels, J50(base) - J50(base + evaluator), with its interval;
  * per cell, the same for the MEAN evaluator HES (all evaluators; the ten with the highest system-level Pearson), which
    122_decisions.py reports only as a point value.
Writes results/EXCLUSION.csv (per cell x evaluator), results/EXCLUSION_cells.csv (per cell) and results/EXCLUSION.md.
usage: 125_exclusion.py [--variant <tag>] [--B 1000] [--thresholds 0.05 0.10]
  --variant: suffix of the run files (e.g. "pick" for _pairmtmepick<ij>, "n2000" for _pairmtmen2000<ij>); default: the paper's runs.
"""
import argparse, glob, json, os, re
import numpy as np, pandas as pd

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
MODES = {"pilot": "cvl", "refit": "cvq", "xfit": "cvu"}


def j50(x, y, tau=0.5):
    ok = y >= tau
    first = ok.argmax(-2); has = ok.any(-2)
    i = np.maximum(first, 1)
    take = lambda a, k: np.take_along_axis(a, k[..., None, :], -2)[..., 0, :]
    x1, y1, x0, y0 = take(x, i), take(y, i), take(x, i - 1), take(y, i - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        interp = x0 + (tau - y0) * (x1 - x0) / (y1 - y0)
    out = np.where(first == 0, take(x, np.zeros_like(first)), interp)
    return np.where(has, out, np.nan)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="")
    ap.add_argument("--B", type=int, default=1000)
    ap.add_argument("--thresholds", nargs="*", type=float, default=[0.05, 0.10])
    ap.add_argument("--informative", type=float, default=0.3)
    a = ap.parse_args()
    V = a.variant; SFX = f"_{V}" if V else ""
    sysr = pd.read_csv(f"{R}/MTME_TABLE.csv").set_index(["lp", "metric"]).sys_pearson
    files = sorted(f for f in glob.glob(f"{R}/mt/mt_*_m2_p*_pairmtme{V}*_draws.parquet") if re.search(rf"pairmtme{V}\d\d_draws", f))
    rows, cells = [], []
    for f in files:
        stem = f[:-len("_draws.parquet")]
        lp = re.search(r"mt_(\w+?)_m2", f).group(1); pair = stem[-2:]
        D = pd.read_parquet(f, columns=["draw", "design", "budget", "eps", "cost", "act"])
        M = pd.read_parquet(stem + "_meta.parquet"); info = json.load(open(stem + "_info.json"))
        judges = info["judges"]; P = info["cfg"]["pilot"]
        des = D.design.astype("category"); dcat = list(des.cat.categories); dcode = des.cat.codes.to_numpy()
        pilot_cost = float(M.pilot_cost.mean())
        bud = np.sort(D.budget.unique()); dr = np.sort(D.draw.unique()); epss = np.sort(D.eps.unique())
        bi = np.searchsorted(bud, D.budget.to_numpy()); di = np.searchsorted(dr, D.draw.to_numpy()); ei = np.searchsorted(epss, D.eps.to_numpy())
        ACT = np.full((len(epss), len(bud), len(dr), len(dcat)), np.nan); CST = ACT.copy()
        ACT[ei, bi, di, dcode] = D.act.to_numpy(); CST[ei, bi, di, dcode] = D.cost.to_numpy()
        rng = np.random.default_rng(0)
        idx = np.vstack([np.arange(len(dr))] + [rng.integers(0, len(dr), len(dr)) for _ in range(a.B)])
        Wt = np.zeros((a.B + 1, len(dr))); np.add.at(Wt, (np.repeat(np.arange(a.B + 1), len(dr)), idx.ravel()), 1.0 / len(dr))
        top10 = {j for j in judges if j.startswith("mtme_")}
        top10 = set(sorted(top10, key=lambda j: -sysr.get((lp, j[5:]), -np.inf))[:10])
        for e_, eps in enumerate(epss):
            human = [d for d in ("uniform", "dedup", "weighted") if d in dcat]
            bases = [d for d in ("dedup", "weighted") if d in dcat] or ["uniform"]
            want = human + [f"{b}_{s}:{j}" for j in judges for b in bases for s in MODES.values()]
            want = [w for w in dict.fromkeys(want) if w in dcat]; wi = [dcat.index(w) for w in want]
            Ab = np.einsum("kd,bdj->kbj", Wt, ACT[e_][:, :, wi]); Cb = np.einsum("kd,bdj->kbj", Wt, CST[e_][:, :, wi])
            J = j50(Cb, Ab); col = {w: k for k, w in enumerate(want)}
            h = {d: J[:, col[d]] for d in human}
            fin = lambda v: v[0] if np.isfinite(v[0]) else np.inf
            base = min(bases, key=lambda d: fin(h[d])); best = min(human, key=lambda d: fin(h[d]))
            post_share = 1 - pilot_cost / h["uniform"][0]
            informative = bool(post_share >= a.informative)
            save = 1 - h[best] / h["uniform"]
            cell = dict(lp=lp, pair=pair, menu=" vs ".join(info["menu"]), eps=eps, pilot=P, pilot_cost=pilot_cost, draws=len(dr),
                        J_uniform=h["uniform"][0], J_base=h[base][0], base=base, post_share=post_share, informative=informative,
                        save=save[0], save_lo=np.nanpercentile(save[1:], 2.5), save_hi=np.nanpercentile(save[1:], 97.5),
                        labels_saved_by_design=h["uniform"][0] - h[best][0])
            per_mode = {}
            for m, s in MODES.items():
                ks = [(j, f"{base}_{s}:{j}") for j in judges if f"{base}_{s}:{j}" in col]
                Vh = np.stack([1 - J[:, col[k]] / h[base] for _, k in ks], 1)        # [B+1, judges] HES
                Lb = np.stack([h[base] - J[:, col[k]] for _, k in ks], 1)           # labels saved by the evaluator
                for (j, k), v, l in zip(ks, Vh.T, Lb.T):
                    if not np.isfinite(v[0]):
                        continue
                    ub = np.nanpercentile(v[1:], 95); lb = np.nanpercentile(v[1:], 5)
                    r = dict(cell, judge=j, mode=m, rho=float(M[f"rho:{j}"].median()), top10=j in top10,
                             hes=v[0], hes_lo=np.nanpercentile(v[1:], 2.5), hes_hi=np.nanpercentile(v[1:], 97.5), ub95=ub, lb95=lb,
                             labels=l[0], labels_lo=np.nanpercentile(l[1:], 2.5), labels_hi=np.nanpercentile(l[1:], 97.5))
                    for t in a.thresholds:
                        r[f"excl_{t:g}"] = bool(ub < t)
                    rows.append(r)
                for lab, sel in (("all", np.ones(len(ks), bool)), ("top10", np.array([j in top10 for j, _ in ks]))):
                    if sel.sum() == 0:
                        continue
                    mv = np.nanmean(Vh[:, sel], 1)
                    per_mode[f"mean_{m}_{lab}"] = mv[0]; per_mode[f"mean_{m}_{lab}_lo"] = np.nanpercentile(mv[1:], 2.5)
                    per_mode[f"mean_{m}_{lab}_hi"] = np.nanpercentile(mv[1:], 97.5); per_mode[f"mean_{m}_{lab}_ub95"] = np.nanpercentile(mv[1:], 95)
                    diff = save - mv                                                 # design saving minus mean evaluator HES
                    per_mode[f"design_minus_mean_{m}_{lab}"] = diff[0]; per_mode[f"design_minus_mean_{m}_{lab}_lo"] = np.nanpercentile(diff[1:], 2.5)
                    per_mode[f"design_minus_mean_{m}_{lab}_hi"] = np.nanpercentile(diff[1:], 97.5)
                    bv = np.nanmax(Vh[:, sel], 1)
                    per_mode[f"best_{m}_{lab}"] = bv[0]; per_mode[f"best_{m}_{lab}_ub95"] = np.nanpercentile(bv[1:], 95)
            cells.append(dict(cell, **per_mode))
    T = pd.DataFrame(rows); C = pd.DataFrame(cells)
    T.to_csv(f"{R}/EXCLUSION{SFX}.csv", index=False); C.to_csv(f"{R}/EXCLUSION_cells{SFX}.csv", index=False)
    report(T, C, a, SFX)


def report(T, C, a, SFX):
    md = [f"# What size of evaluator saving do the two-system MT decisions rule out? (exploratory{', variant ' + a.variant if a.variant else ''})", "",
          f"Informative cells: post-pilot share >= {a.informative}. One-sided 95% upper bound (ub95) of HES over the matched best fixed judge-free base, "
          f"paired bootstrap over the simulated audits (B = {a.B}). 'excluded' = ub95 below the threshold.", ""]
    Ti = T[T.informative]; Ci = C[C.informative]
    md += [f"Cells: {len(Ci)} ({int((Ci.lp == 'ende').sum())} en-de, {int((Ci.lp == 'zhen').sum())} zh-en); draws per cell: {sorted(Ci.draws.unique())}; pilot: {sorted(Ci.pilot.unique())}", ""]
    md += ["## Per (cell, evaluator): share of pairs whose upper bound excludes a saving of t", ""]
    tab = []
    for lab, sub in (("all evaluators", Ti), ("top-10 by system-level Pearson", Ti[Ti.top10])):
        for m in MODES:
            s = sub[sub["mode"] == m]
            r = dict(evaluators=lab, mode=m, n=len(s), median_hes=s.hes.median(), median_ub95=s.ub95.median(), median_halfwidth=((s.hes_hi - s.hes_lo) / 2).median(),
                     share_lb95_above_0=(s.lb95 > 0).mean())
            for t in a.thresholds:
                r[f"excl_{t:g}"] = s[f"excl_{t:g}"].mean()
            tab.append(r)
    md += [pd.DataFrame(tab).round(3).to_markdown(index=False), ""]
    md += ["## Per cell: the mean evaluator (point, 95% interval, one-sided upper bound) and the design's saving", ""]
    for lab in ("all", "top10"):
        for m in MODES:
            k = f"mean_{m}_{lab}"
            if k not in Ci:
                continue
            md.append(f"* {lab}, {m}: median mean-evaluator HES {Ci[k].median():.3f}; median ub95 {Ci[k + '_ub95'].median():.3f}; "
                      f"cells with ub95 < 5%: {(Ci[k + '_ub95'] < 0.05).mean():.2f}, < 10%: {(Ci[k + '_ub95'] < 0.10).mean():.2f}; "
                      f"design saving > mean evaluator: {(Ci['save'] > Ci[k]).mean():.2f}, with the interval of the difference above 0: {(Ci[f'design_minus_mean_{m}_{lab}_lo'] > 0).mean():.2f}, below 0: {(Ci[f'design_minus_mean_{m}_{lab}_hi'] < 0).mean():.2f}")
    md += ["", "## Per cell table (refit, all evaluators)", ""]
    cols = ["lp", "pair", "eps", "J_uniform", "J_base", "base", "post_share", "save", "save_lo", "save_hi", "labels_saved_by_design",
            "mean_refit_all", "mean_refit_all_lo", "mean_refit_all_hi", "mean_refit_top10", "mean_refit_top10_ub95", "best_refit_all", "best_refit_all_ub95"]
    md += [Ci[[c for c in cols if c in Ci]].round(3).to_markdown(index=False), ""]
    md += ["## Labels saved (refit; per cell, mean over evaluators): design vs evaluator", ""]
    g = Ti[Ti["mode"] == "refit"].groupby(["lp", "pair", "eps"]).agg(J_base=("J_base", "first"), design_labels=("labels_saved_by_design", "first"), evaluator_labels_mean=("labels", "mean"), evaluator_labels_best=("labels", "max")).reset_index()
    md += [g.assign(eps=g.eps.round(3)).round(1).to_markdown(index=False), ""]
    open(f"{R}/EXCLUSION{SFX}.md", "w").write("\n".join(md)); print("\n".join(md[:30]))


if __name__ == "__main__":
    main()
