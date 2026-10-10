#!/usr/bin/env python3
"""Pre-specified auditor strategies on the two-system decisions (development year WMT22; held-out year WMT23).

Every strategy is a per-audit choice of one arm from the records of 110_unit_audit.py, made with pilot information only:
  S1 design      the fixed judge-free design D (dedup or weighted; fixed on WMT22)
  S2 fixed       D + one evaluator fixed in advance (f_fix; fixed on WMT22) as control variate
  S3 select      D + the evaluator with the best pilot statistic (pilot rho, or predicted post-pilot labels L_pred)
  S4 select/abstain  S3 unless the pilot evidence is weak (pilot rho below r0, or predicted saving below s0): then S1
Reference points (not strategies: they use the realised costs): the post-hoc best evaluator on D, the mean evaluator, and
the cheapest fixed arm overall. Coefficient rule: pilot-fixed (cvl) or refitted on all labels (cvq).
A strategy's cost curve is the mean over audits of the chosen arm's cost and certification at every budget; J50 is the
cost at 50% certification (111_summarize.j_tau), pilot included. Intervals: paired bootstrap over audits.

usage: 128_strategies.py --glob 'results/mt/mt_*_m2_p50_pairmtme??' --design dedup --fixed mtme_COMET-22-refA --mode cvq
                         [--stat rho|lpred] [--r0 0.2] [--s0 0.05] [--judges <prefix>] --out results/STRATEGIES_dev
"""
import argparse, glob, json, os, re
import numpy as np, pandas as pd


def j_tau(x, y, tau=0.5):
    o = np.argsort(x); x = np.asarray(x, float)[o]; y = np.asarray(y, float)[o]
    if y[0] >= tau:
        return float(x[0])
    for i in range(1, len(x)):
        if y[i] >= tau:
            return float(x[i - 1] + (tau - y[i - 1]) * (x[i] - x[i - 1]) / (y[i] - y[i - 1]))
    return float("nan")


def load(stem):
    D = pd.read_parquet(stem + "_draws.parquet"); Pd = pd.read_parquet(stem + "_pred.parquet"); M = pd.read_parquet(stem + "_meta.parquet")
    info = json.load(open(stem + "_info.json"))
    return D, Pd, M, info


class Cell:
    """Arrays ACT/COST/WRONG [eps, budget, draw, design] and pilot quantities per draw."""
    def __init__(self, stem, judges_prefix="mtme_"):
        D, Pd, M, info = load(stem)
        self.info = info; self.judges = [j for j in info["judges"] if j.startswith(judges_prefix)]
        self.dcat = list(D.design.astype("category").cat.categories); code = D.design.astype("category").cat.codes.to_numpy()
        self.bud = np.sort(D.budget.unique()); self.dr = np.sort(D.draw.unique()); self.eps = np.sort(D.eps.unique())
        bi = np.searchsorted(self.bud, D.budget.to_numpy()); di = np.searchsorted(self.dr, D.draw.to_numpy()); ei = np.searchsorted(self.eps, D.eps.to_numpy())
        shp = (len(self.eps), len(self.bud), len(self.dr), len(self.dcat))
        self.ACT = np.full(shp, np.nan); self.COST = np.full(shp, np.nan); self.WRONG = np.full(shp, np.nan)
        self.ACT[ei, bi, di, code] = D.act.to_numpy(); self.COST[ei, bi, di, code] = D.cost.to_numpy(); self.WRONG[ei, bi, di, code] = D.wrong.to_numpy()
        self.M = M.set_index("draw").loc[self.dr]
        self.pilot_cost = self.M.pilot_cost.to_numpy(float)
        self.L = {e: Pd[Pd.eps == e].pivot(index="draw", columns="design", values="L_pred").loc[self.dr] for e in self.eps}
        self.col = {d: k for k, d in enumerate(self.dcat)}

    def curve(self, e, choice):
        """choice: array of design indices per draw -> (mean cost, mean act, mean wrong) per budget."""
        ei = int(np.where(self.eps == e)[0][0]); idx = np.arange(len(self.dr))
        c = self.COST[ei][:, idx, choice]; a = self.ACT[ei][:, idx, choice]; w = self.WRONG[ei][:, idx, choice]
        return c, a, w

    def j50(self, e, choice, draws=None):
        c, a, w = self.curve(e, choice)
        if draws is not None:
            c, a, w = c[:, draws], a[:, draws], w[:, draws]
        x, y = c.mean(1), a.mean(1)
        J = j_tau(x, y)
        wr = float(w.mean(1)[int(np.nanargmin(np.abs(x - J)))]) if np.isfinite(J) else np.nan   # wrong-certificate rate at the budget nearest J50
        return J, wr


