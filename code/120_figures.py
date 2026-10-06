#!/usr/bin/env python3
"""Paper figures (PDF + PNG) from the committed results. Palette: validated categorical slots (blue, orange, aqua) with
direct labels / marker shapes as secondary encoding; recessive grid; one y-axis per panel."""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "..", "results"); OUT = os.path.join(HERE, "..", "paper", "figures")
os.makedirs(OUT, exist_ok=True)
BLUE, ORANGE, AQUA, GREY, INK, INK2 = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": GREY, "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e0",
                     "grid.linewidth": 0.6, "legend.frameon": False, "font.family": "serif", "pdf.fonttype": 42})


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.pdf", bbox_inches="tight"); fig.savefig(f"{OUT}/{name}.png", dpi=200, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- Figure 1: levels of evaluator quality (31 WMT22 metrics)
T = pd.read_csv(f"{R}/MTME_TABLE.csv")
T = T[T.metric != "REUSE-src"]          # negatively correlated metric; lambda >= 0 switches it off (reported in the table)
T["hes_best"] = T[["hes_best_0.01", "hes_best_0.02"]].mean(1)
T["hes_oracle"] = T[["hes_w_oracle_0.01", "hes_w_oracle_0.02"]].mean(1)
fig, ax = plt.subplots(1, 3, figsize=(7.0, 2.4), sharey=True); fig.subplots_adjust(wspace=0.12)
for lp, c, mk, lab in (("ende", BLUE, "o", "en→de"), ("zhen", ORANGE, "s", "zh→en")):
    g = T[T.lp == lp]
    ax[0].scatter(g.sys_pearson, g.hes_best, s=14, c=c, marker=mk, edgecolor="white", linewidth=0.5, label=lab, zorder=3)
    ax[1].scatter(g.top4_kendall + np.random.default_rng(1).uniform(-.03, .03, len(g)), g.hes_best, s=14, c=c, marker=mk, edgecolor="white", linewidth=0.5, zorder=3)
    ax[2].scatter(g.rho_bar, g.hes_best, s=14, c=c, marker=mk, edgecolor="white", linewidth=0.5, zorder=3)
    ax[2].scatter(g.rho_bar, g.hes_oracle, s=14, facecolor="none", edgecolor=c, marker=mk, linewidth=0.7, zorder=2)
r = np.linspace(0, .42, 50)
ax[2].plot(r, r ** 2, color=GREY, lw=1, ls="--"); ax[2].text(.405, .15, "ρ²", color=INK2, fontsize=7)
for a in ax:
    a.axhline(0, color=GREY, lw=0.8)
ax[0].set_xlabel("system-level Pearson\n(11 WMT systems)"); ax[1].set_xlabel("Kendall τ among\nthe top-4 systems"); ax[2].set_xlabel("decision-level ρ̄\n(paired differences)")
ax[0].set_ylabel("HES over best fixed\njudge-free baseline")
ax[0].legend(loc="upper left", fontsize=7, handletextpad=0.2)
ax[2].text(0.01, 0.135, "open: oracle λ", color=INK2, fontsize=7)
for a, t in zip(ax, ("(a) global ranking", "(b) local ranking", "(c) decision level")):
    a.set_title(t, fontsize=8, loc="left", color=INK)
save(fig, "F1_levels")

# ---------------------------------------------------------------- Figure 2: where the savings come from
ir = pd.read_csv(f"{R}/ir/IR_HES_long.csv"); ir = ir[(ir.variant == "p20") & (ir.metric == "J50") & (ir.eps == 0.02)]
rows = []
for c, lab in (("antique", "ANTIQUE"), ("cast19", "CAsT"), ("dbpedia-entity", "DBpedia"), ("dl212223", "DL 21–23")):
    J = ir[ir.collection == c].set_index("arm").value
    rows.append((f"IR {lab}", 1 - J["weighted"] / J["uniform"], 1 - J["cvl_llm"] / J["uniform"]))
for lp, lab in (("ende", "en→de"), ("zhen", "zh→en")):
    g = T[T.lp == lp]; e = 0.01
    best = g.loc[g[f"hes_best_{e}"].idxmax()]
    d = best[f"design_save_{e}"]; rows.append((f"MT {lab}", d, 1 - (1 - d) * (1 - best[f"hes_best_{e}"])))
fig, ax = plt.subplots(figsize=(3.4, 2.2))
y = np.arange(len(rows))[::-1]
for yi, (lab, d, tot) in zip(y, rows):
    ax.barh(yi, d, color=BLUE, height=0.6, zorder=3)
    ax.barh(yi, tot - d, left=d, color=ORANGE, height=0.6, zorder=3, edgecolor="white", linewidth=1)
    inc = tot - d
    ax.text(max(tot, d) + 0.01, yi, f"{d:.0%} {'+' if inc >= 0 else '−'} {abs(inc):.0%}", va="center", fontsize=7, color=INK2)
