"""Import the segment-level scores of every WMT23 submitted metric as judges for the held-out year (ende23, zhen23).
Reference-based variants scored against refA and source-only (-src) variants; synthetic-reference variants and the
Random-sysname baseline are skipped. Line i of a system's segment scores is segment i of the test set (as mtme_import.py).
Writes $JV_DATA/mt/{ende23,zhen23}/judge_mtme_<metric>.parquet and $JV_DATA/mt/MTME_METRICS23.txt."""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
ROOT = os.path.join(DATA, "mtme", "mt-metrics-eval-v2", "wmt23")
names = {}
for lp, ours in (("en-de", "ende23"), ("zh-en", "zhen23")):
    pool = pd.read_parquet(f"{DATA}/mt/{ours}/pool.parquet", columns=["seg_id", "system", "hyp"])
    systems = set(pool.system)
    for fn in sorted(os.listdir(f"{ROOT}/metric-scores/{lp}")):
        if not fn.endswith(".seg.score") or not (fn.endswith("-refA.seg.score") or fn.endswith("-src.seg.score")) or fn.startswith("Random-sysname"):
            continue
        metric = fn[:-len(".seg.score")]
        rows = []; cnt = {}
        for line in open(f"{ROOT}/metric-scores/{lp}/{fn}", encoding="utf-8"):
            sys_, sc = line.rstrip("\n").split("\t")
            i = cnt.get(sys_, 0); cnt[sys_] = i + 1
            if sys_ in systems:
                rows.append((i + 1, sys_, float(sc) if sc not in ("None", "") else float("nan")))
        d = pool[["seg_id", "system"]].merge(pd.DataFrame(rows, columns=["seg_id", "system", "score"]), on=["seg_id", "system"], how="left")
        cov = d.score.notna().mean()
        if cov < 0.99:
            print(f"skip {lp} {metric}: coverage {cov:.3f}"); continue
        safe = metric.replace("/", "_")
        d.to_parquet(f"{DATA}/mt/{ours}/judge_mtme_{safe}.parquet", index=False)
        names.setdefault(ours, []).append(f"mtme_{safe}")
    print(lp, len(names.get(ours, [])), "metrics")
with open(f"{DATA}/mt/MTME_METRICS23.txt", "w") as f:
    for lp, ns in names.items():
        f.write(lp + "\t" + " ".join(ns) + "\n")
