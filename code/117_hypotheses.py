#!/usr/bin/env python3
"""Verdicts of the pre-registered hypotheses (locks v0.8, v0.9) from the locked runs. Writes results/HYPOTHESES.md."""
import glob, json, os
import numpy as np, pandas as pd
from scipy.stats import spearmanr, beta
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
TEST_MT = ["comet22", "qwen3_8b", "mistral_7b"]; TEST_AR = ["qwen3_8b", "mistral_7b", "longer"]
out = []


def S(stem):
    return pd.read_csv(f"{stem}_summary.csv")


def val(s, metric, design, eps):
    v = s[(s.metric == metric) & (s.design == design) & (s.eps == eps)]
    return (v.value.iloc[0], v.lo.iloc[0] if "lo" in v else np.nan) if len(v) else (np.nan, np.nan)


# ---- H1, H2 (MT primary cells)
h1, h2, rows = [], [], []
for lp in ("ende", "zhen"):
    s = S(f"{R}/mt/mt_{lp}_m4_p50")
    for eps in (0.01, 0.02):
        bh = s[(s.metric == "best_human") & (s.eps == eps)].design.iloc[0]
        save = val(s, f"save_vs_uniform_J50", bh, eps)[0] if bh != "uniform" else 0.0
        hes = {f: val(s, "HES_best_J50", f, eps)[0] for f in TEST_MT}
        hesu = {f: val(s, "HES_uniform_J50", f, eps)[0] for f in TEST_MT}
        fbest = max(hes, key=hes.get); fu = max(hesu, key=hesu.get)
        infl = val(s, "inflation_J50", fu, eps)[0]
        h1.append(save > hes[fbest]); h2.append(infl >= 0.05)
        rows.append(f"| {lp} | {eps} | {bh} | {save:+.3f} | {fbest} {hes[fbest]:+.3f} | {fu} {hesu[fu]:+.3f} | {infl:+.3f} |")
out += ["## H1 / H2 (MT, primary cells: pilot 50, ε ∈ {0.01, 0.02})", "",
        "| lp | ε | best human | its saving vs uniform | best judge HES over best human | best judge HES over uniform | inflation |",
        "|---|---|---|---|---|---|---|"] + rows + ["",
        f"**H1** (≥ 3/4 cells: design saving > best judge HES): {sum(h1)}/4 → {'SUPPORTED' if sum(h1) >= 3 else 'NOT SUPPORTED'}",
        f"**H2** (≥ 3/4 cells: inflation ≥ 0.05): {sum(h2)}/4 → {'SUPPORTED' if sum(h2) >= 3 else 'NOT SUPPORTED'}", ""]


# ---- H3 (2-system menus)
def h3(stems, judges, eps_list, label):
    pts, best = [], []
    for st in stems:
        s = S(st); m = pd.read_parquet(f"{st}_meta.parquet")
        for eps in eps_list:
            hs = {f: val(s, "HES_best_J50", f, eps)[0] if len(s[(s.metric == "HES_best_J50")]) else val(s, "HES_uniform_J50", f, eps)[0] for f in judges}
            if any(np.isnan(v) for v in hs.values()):
                hs = {f: val(s, "HES_uniform_J50", f, eps)[0] for f in judges}
            for f in judges:
                pts.append((hs[f], m[f"rho:{f}"].median(), m[f"acc:{f}"].median()))
            best.append(max(hs, key=hs.get))
    P = np.array(pts, float); P = P[~np.isnan(P).any(1)]
    r_rho = spearmanr(P[:, 0], P[:, 1])[0]; r_acc = spearmanr(P[:, 0], P[:, 2])[0]
    ok = (r_rho > r_acc) and len(set(best)) >= 2
    return [f"**H3 {label}**: n = {len(P)} (menu × ε × judge); Spearman(HES, pilot ρ) = {r_rho:.3f}, Spearman(HES, pilot accuracy) = {r_acc:.3f}; "
            f"distinct best judges across menus: {sorted(set(best))} → {'SUPPORTED' if ok else 'NOT SUPPORTED'}", ""]


mt_pairs = sorted(st[:-12] for st in glob.glob(f"{R}/mt/mt_*_m2_p50_pair*_summary.csv"))
ar9 = [f"{R}/arena/arena_{p}_m2_p50" for p in range(10, 16)]
ar8 = [f"{R}/arena/arena_{p}_m2_p50" for p in range(0, 6)]
out += ["## H3 (decision-conditional value; 2-system menus)", ""] + h3(mt_pairs, TEST_MT, (0.01, 0.02), "MT (30 pairs)") \
       + h3(ar9, TEST_AR, (0.05, 0.1), "Arena v0.9 (6 pairs)") + h3(ar8, TEST_AR, (0.02, 0.05), "Arena v0.8 (6 pairs; uninformative decision)")


