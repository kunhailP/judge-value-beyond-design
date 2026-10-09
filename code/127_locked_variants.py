#!/usr/bin/env python3
"""Pre-submission checks on the four locked MT cells (top-4 menus, pilot 50, the 31 WMT22 metric variants), from the
per-draw records (paired bootstrap over the 300 simulated audits, B = 200, as in 122_decisions.py):
  * matched-base comparison: every metric on the best fixed judge-free design of the cell (dedup on zh->en, weighted on
    en->de) with the pilot-fixed (cvl), refitted (cvq) and cross-fitted (cvu) coefficient (run tag _mtmex: the locked
    run plus the --extra arms, same seed; the locked arms reproduce the locked records exactly);
  * the weighted design with four quartile dissimilarity bins instead of the locked three (run tag _mtmeb4).
Writes results/LOCKED_VARIANTS.csv and results/LOCKED_VARIANTS.md.
"""
import json, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
B = 200


def j50(x, y, tau=0.5):
    ok = y >= tau; first = ok.argmax(-2); has = ok.any(-2); i = np.maximum(first, 1)
    take = lambda a, k: np.take_along_axis(a, k[..., None, :], -2)[..., 0, :]
    x1, y1, x0, y0 = take(x, i), take(y, i), take(x, i - 1), take(y, i - 1)
    with np.errstate(invalid="ignore", divide="ignore"):
        interp = x0 + (tau - y0) * (x1 - x0) / (y1 - y0)
    return np.where(has, np.where(first == 0, take(x, np.zeros_like(first)), interp), np.nan)


def load(stem):
    D = pd.read_parquet(stem + "_draws.parquet", columns=["draw", "design", "budget", "eps", "cost", "act"])
    des = D.design.astype("category"); dcat = list(des.cat.categories); dcode = des.cat.codes.to_numpy()
    bud = np.sort(D.budget.unique()); dr = np.sort(D.draw.unique()); epss = np.sort(D.eps.unique())
    bi = np.searchsorted(bud, D.budget.to_numpy()); di = np.searchsorted(dr, D.draw.to_numpy()); ei = np.searchsorted(epss, D.eps.to_numpy())
    ACT = np.full((len(epss), len(bud), len(dr), len(dcat)), np.nan); CST = ACT.copy()
    ACT[ei, bi, di, dcode] = D.act.to_numpy(); CST[ei, bi, di, dcode] = D.cost.to_numpy()
    rng = np.random.default_rng(0)
    idx = np.vstack([np.arange(len(dr))] + [rng.integers(0, len(dr), len(dr)) for _ in range(B)])
    Wt = np.zeros((B + 1, len(dr))); np.add.at(Wt, (np.repeat(np.arange(B + 1), len(dr)), idx.ravel()), 1.0 / len(dr))
    out = {}
    for e_, eps in enumerate(epss):
        J = j50(np.einsum("kd,bdj->kbj", Wt, CST[e_]), np.einsum("kd,bdj->kbj", Wt, ACT[e_]))
        out[eps] = pd.DataFrame(J, columns=dcat)        # row 0 = point estimate, rows 1.. = bootstrap
    return out


def q(v):
    return (float(v[0]), *np.nanpercentile(v[1:], [2.5, 97.5])) if np.isfinite(v[0]) else (np.nan, np.nan, np.nan)


