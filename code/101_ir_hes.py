#!/usr/bin/env python3
"""IR block of the NAACL paper: J_tau, HES and judge selection from the per-draw records of the fixed-budget grid.

Input: the *_draws.csv files of `81_sampling_baselines.py --dump_draws` (release asset draw_records.tar.gz).
For every (collection, pilot variant, eps) it reports, per arm and judge,
  J_tau (tau = 0.5, 0.8): unique human labels, pilot included, at which the certification rate of a pre-committed budget
                          reaches tau (linear interpolation between budgets; NaN if never reached);
  AUC                   : mean certification rate over a common label grid (tau-free check);
  HES_s(f)              : 1 - J(s + judge f) / J(s), for base design s = weighted (humans-only decision-weight sampling);
  saving of each human design over uniform;
and judge selection: always-<judge>, per-draw pilot selector (argmin pilot variance ratio; abstain to humans-only if the
ratio is not below `thr`), oracle; regret = (J(selected) - J(oracle)) / J(weighted).
Paired bootstrap over draw indices (the same resample for every arm and judge) gives 95% intervals.
Draws are paired across judges (same permutation and pilot for a given draw index), which the script checks.
"""
import argparse, glob, os, re
import numpy as np, pandas as pd

ARMS_H = ["uniform", "uniform_nz", "weighted"]
JUDGES = ["llm", "rr", "inv"]


def j_tau(x, y, tau):
    o = np.argsort(x); x = np.asarray(x, float)[o]; y = np.asarray(y, float)[o]
    if y[0] >= tau:
        return float(x[0])
    for i in range(1, len(x)):
        if y[i] >= tau:
            return float(x[i - 1] + (tau - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1]))
    return float("nan")


def load(d):
    groups = {}
    for f in glob.glob(os.path.join(d, "baselines_*_draws.csv")):
        n = os.path.basename(f)
        m = re.match(r"baselines_(\w+?)_(llm|rr|inv)(?:_(ho10_covid|ho10_touche|ho_covid|ho_touche|nc10|nc))?_(?:v3)?b\d+_", n)
        groups.setdefault(m.group(3) or "p20", {}).setdefault(m.group(2), []).append(f)
    out = []
    for var, J in groups.items():
        for j, fs in J.items():
            d_ = pd.concat([pd.read_csv(f) for f in fs])
            d_["variant"] = var; d_["judge_run"] = j
            out.append(d_)
    return pd.concat(out)


def cell_tables(g):
    """g: rows of one (collection, variant, eps). Returns wide frames act/docs/vr indexed by (budget, draw), columns = arm keys."""
    keys = {}
    for (j, m), h in g.groupby(["judge_run", "method"]):
        if m in ARMS_H:
            k = m
        elif m == "weighted_cvl":
            k = f"cvl_{j}"
        else:
            continue
        keys.setdefault(k, h.set_index(["budget_full_eq", "draw"]))
    idx = None
    for k, h in keys.items():
        idx = h.index if idx is None else idx.intersection(h.index)
    act = pd.DataFrame({k: h.loc[idx, "act"] for k, h in keys.items()})
    docs = pd.DataFrame({k: h.loc[idx, "docs"] for k, h in keys.items()})
    vr = pd.DataFrame({k: (h.loc[idx, "v_pilot"] / h.loc[idx, "v_pilot_ref"]) for k, h in keys.items() if k.startswith("cvl_")})
    return act, docs, vr