# ---- H4, H5
def h45(cells, label):
    cors, rp, ra = [], [], []
    for st, eps in cells:
        s = S(st); c = s[(s.metric == "pred_corr_logratio") & (s.eps == eps)].value
        if len(c):
            cors.append(c.iloc[0])
        sel = pd.read_csv(f"{st}_selection.csv"); sel = sel[sel.eps == eps].set_index("selector").regret
        rp.append(sel["sel_pilotcost"]); ra.append(sel["sel_accuracy"])
    med = np.nanmedian(cors)
    return [f"**H4 {label}**: median corr(log predicted, log realised post-pilot cost ratio) = {med:.3f} over {len(cors)} cells → {'SUPPORTED' if med >= 0.8 else 'NOT SUPPORTED'}",
            f"**H5 {label}**: mean regret pilot-cost selector = {np.mean(rp):.3f}, accuracy selector = {np.mean(ra):.3f} → {'SUPPORTED' if np.mean(rp) <= np.mean(ra) else 'NOT SUPPORTED'}", ""]


mt_cells = [(f"{R}/mt/mt_{lp}_m4_p50", e) for lp in ("ende", "zhen") for e in (0.01, 0.02)]
ar_cells = [(st, e) for st in ar9 for e in (0.05, 0.1)]
out += ["## H4 / H5", ""] + h45(mt_cells, "MT") + h45(ar_cells, "Arena v0.9")

# ---- H6
cnt, rows = 0, []
for st in ar9:
    s = S(st)
    best = max(TEST_AR, key=lambda f: val(s, "HES_uniform_J50", f, 0.05)[0])
    v = s[(s.metric == "HES_uniform_J50") & (s.design == best) & (s.eps == 0.05)].iloc[0]
    ok = v.value >= 0.05 and v.lo > 0; cnt += ok
    rows.append(f"| {os.path.basename(st)} | {best} | {v.value:+.3f} [{v.lo:+.3f}, {v.hi:+.3f}] | {'yes' if ok else 'no'} |")
out += ["## H6 (Arena v0.9, ε = 0.05: best judge HES ≥ 0.05 with interval above 0)", "", "| run | best judge | HES [95% CI] | meets |", "|---|---|---|---|"] + rows + \
       ["", f"**H6**: {cnt}/6 pairs (needed ≥ 3) → {'SUPPORTED' if cnt >= 3 else 'NOT SUPPORTED'}", ""]

# ---- validity (lock: CP upper <= 0.15 in every regular cell; boundary stress type-I <= 0.15)
reg, bnd = [], []
for f in glob.glob(f"{R}/*/*_draws.parquet"):
    if any(t in f for t in ("_dev", "_syn", "_diag", "_smoke")):
        continue
    d = pd.read_parquet(f, columns=["design", "budget", "eps", "wrong"])
    g = d.groupby(["design", "budget", "eps"]).wrong.agg(["sum", "count"])
    g["cp"] = beta.ppf(0.975, g["sum"] + 1, g["count"] - g["sum"]); g["rate"] = g["sum"] / g["count"]
    (bnd if "boundary" in f else reg).append((os.path.basename(f)[:-14], g.rate.max(), g.cp.max(), g.rate.xs("uniform", level="design").max()))
Rg = pd.DataFrame(reg, columns=["run", "max_wrong", "max_cp", "uniform"]).sort_values("max_cp", ascending=False)
Bd = pd.DataFrame(bnd, columns=["run", "max_wrong", "max_cp", "uniform"]).sort_values("max_wrong", ascending=False)
out += ["## Validity", "",
        f"Regular locked cells ({len(Rg)} runs): max wrong-certificate rate {Rg.max_wrong.max():.3f}, max Clopper–Pearson upper limit "
        f"{Rg.max_cp.max():.3f} ({Rg.run.iloc[0]}) → {'MET' if Rg.max_cp.max() <= 0.15 else 'NOT MET'} (criterion ≤ 0.15)", "",
        f"Boundary stress ({len(Bd)} runs; nominal α = 0.10): max type-I {Bd.max_wrong.max():.3f} ({Bd.run.iloc[0]}) → "
        f"{'MET' if Bd.max_wrong.max() <= 0.15 else 'NOT MET'} (criterion ≤ 0.15). Human-only uniform design alone reaches "
        f"{Bd.uniform.max():.3f}: the normal bound is mildly anti-conservative for binary Arena votes, independent of the judge "
        f"(MT boundary ≤ {Bd[Bd.run.str.startswith('mt')].max_wrong.max():.3f}).", ""]
md = "# Pre-registered hypotheses: verdicts\n\nGenerated by `code/117_hypotheses.py` from the locked runs.\n\n" + "\n".join(out)
open(f"{R}/HYPOTHESES.md", "w").write(md); print(md)
