#!/usr/bin/env python3
"""J_tau, HES, inflation, selection and pilot-prediction scores for the outputs of 110_unit_audit.py.

usage: 111_summarize.py <results/<domain>/<stem>> [--boot B]
Writes <stem>_summary.csv (one row per eps x design: J50, J80, AUC with paired-bootstrap intervals over draws) and prints
  * savings of human designs over uniform, HES of every judge over uniform and over the best human design, inflation;
  * selection: always-f, accuracy / rho / pilot-cost selectors (per draw), best fixed arm; excess cost over the best fixed arm (by aggregate J50), relative to the best human design (can be negative for adaptive selectors);
  * pilot prediction: corr(log predicted, log realised) post-pilot cost ratio of every design to the reference.
"""
import argparse, os
import numpy as np, pandas as pd


def j_tau(x, y, tau):
    o = np.argsort(x); x = np.asarray(x, float)[o]; y = np.asarray(y, float)[o]
    if y[0] >= tau:
        return float(x[0])
    for i in range(1, len(x)):
        if y[i] >= tau:
            return float(x[i - 1] + (tau - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1]))
    return float("nan")


def curves(T, choice, draws):
    """T: dict design -> DataFrame[budget x draw] of act and cost; choice: Series draw -> design; draws: resampled draw ids."""
    out = []
    budgets = T["act"].index.get_level_values(0).unique()
    for b in budgets:
        acts = T["act"].loc[b]; costs = T["cost"].loc[b]
        ch = choice.loc[draws].to_numpy()
        a = acts.to_numpy()[np.searchsorted(acts.index, draws), [acts.columns.get_loc(x) for x in ch]]
        cc = costs.to_numpy()[np.searchsorted(costs.index, draws), [costs.columns.get_loc(x) for x in ch]]
        out.append((cc.mean(), a.mean()))
    x, y = np.array(out).T
    return dict(J50=j_tau(x, y, 0.5), J80=j_tau(x, y, 0.8))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stem")
    ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--thr", type=float, default=0.05, help="pilot selector abstains to the best human design unless predicted saving > thr")
    a = ap.parse_args()
    R = pd.read_parquet(a.stem + "_draws.parquet"); Pd = pd.read_parquet(a.stem + "_pred.parquet"); Mt = pd.read_parquet(a.stem + "_meta.parquet")
    designs = list(R.design.unique()); judges = sorted({d.split(":")[1] for d in designs if ":" in d})
    human = [d for d in ["uniform", "dedup", "weighted"] if d in designs]
    rng = np.random.default_rng(0)
    rows, sel = [], []
    for eps, g in R.groupby("eps"):
        T = {k: g.pivot_table(index=["budget", "draw"], columns="design", values=k) for k in ["act", "cost"]}
        draws = np.array(sorted(g.draw.unique()))
        pe = Pd[Pd.eps == eps].pivot(index="draw", columns="design", values="L_pred")
        # best human design by point J50 (pre-specified family; reported as such)
        const = {d: pd.Series(d, index=draws) for d in designs}
        pt = {d: curves(T, const[d], draws) for d in designs}
        best_h = min(human, key=lambda d: pt[d]["J50"] if np.isfinite(pt[d]["J50"]) else np.inf)
        cvl_base = "weighted_cvl" if "weighted" in designs else "uniform_cvl"
        # selectors: choose a judge (design `cvl_base:f`) or no judge (best_h)
        def pick(score, larger=True):
            s = score.copy()
            return s.idxmax(axis=1) if larger else s.idxmin(axis=1)
        acc = Mt.set_index("draw")[[f"acc:{f}" for f in judges]].rename(columns=lambda c: f"{cvl_base}:{c[4:]}")
        rho = Mt.set_index("draw")[[f"rho:{f}" for f in judges]].rename(columns=lambda c: f"{cvl_base}:{c[4:]}")
        Lp = pe[[f"{cvl_base}:{f}" for f in judges]]
        pilot_cost = Pd[Pd.eps == eps].groupby("draw").pilot_cost.first()
        sav = 1 - (pilot_cost.values[:, None] + Lp.values) / (pilot_cost.values[:, None] + pe[best_h].values[:, None])
        sav = pd.DataFrame(sav, index=pe.index, columns=Lp.columns)
        bestsav = sav.max(axis=1)
        choices = {**const,
                   "sel_accuracy": pick(acc), "sel_rho": pick(rho),
                   "sel_pilotcost": pd.Series(np.where(bestsav > a.thr, sav.idxmax(axis=1), best_h), index=sav.index)}
        def evaluate(ds):
            return {k: curves(T, ch, ds) for k, ch in choices.items()}
        point = evaluate(draws)
        boots = [evaluate(rng.choice(draws, len(draws), replace=True)) for _ in range(a.boot)]
        def ci(fn):
            v = fn(point); bs = np.array([fn(b) for b in boots], float); bs = bs[np.isfinite(bs)]
            return v, *(np.percentile(bs, [2.5, 97.5]) if len(bs) > 10 else (np.nan, np.nan))
        for d in choices:
            for t in ("J50", "J80"):
                v, lo, hi = ci(lambda r: r[d][t])
                rows.append(dict(eps=eps, design=d, metric=t, value=v, lo=lo, hi=hi))
        for t in ("J50", "J80"):
            for d in human[1:]:
                v, lo, hi = ci(lambda r: 1 - r[d][t] / r["uniform"][t]); rows.append(dict(eps=eps, design=d, metric=f"save_vs_uniform_{t}", value=v, lo=lo, hi=hi))
            for f in judges:
                for base, jd in [("uniform", f"uniform_cvl:{f}"), (best_h, f"{cvl_base}:{f}")]:
                    v, lo, hi = ci(lambda r: 1 - r[jd][t] / r[base][t])
                    rows.append(dict(eps=eps, design=f, metric=f"HES_{'uniform' if base == 'uniform' else 'best'}_{t}", value=v, lo=lo, hi=hi))
                v, lo, hi = ci(lambda r: (1 - r[f"uniform_cvl:{f}"][t] / r["uniform"][t]) - (1 - r[f"{cvl_base}:{f}"][t] / r[best_h][t]))
                rows.append(dict(eps=eps, design=f, metric=f"inflation_{t}", value=v, lo=lo, hi=hi))
        cand = [best_h] + [f"{cvl_base}:{f}" for f in judges]
        for k in cand + ["sel_accuracy", "sel_rho", "sel_pilotcost"]:
            v, lo, hi = ci(lambda r: (r[k]["J50"] - min(r[q]["J50"] for q in cand)) / r[best_h]["J50"])
            sel.append(dict(eps=eps, selector=k, excess_vs_best_fixed=v, lo=lo, hi=hi,
                            best_fixed=min(cand, key=lambda q: point[q]["J50"] if np.isfinite(point[q]["J50"]) else np.inf),
                            picks=dict(choices[k].value_counts(normalize=True).round(2)) if k.startswith("sel") else ""))
        # pilot prediction of relative post-pilot cost (median over draws) vs realised (J50 - pilot)
        P0 = pilot_cost.median(); ref = best_h
        pr = []
        for d in designs:
            if np.isfinite(pt[d]["J50"]) and np.isfinite(pt[ref]["J50"]):
                pr.append((np.log(pe[d].median() / pe[ref].median()), np.log((pt[d]["J50"] - P0) / (pt[ref]["J50"] - P0))))
        if len(pr) > 2:
            x, y = np.array(pr).T
            rows.append(dict(eps=eps, design="ALL", metric="pred_corr_logratio", value=float(np.corrcoef(x, y)[0, 1]), lo=np.nan, hi=np.nan))
        rows.append(dict(eps=eps, design=best_h, metric="best_human", value=np.nan, lo=np.nan, hi=np.nan))
        rows.append(dict(eps=eps, design="ALL", metric="max_wrong", value=float(g.groupby(["design", "budget"]).wrong.mean().max()), lo=np.nan, hi=np.nan))
    out = pd.DataFrame(rows); S = pd.DataFrame(sel)
    out.to_csv(a.stem + "_summary.csv", index=False); S.to_csv(a.stem + "_selection.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 400)
    f = lambda r: f"{r.value:.3f} [{r.lo:.3f},{r.hi:.3f}]" if pd.notna(r.lo) else (f"{r.value:.3f}" if pd.notna(r.value) else "")
    out["s"] = out.apply(f, axis=1)
    print(out.pivot_table(index=["metric", "design"], columns="eps", values="s", aggfunc="first").to_string())
    print(S.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
