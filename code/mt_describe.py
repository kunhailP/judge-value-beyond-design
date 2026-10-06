"""Describe MT pools: system ranking and pairwise stats for top-4 / top-6 menus.

Run: python3 -I code/mt_describe.py
"""
import itertools
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mt_common import LPS, load_pool, dissimilarity  # noqa: E402

pd.set_option("display.width", 200)


def pair_table(W, H, systems):
    rows = []
    for a, b in itertools.combinations(systems, 2):
        d = W[a] - W[b]
        ident = (H[a] == H[b])
        dis = np.array([dissimilarity(x, y) for x, y in zip(H[a], H[b])])
        rows.append(dict(a=a, b=b, gap=d.mean(), se=d.std(ddof=1) / np.sqrt(len(d)), sd_diff=d.std(ddof=1),
                         frac_ident=ident.mean(), sd_diff_nonident=d[~ident].std(ddof=1),
                         mean_dissim=dis.mean(), corr_absdiff_dissim=np.corrcoef(np.abs(d), dis)[0, 1]))
    return pd.DataFrame(rows)


for lp in LPS:
    p = load_pool(lp)
    W = p.pivot(index="seg_id", columns="system", values="u")
    H = p.pivot(index="seg_id", columns="system", values="hyp")
    rank = W.mean().sort_values(ascending=False)
    print(f"\n===== {lp}: {W.shape[0]} segments x {W.shape[1]} systems =====")
    tab = pd.DataFrame({"mean_u": rank, "mean_mqm": p.groupby("system").mqm.mean()[rank.index],
                        "mean_chrf": p.groupby("system").chrf.mean()[rank.index]})
    if "u_3r" in p:
        tab["mean_u_3r"] = p.groupby("system").u_3r.mean()[rank.index]
    print(tab.round(4).to_string())
    for k in (4, 6):
        top = list(rank.index[:k])
        print(f"\n-- {lp} top-{k}: {top}")
        print(pair_table(W, H, top).round(4).to_string(index=False))
