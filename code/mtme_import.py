#!/usr/bin/env python3
"""Import the segment-level scores of every WMT22 submitted metric (google-research/mt-metrics-eval, data
https://data.statmt.org/wmt26/mt-metrics-eval-v2.tgz) as judges for the MT block (lock v1.1).

One judge per metric: the reference-based variant scored against refA (the reference the MQM pool keeps) and the
reference-free (-src) variants; refB duplicates are skipped. Line i of a system's segment scores is segment seg_id = i + 1
of the MQM pool (verified: 100% string match of the system outputs on both language pairs).
Writes $JV_DATA/mt/{ende,zhen}/judge_mtme_<metric>.parquet (seg_id, system, score) and $JV_DATA/mt/MTME_METRICS.txt.
"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
ROOT = os.path.join(DATA, "mtme", "mt-metrics-eval-v2", "wmt22")
names = {}
for lp, ours in (("en-de", "ende"), ("zh-en", "zhen")):
    pool = pd.read_parquet(f"{DATA}/mt/{ours}/pool.parquet", columns=["seg_id", "system"])
    systems = set(pool.system); n_seg = None
    for fn in sorted(os.listdir(f"{ROOT}/metric-scores/{lp}")):
        if not fn.endswith(".seg.score") or not (fn.endswith("-refA.seg.score") or fn.endswith("-src.seg.score")):
            continue
        metric = fn[:-len(".seg.score")]
        rows = []
        cnt = {}
        for line in open(f"{ROOT}/metric-scores/{lp}/{fn}", encoding="utf-8"):
            sys_, sc = line.rstrip("\n").split("\t")
            i = cnt.get(sys_, 0); cnt[sys_] = i + 1
            if sys_ in systems:
                rows.append((i + 1, sys_, float(sc) if sc not in ("None", "") else float("nan")))
        d = pd.DataFrame(rows, columns=["seg_id", "system", "score"])
        d = pool.merge(d, on=["seg_id", "system"], how="left")
        cov = d.score.notna().mean()
        if cov < 0.99:
            print(f"skip {lp} {metric}: coverage {cov:.3f}"); continue
        safe = metric.replace("/", "_")
        d.to_parquet(f"{DATA}/mt/{ours}/judge_mtme_{safe}.parquet", index=False)
        names.setdefault(ours, []).append(f"mtme_{safe}")
    print(lp, len(names.get(ours, [])), "metrics")
with open(f"{DATA}/mt/MTME_METRICS.txt", "w") as f:
    for lp, ns in names.items():
        f.write(lp + "\t" + " ".join(ns) + "\n")
print(open(f"{DATA}/mt/MTME_METRICS.txt").read())