def strategies(cell, e, design, fixed, mode, stat, r0, s0):
    """Return dict name -> design index per draw."""
    n = len(cell.dr); col = cell.col; J = cell.judges
    arm = lambda f: f"{design}_{mode}:{f}"
    S = {"S1_design": np.full(n, col[design])}
    fx = fixed if fixed in J else None
    S["S2_fixed"] = np.full(n, col[arm(fx)]) if fx and arm(fx) in col else np.full(n, col[design])
    rho = np.stack([cell.M[f"rho:{f}"].to_numpy(float) for f in J], 1)                     # [draw, judge] pilot rho
    L = cell.L[e]; Lp = np.stack([L[arm(f)].to_numpy(float) for f in J], 1); L0 = L[design].to_numpy(float)
    P = cell.pilot_cost
    sav = 1 - (P[:, None] + Lp) / (P[:, None] + L0[:, None])                                   # predicted saving over S1
    if stat == "rho":
        pick = np.nanargmax(np.where(np.isnan(rho), -np.inf, rho), 1)
    else:
        pick = np.nanargmax(np.where(np.isnan(sav), -np.inf, sav), 1)
    chosen = np.array([col[arm(J[k])] for k in pick])
    S["S3_select"] = chosen
    ev_rho = rho[np.arange(n), pick]; ev_sav = sav[np.arange(n), pick]
    weak = (ev_rho < r0) | (ev_sav < s0)
    S["S4_select_or_abstain"] = np.where(weak, col[design], chosen)
    S["_abstain_share"] = float(weak.mean())
    # reference points (realised costs; not available to the auditor)
    S["_judge_arms"] = [col[arm(f)] for f in J if arm(f) in col]
    return S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", required=True); ap.add_argument("--design", default="dedup"); ap.add_argument("--fixed", default="mtme_COMET-22-refA")
    ap.add_argument("--mode", default="cvq", choices=["cvl", "cvq", "cvu"]); ap.add_argument("--stat", default="rho", choices=["rho", "lpred"])
    ap.add_argument("--r0", type=float, default=0.0); ap.add_argument("--s0", type=float, default=-1.0)
    ap.add_argument("--boot", type=int, default=200); ap.add_argument("--judges", default="mtme_")
    ap.add_argument("--inf", type=float, default=0.3, help="informative cell: 1 - P/J50(uniform) >= inf")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    stems = sorted(f[:-len("_draws.parquet")] for f in glob.glob(a.glob + "_draws.parquet"))
    rows, jrows = [], []
    rng = np.random.default_rng(0)
    for stem in stems:
        cell = Cell(stem, a.judges)
        lp = re.search(r"mt_(\w+?)_m2", os.path.basename(stem)).group(1); pair = stem[-2:]
        for e in cell.eps:
            S = strategies(cell, e, a.design, a.fixed, a.mode, a.stat, a.r0, a.s0)
            n = len(cell.dr); boots = [rng.integers(0, n, n) for _ in range(a.boot)]
            uni = np.full(n, cell.col["uniform"]); Ju, _ = cell.j50(e, uni)
            P = cell.pilot_cost.mean(); informative = bool(1 - P / Ju >= a.inf) if np.isfinite(Ju) else False
            res = {}
            for k in ("S1_design", "S2_fixed", "S3_select", "S4_select_or_abstain"):
                J, wr = cell.j50(e, S[k]); Jb = np.array([cell.j50(e, S[k], b)[0] for b in boots])
                res[k] = (J, wr, Jb)
            # reference: every fixed judge arm on D; post-hoc best, mean; cheapest overall arm (any design/mode)
            Jj = np.array([cell.j50(e, np.full(n, k))[0] for k in S["_judge_arms"]])
            Jj_b = np.array([[cell.j50(e, np.full(n, k), b)[0] for k in S["_judge_arms"]] for b in boots])   # [B, judges]
            best_k = int(np.nanargmin(Jj)) if np.isfinite(Jj).any() else -1
            J1, _, J1b = res["S1_design"]
            r = dict(lp=lp, pair=pair, eps=e, N=cell.info["N"], pilot_cost=P, J_uniform=Ju, informative=informative,
                     abstain_share=S["_abstain_share"], n_judges=len(S["_judge_arms"]),
                     J_best_posthoc=float(Jj[best_k]) if best_k >= 0 else np.nan, best_posthoc=cell.judges[best_k] if best_k >= 0 else "",
                     J_mean_judge=float(np.nanmean(Jj)), save_design=1 - J1 / Ju)
            for k, (J, wr, Jb) in res.items():
                r[f"J_{k}"] = J; r[f"wrong_{k}"] = wr
                ex = Jb / J1b - 1
                r[f"excess_{k}"] = J / J1 - 1; r[f"excess_lo_{k}"] = np.nanpercentile(ex, 2.5); r[f"excess_hi_{k}"] = np.nanpercentile(ex, 97.5)
            r["excess_best_posthoc"] = r["J_best_posthoc"] / J1 - 1; r["excess_mean_judge"] = r["J_mean_judge"] / J1 - 1
            # selection-noise null for the post-hoc best: as 122_decisions.py
            V = 1 - Jj_b / J1b[:, None]; obs = (1 - Jj / J1).max() - (1 - Jj / J1).mean(); E = V - (1 - Jj / J1)[None, :]
            null = np.nanmax(E, 1) - np.nanmean(E, 1); r["p_best_vs_noise"] = float(np.nanmean(null >= obs))
            for f in cell.judges:                                     # per-evaluator table (both coefficient rules)
                jr = dict(lp=lp, pair=pair, eps=e, informative=informative, judge=f, rho=float(np.nanmedian(cell.M[f"rho:{f}"])))
                for md in ("cvl", "cvq"):
                    k = f"{a.design}_{md}:{f}"
                    jr[f"HES_{md}"] = 1 - cell.j50(e, np.full(n, cell.col[k]))[0] / J1 if k in cell.col else np.nan
                jrows.append(jr)
            rows.append(r)
            print(f"{lp} {pair} eps={e}: inf={informative} S1 {J1:.0f} S2 {res['S2_fixed'][0]:.0f} S3 {res['S3_select'][0]:.0f} S4 {res['S4_select_or_abstain'][0]:.0f} (abstain {S['_abstain_share']:.2f}) best {r['J_best_posthoc']:.0f} ({r['best_posthoc']})", flush=True)
    T = pd.DataFrame(rows); T.to_csv(a.out + ".csv", index=False)
    Jt = pd.DataFrame(jrows); Jt.to_csv(a.out + "_judges.csv", index=False)
    report(T, a, Jt)