rows = []
for lp in ("ende", "zhen"):
    base_run = load(f"{R}/mt/mt_{lp}_m4_p50_mtme")
    for tag, name in (("_mtmex", "3 bins (locked)"), ("_mtmeb4", "4 bins")):
        stem = f"{R}/mt/mt_{lp}_m4_p50{tag}"
        if not os.path.exists(stem + "_draws.parquet"):
            continue
        run = load(stem)
        for eps, J in run.items():
            J0 = base_run[eps]
            metrics = sorted({d.split(":")[1] for d in J.columns if d.startswith("weighted_cvl:")})
            bh = min(("dedup", "weighted"), key=lambda d: J[d][0])
            r = dict(lp=lp, eps=eps, variant=name, J_uniform=J["uniform"][0], J_dedup=J["dedup"][0], J_weighted=J["weighted"][0], best_fixed=bh)
            for d, k in (("dedup", "dedup_save"), ("weighted", "weighted_save"), (bh, "design_save")):
                r[k], r[k + "_lo"], r[k + "_hi"] = q(1 - J[d] / J["uniform"])
            common = [c for c in J0.columns if c in J.columns]
            r["max_dev_from_locked"] = float(np.nanmax(np.abs(J[common].iloc[0].to_numpy() - J0[common].iloc[0].to_numpy()) / J0[common].iloc[0].to_numpy()))
            for b in ("weighted", "dedup"):
                for mode, suf in (("pilot", "cvl"), ("refit", "cvq"), ("xfit", "cvu")):
                    ks = [(m, f"{b}_{suf}:{m}") for m in metrics if f"{b}_{suf}:{m}" in J.columns]
                    if not ks:
                        continue
                    H = np.stack([1 - J[k].to_numpy() / J[b].to_numpy() for _, k in ks], 1)   # [B+1, metrics]
                    pt = H[0]; ib = int(np.nanargmax(pt))
                    r[f"{b}_{mode}_best"], r[f"{b}_{mode}_best_lo"], r[f"{b}_{mode}_best_hi"] = q(H[:, ib])
                    r[f"{b}_{mode}_best_name"] = ks[ib][0][5:]
                    r[f"{b}_{mode}_median"], r[f"{b}_{mode}_median_lo"], r[f"{b}_{mode}_median_hi"] = q(np.nanmedian(H, 1))
                    r[f"{b}_{mode}_mean"] = float(np.nanmean(pt)); r[f"{b}_{mode}_n_pos"] = int((np.nanpercentile(H[1:], 2.5, 0) > 0).sum())
            rows.append(r)
T = pd.DataFrame(rows); T.to_csv(f"{R}/LOCKED_VARIANTS.csv", index=False)
md = ["# Locked MT cells: matched-base comparison and the four-bin variant (exploratory, pre-submission)", "",
      "J50 (unique human labels, pilot included); savings as fractions with 95% paired-bootstrap (Monte-Carlo) intervals over the 300 audits.", "",
      "## Human-only designs", "",
      T[["lp", "eps", "variant", "J_uniform", "J_dedup", "J_weighted", "best_fixed", "dedup_save", "weighted_save", "weighted_save_lo", "weighted_save_hi", "design_save", "max_dev_from_locked"]].round(3).to_markdown(index=False), "",
      "## The 31 metric variants on the SAME design (HES; best post hoc with its interval, median metric, number with interval above 0)", ""]
cols = ["lp", "eps", "variant"] + [f"{b}_{m}_{k}" for b in ("weighted", "dedup") for m in ("pilot", "refit", "xfit") for k in ("best", "median", "n_pos")]
md += [T[[c for c in cols if c in T]].round(3).to_markdown(index=False), "", "## Table 1 rows (locked bins; evaluators on the best fixed design)", ""]
for _, r in T[T.variant.str.startswith("3")].iterrows():
    b = r.best_fixed; J = r[f"J_{b}"]
    md.append(f"* {r.lp} eps={r.eps}: uniform {r.J_uniform:.0f}; best fixed = {b} {J:.0f} (saves {r.design_save:.1%} [{r.design_save_lo:.1%}, {r.design_save_hi:.1%}]); "
              f"+ best metric ({r[f'{b}_pilot_best_name']}) {J * (1 - r[f'{b}_pilot_best']):.0f} = HES {r[f'{b}_pilot_best']:+.1%} [{r[f'{b}_pilot_best_lo']:+.1%}, {r[f'{b}_pilot_best_hi']:+.1%}]; "
              f"median metric {J * (1 - r[f'{b}_pilot_median']):.0f} = {r[f'{b}_pilot_median']:+.1%}; refit: best {r[f'{b}_refit_best']:+.1%} ({r[f'{b}_refit_best_name']}), median {r[f'{b}_refit_median']:+.1%}; "
              f"cross-fit: best {r[f'{b}_xfit_best']:+.1%}, median {r[f'{b}_xfit_median']:+.1%}")
open(f"{R}/LOCKED_VARIANTS.md", "w").write("\n".join(md)); print("\n".join(md))
