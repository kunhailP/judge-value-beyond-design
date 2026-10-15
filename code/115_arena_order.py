#!/usr/bin/env python3
"""Exploratory: position bias of the Arena judges. One presentation order (@o1, @o2) vs both orders averaged:
decision-level rho, pairwise accuracy (pilot medians) and HES with pilot and oracle lambda (v0.9 pairs, pilot 50)."""
import glob, os
import pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
rows = []
for f in sorted(glob.glob(f"{R}/arena/arena_1[0-5]_m2_p50_diag_summary.csv")):
    s = pd.read_csv(f); m = pd.read_parquet(f.replace("_summary.csv", "_meta.parquet"))
    for eps, g in s.groupby("eps"):
        J = g[g.metric == "J50"].set_index("design").value
        for j in ["qwen3_8b", "mistral_7b"]:
            for v, lab in [("@o1", "x shown first"), ("@o2", "y shown first"), ("", "both orders")]:
                k = j + v
                rows.append(dict(pair=os.path.basename(f).split("_")[1], eps=eps, judge=j, order=lab, rho=m[f"rho:{k}"].median(),
                                 acc=m[f"acc:{k}"].median(), hes_pilot=1 - J[f"uniform_cvl:{k}"] / J["uniform"],
                                 hes_oracle=1 - J[f"uniform_cvo:{k}"] / J["uniform"]))
T = pd.DataFrame(rows); T.to_csv(f"{R}/ARENA_ORDER.csv", index=False)
print(T.groupby(["judge", "order"])[["rho", "acc", "hes_pilot", "hes_oracle"]].mean().round(3).to_string())