def curve_stats(act, docs, choice, draws_sel, taus=(0.5, 0.8), grid=None):
    """choice: DataFrame/Series giving per-(budget,draw) the arm key; draws_sel: array of draw ids (bootstrap resample)."""
    rows = []
    for b in act.index.get_level_values(0).unique():
        a_b = act.loc[b]; d_b = docs.loc[b]; c_b = choice.loc[b]
        a = np.array([a_b.at[i, c_b.at[i]] for i in draws_sel]); dd = np.array([d_b.at[i, c_b.at[i]] for i in draws_sel])
        rows.append((dd.mean(), a.mean()))
    x, y = np.array(rows).T
    res = {f"J{int(t*100)}": j_tau(x, y, t) for t in taus}
    if grid is not None:
        o = np.argsort(x); res["AUC"] = float(np.interp(grid, x[o], y[o], left=0.0, right=y[o][-1]).mean())
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draws_dir")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "ir"))
    ap.add_argument("--boot", type=int, default=200)
    ap.add_argument("--thr", type=float, default=0.9)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    D = load(a.draws_dir)
    rng = np.random.default_rng(0)
    rows, sel_rows = [], []
    for (c, var, eps), g in D.groupby(["collection", "variant", "eps"]):
        act, docs, vr = cell_tables(g)
        if "weighted" not in act or not any(k.startswith("cvl_") for k in act):
            continue
        draws = np.array(sorted(act.index.get_level_values(1).unique()))
        judges = [k for k in act.columns if k.startswith("cvl_")]
        best = vr[judges].idxmin(axis=1); bestv = vr[judges].min(axis=1)
        choices = {k: pd.Series(k, index=act.index) for k in act.columns}
        choices["sel_pilot"] = pd.Series(np.where(bestv < a.thr, best, "weighted"), index=act.index)
        choices["sel_argmin"] = best
        grid = np.linspace(docs.values.min(), docs["weighted"].groupby(level=0).mean().max(), 50)

        def evaluate(ds):
            return {k: curve_stats(act, docs, ch, ds, grid=grid) for k, ch in choices.items()}

        point = evaluate(draws)
        boots = [evaluate(rng.choice(draws, len(draws), replace=True)) for _ in range(a.boot)]

        def stat(fn):
            v = fn(point); bs = np.array([fn(b) for b in boots], float); bs = bs[np.isfinite(bs)]
            lo, hi = (np.percentile(bs, [2.5, 97.5]) if len(bs) > 10 else (np.nan, np.nan))
            return v, lo, hi

        base = dict(collection=c, variant=var, eps=eps)
        for k in choices:
            for t in ("J50", "J80", "AUC"):
                rows.append({**base, "arm": k, "metric": t, "value": point[k][t]})
        for t in ("J50", "J80"):
            for k in ["uniform_nz", "weighted"]:
                v, lo, hi = stat(lambda r, k=k, t=t: 1 - r[k][t] / r["uniform"][t])
                rows.append({**base, "arm": k, "metric": f"save_vs_uniform_{t}", "value": v, "lo": lo, "hi": hi})
            for k in judges + ["sel_pilot"]:
                v, lo, hi = stat(lambda r, k=k, t=t: 1 - r[k][t] / r["weighted"][t])
                rows.append({**base, "arm": k, "metric": f"HES_weighted_{t}", "value": v, "lo": lo, "hi": hi})
        # selection (J50)
        J = {k: point[k]["J50"] for k in choices}
        cand = ["weighted"] + judges
        oracle = min(cand, key=lambda k: J[k] if np.isfinite(J[k]) else np.inf)
        for k in cand + ["sel_pilot", "sel_argmin"]:
            v, lo, hi = stat(lambda r, k=k: (r[k]["J50"] - min(r[q]["J50"] for q in cand)) / r["weighted"]["J50"])
            sel_rows.append({**base, "selector": k, "regret": v, "lo": lo, "hi": hi, "oracle": oracle,
                             "pick_share": dict(choices[k].value_counts(normalize=True).round(2)) if k.startswith("sel") else ""})
    R = pd.DataFrame(rows); S = pd.DataFrame(sel_rows)
    R.to_csv(os.path.join(a.out, "IR_HES_long.csv"), index=False); S.to_csv(os.path.join(a.out, "IR_selection.csv"), index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    w = R[R.metric.str.startswith(("save_", "HES_"))].copy()
    w["cell"] = w.apply(lambda r: f"{r.value:+.3f} [{r.lo:+.3f},{r.hi:+.3f}]" if pd.notna(r.value) else "n/a", axis=1)
    print(w.pivot_table(index=["collection", "variant", "eps"], columns=["metric", "arm"], values="cell", aggfunc="first").T.to_string())
    print(S.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
