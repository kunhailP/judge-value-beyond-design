#!/usr/bin/env python3
"""Boundary-stress calibration: is any (run, design, budget) cell's type-I error significantly above alpha = 0.10?
One-sided exact binomial test per cell, Bonferroni over cells; normal bound (locked) and Student-t bound (robustness,
110_unit_audit.py --bound t). The maximum over hundreds of cells is biased upward (Monte-Carlo SE ~0.017 at 300 draws)."""
import glob, os
import numpy as np, pandas as pd
from scipy.stats import binomtest
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
lines = []
for tag, pat in [("normal (locked)", "*/*_boundary_draws.parquet"), ("Student t", "*/*_boundary_tbound_draws.parquet")]:
    rows = []
    for f in glob.glob(f"{R}/{pat}"):
        d = pd.read_parquet(f); g = d.groupby(["design", "budget"]).wrong.agg(["sum", "count"]).reset_index()
        g["domain"] = "arena" if "arena" in os.path.basename(f) else "mt"; rows.append(g)
    G = pd.concat(rows)
    G["p"] = [binomtest(int(s), int(n), 0.10, alternative="greater").pvalue for s, n in zip(G["sum"], G["count"])]
    for dom, h in G.groupby("domain"):
        lines.append(f"| {tag} | {dom} | {len(h)} | {(h['sum'] / h['count']).max():.3f} | {(h.p < .05).mean():.3f} | {min(1, h.p.min() * len(h)):.2f} |")
md = ["## Boundary-stress calibration (α = 0.10)", "",
      "| bound | domain | cells | max type-I | share of cells with p < .05 (≤ .05 expected) | Bonferroni p of the worst cell |",
      "|---|---|---|---|---|---|"] + lines
open(f"{R}/BOUNDARY_CALIBRATION.md", "w").write("\n".join(md) + "\n"); print("\n".join(md))
