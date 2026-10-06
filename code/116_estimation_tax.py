#!/usr/bin/env python3
"""Exploratory: realised HES with the pilot-fitted lambda vs the population (oracle) lambda, MT top-4 menus, pilot 50.
The difference is the estimation tax of fitting lambda on the pilot."""
import os
import pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "mt")
rows = []
for lp in ("ende", "zhen"):
    s = pd.read_csv(f"{R}/mt_{lp}_m4_p50_diag_summary.csv"); m = pd.read_parquet(f"{R}/mt_{lp}_m4_p50_diag_meta.parquet")
    J = s[s.metric == "J50"].pivot_table(index="design", columns="eps", values="value")
    for f in ["comet22", "qwen3_8b", "mistral_7b", "chrf"]:
        for e in J.columns:
            hp = 1 - J.loc[f"weighted_cvl:{f}", e] / J.loc["weighted", e]; ho = 1 - J.loc[f"weighted_cvo:{f}", e] / J.loc["weighted", e]
            rows.append(dict(lp=lp, judge=f, eps=e, hes_pilot=hp, hes_oracle=ho, tax=ho - hp,
                             lam_pilot_cv=m[f"lam:{f}"].std() / max(m[f"lam:{f}"].mean(), 1e-12)))
T = pd.DataFrame(rows); T.to_csv(os.path.join(R, "..", "ESTIMATION_TAX.csv"), index=False)
print(T.round(3).to_string(index=False))
print(T.groupby("lp")[["hes_pilot", "hes_oracle", "tax"]].mean().round(3))