ax.set_yticks(y, [r[0] for r in rows]); ax.set_xlim(0, 0.8); ax.set_xlabel("share of uniform-sampling human labels saved (J50)")
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="judge-free decision-aware design"), Patch(color=ORANGE, label="+ best evaluator on top")],
          loc="upper center", bbox_to_anchor=(0.45, -0.28), ncol=2, fontsize=6.5); ax.grid(axis="y", visible=False)
save(fig, "F2_waterfall")

# ---------------------------------------------------------------- Figure 3: controlled rho dial + the cost law
D = pd.read_csv(f"{R}/RHO_DIAL.csv")
fig, ax = plt.subplots(figsize=(3.4, 2.3))
m = D.groupby("rho")[["real", "pred", "ceil"]].mean()
for run, g in D.groupby("run"):
    ax.plot(g.groupby("rho").real.mean(), color=GREY, lw=0.6, alpha=0.6, zorder=1)
ax.plot(m.index, m.real, color=BLUE, lw=2, marker="o", ms=4, label="realised (mean of 7 runs)", zorder=3)
ax.plot(m.index, m.pred, color=ORANGE, lw=1.5, ls="--", label="cost law [ρ² − (1−ρ²)/P_eff](1 − P/J)", zorder=2)
ax.plot(m.index, m.ceil, color=INK2, lw=1, ls=":", label="ceiling ρ²(1 − P/J)", zorder=2)
ax.axvspan(0.07, 0.38, color="#e6e5e0", zorder=0); ax.text(0.09, -0.035, "real evaluators", fontsize=6.5, color=INK2)
ax.set_xlabel("decision-level ρ (semi-synthetic evaluator)"); ax.set_ylabel("HES"); ax.legend(loc="upper left", fontsize=6.5)
save(fig, "F3_rho_dial")

# ---------------------------------------------------------------- Figure 4: Arena close pairs + presentation order
fig, ax = plt.subplots(1, 2, figsize=(7.0, 2.2), gridspec_kw=dict(width_ratios=[1.6, 1]))
names = {"qwen3_8b": ("Qwen3-8B", BLUE, "o"), "mistral_7b": ("Mistral-7B", ORANGE, "s"), "longer": ("longer wins", AQUA, "^")}
for k, pid in enumerate(range(10, 16)):
    s = pd.read_csv(f"{R}/arena/arena_{pid}_m2_p50_summary.csv"); s = s[(s.metric == "HES_uniform_J50") & (s.eps == 0.05)].drop_duplicates("design").set_index("design")
    for j, (f, (lab, c, mk)) in enumerate(names.items()):
        v = s.loc[f]; x = k + (j - 1) * 0.22
        ax[0].errorbar(x, v.value, yerr=[[v.value - v.lo], [v.hi - v.value]], fmt=mk, color=c, ms=4, elinewidth=0.8, capsize=0, label=lab if k == 0 else None, zorder=3)
info = [json.load(open(f"{R}/arena/arena_{p}_m2_p50_info.json")) for p in range(10, 16)]
ax[0].set_xticks(range(6), [f"P{10+k}\nΔ={abs(i['mu'][0]-i['mu'][1]):.3f}" for k, i in enumerate(info)], fontsize=6.5)
ax[0].axhline(0, color=GREY, lw=0.8); ax[0].set_ylabel("HES over uniform (ε = 0.05)"); ax[0].legend(fontsize=7, ncol=3, loc="upper center", bbox_to_anchor=(0.5, -0.22))
ax[0].set_title("(a) six close Arena pairs (lock v0.9)", fontsize=8, loc="left")
O = pd.read_csv(f"{R}/ARENA_ORDER.csv").groupby(["judge", "order"])[["rho"]].mean().reset_index()
for i, (f, (lab, c, mk)) in enumerate(list(names.items())[:2]):
    g = O[O.judge == f].set_index("order").rho
    vals = [g["x shown first"], g["y shown first"], g["both orders"]]
    ax[1].bar(np.arange(3) + i * 0.38, vals, width=0.34, color=c, label=lab, zorder=3)
ax[1].set_xticks(np.arange(3) + 0.19, ["one order\n(x first)", "one order\n(y first)", "both orders\naveraged"], fontsize=6.5)
ax[1].set_ylabel("decision-level ρ"); ax[1].legend(fontsize=7); ax[1].set_title("(b) position bias lowers ρ", fontsize=8, loc="left")
ax[1].grid(axis="x", visible=False)
save(fig, "F4_arena")
print("figures written to", OUT)