def report(T, a, Jt=None):
    Ti = T[T.informative]
    md = [f"# Auditor strategies ({a.glob}; design={a.design}, fixed={a.fixed}, mode={a.mode}, stat={a.stat}, r0={a.r0}, s0={a.s0})", "",
          f"Cells: {len(T)}; informative (1 - P/J50_uniform >= {a.inf}): {len(Ti)} ({Ti.lp.value_counts().to_dict()})", ""]
    ks = ["S2_fixed", "S3_select", "S4_select_or_abstain", "best_posthoc", "mean_judge"]
    rows = []
    for k in ks:
        ex = Ti[f"excess_{k}"]
        rows.append(dict(strategy=k, mean_excess_over_S1=ex.mean(), median_excess=ex.median(), share_cheaper_than_S1=(ex < 0).mean(),
                         share_costlier_by_2pct=(ex > 0.02).mean(), labels_saved_vs_S1_total=(Ti.J_S1_design - Ti[f"J_{k}"]).sum() if f"J_{k}" in Ti else (Ti.J_S1_design - Ti.J_best_posthoc).sum() if k == "best_posthoc" else (Ti.J_S1_design - Ti.J_mean_judge).sum()))
    md += ["## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)", "", pd.DataFrame(rows).round(4).to_markdown(index=False), ""]
    for lp, x in Ti.groupby("lp"):
        md += [f"### {lp}: {len(x)} cells; median design saving vs uniform {x.save_design.median():.3f}", "",
               pd.DataFrame([dict(strategy=k, mean_excess=x[f'excess_{k}'].mean(), median=x[f'excess_{k}'].median(), share_cheaper=(x[f'excess_{k}'] < 0).mean()) for k in ks]).round(4).to_markdown(index=False), ""]
    md += ["## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)", "",
           pd.DataFrame([dict(strategy=k, wrong=Ti[f"wrong_{k}"].mean(), max=Ti[f"wrong_{k}"].max()) for k in ("S1_design", "S2_fixed", "S3_select", "S4_select_or_abstain")]).round(4).to_markdown(index=False), "",
           f"Abstention share (S4), mean over informative cells: {Ti.abstain_share.mean():.3f}", "",
           f"Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in {(Ti.p_best_vs_noise < .05).mean():.2f} of informative cells", "",
           "## Per informative cell", "",
           Ti[["lp", "pair", "eps", "N", "pilot_cost", "J_uniform", "save_design", "excess_S2_fixed", "excess_S3_select", "excess_S4_select_or_abstain", "abstain_share", "excess_best_posthoc", "best_posthoc", "excess_mean_judge", "p_best_vs_noise"]].round(3).to_markdown(index=False)]
    if Jt is not None and len(Jt):
        Ji = Jt[Jt.informative]
        g = Ji.groupby("judge").agg(rho=("rho", "median"), HES_pilot=("HES_cvl", "mean"), HES_refit=("HES_cvq", "mean"), cells=("eps", "size")).sort_values("rho", ascending=False)
        md += ["", "## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)", "", g.round(3).to_markdown()]
    open(a.out + ".md", "w").write("\n".join(md)); print("\n".join(md[:40]))


if __name__ == "__main__":
    main()
