#!/usr/bin/env python3
"""Exploratory test of the cost law with an estimation tax on every 2-system menu (MT pairs, Arena v0.8 and v0.9).

Prediction for judge f over the base design h (pilot-fixed lambda, normal fixed-budget approximation):
    HES_pred = [rho^2 - (1 - rho^2) / P_eff] * (1 - P / J_h)          (estimation-taxed)
    HES_ceil = rho^2 * (1 - P / J_h)                                    (oracle lambda; ceiling)
rho   = population correlation of D and the judge's predicted difference over the units with D or Dhat non-zero,
P_eff = pilot units with a non-zero paired difference (expected: P * share of non-zero D),
P     = median pilot labels, J_h = realised J50 of the base design.
Compares with the realised HES (J50) of 111_summarize.py; prints correlation, MAE and the break-even rho.
"""
import glob, json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
spec = __import__("importlib.util").util.spec_from_file_location("ua", os.path.join(HERE, "110_unit_audit.py"))
ua = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(ua)
R = os.path.join(HERE, "..", "results")
rows = []
runs = [(f, "mt") for f in sorted(glob.glob(f"{R}/mt/mt_*_m2_p50_pair*_info.json"))] + \
       [(f, "arena") for f in sorted(glob.glob(f"{R}/arena/arena_*_m2_p*_info.json")) if not any(t in f for t in ("diag", "boundary", "_syn", "_dev", "_smoke"))]
cache = {}
for info_f, dom in runs:
    stem = info_f[:-len("_info.json")]
    info = json.load(open(info_f)); cfgP = info["cfg"]["pilot"]
    if not os.path.exists(stem + "_summary.csv"):
        continue
    S = pd.read_csv(stem + "_summary.csv"); pred = pd.read_parquet(stem + "_pred.parquet")
    key = (dom, tuple(info["menu"]), info.get("N"), tuple(info["judges"]))
    if key not in cache:
        if dom == "mt":
            lp = os.path.basename(stem).split("_")[1]
            cache[key] = ua.load_mt(lp, menu=info["menu"], judges=[j for j in info["judges"] if j != "chrf"] + ["chrf"])
        else:
            pid = os.path.basename(stem).split("_")[1]
            cache[key] = ua.load_arena(pid, judges=info["judges"])
    data = cache[key]
    Y = data["Y"]; D = Y[:, 0] - Y[:, 1]
    nzshare = float((D != 0).mean())
    for eps, g in S.groupby("eps"):
        bh = g[g.metric == "best_human"].design.iloc[0]
        Jh = g[(g.metric == "J50") & (g.design == bh)].value.iloc[0]
        P = pred[pred.eps == eps].pilot_cost.median()
        for f in info["judges"]:
            if f.startswith("inv_"):
                continue
            sc = data["J"][f]; Dh = sc[:, 0] - sc[:, 1]
            m = (D != 0) | (Dh != 0)
            rho = float(np.corrcoef(D[m], Dh[m])[0, 1]) if m.sum() > 2 else 0.0
            rho = max(rho, 0.0)
            Peff = cfgP * nzshare
            share = 1 - P / Jh if np.isfinite(Jh) else np.nan
            # base-matched judge value: CV on the same sampling design as its own humans-only base
            base, arm = ("weighted", f"weighted_cvl:{f}") if dom == "mt" else ("uniform", f"uniform_cvl:{f}")
            Jb = g[(g.metric == "J50") & (g.design == base)].value; Ja = g[(g.metric == "J50") & (g.design == arm)].value
            real = pd.Series([1 - Ja.iloc[0] / Jb.iloc[0]]) if len(Jb) and len(Ja) else pd.Series([], dtype=float)
            Jh = Jb.iloc[0] if len(Jb) else Jh
            share = 1 - P / Jh if np.isfinite(Jh) else np.nan
            rows.append(dict(domain=dom, run=os.path.basename(stem), eps=eps, judge=f, rho=rho, P_eff=Peff, share=share,
                             pred=max(rho ** 2 - (1 - rho ** 2) / Peff, -0.2) * share, ceil=rho ** 2 * share,
                             real=real.iloc[0] if len(real) else np.nan))
T = pd.DataFrame(rows).dropna(subset=["real", "pred"])
T.to_csv(os.path.join(R, "COST_LAW_2system.csv"), index=False)
pd.set_option("display.width", 200)
for dom, g in list(T.groupby("domain")) + [("all", T)]:
    print(f"{dom:6s} n={len(g):4d}  corr(pred,real)={np.corrcoef(g.pred, g.real)[0,1]:.3f}  MAE={np.abs(g.pred-g.real).mean():.3f}  "
          f"corr(ceil,real)={np.corrcoef(g.ceil, g.real)[0,1]:.3f}  share real>ceil+0.03: {(g.real > g.ceil + 0.03).mean():.2f}  "
          f"mean rho={g.rho.mean():.2f}  mean P_eff={g.P_eff.mean():.0f}")
print("judges above break-even (rho^2 > 1/(P_eff+1)):", (T.rho ** 2 > 1 / (T.P_eff + 1)).mean().round(2))
print(T.groupby(["domain", "judge"])[["rho", "pred", "real"]].mean().round(3).to_string())
