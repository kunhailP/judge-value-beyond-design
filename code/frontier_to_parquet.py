#!/usr/bin/env python3
"""Convert frontier judge outputs to the judge files read by 110_unit_audit.py (scoring rule fixed in lock v1.0).

MT  : score = expected value over the first-token top-20 alternatives that parse as an integer 0..100 (renormalised),
      when logprobs exist and those alternatives carry >= 0.5 probability; otherwise the first number in the text
      (clipped to 0..100); NaN if none.        -> $JV_DATA/mt/<lp>/judge_<name>.parquet (seg_id, system, score)
Arena: P(A) = renormalised probability of first tokens "A" vs "B" (stripped) when logprobs exist and carry >= 0.5;
      otherwise 1/0 from the first A/B letter in the text, 0.5 if none. p_x = mean(P(A | x first), 1 - P(A | y first)).
                                               -> $JV_DATA/arena/judge_<name>_v09.parquet (battle_id, p_x, ...)
usage: frontier_to_parquet.py <judge_name>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
import json, math, os, re, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.join(HERE, "..", "frontier", "outputs")
name = sys.argv[1]


def load(task):
    p = os.path.join(OUTD, f"{task}__{name}.jsonl")
    recs = {}
    for l in open(p):
        r = json.loads(l)
        if r["error"] is None or r["id"] not in recs:
            recs[r["id"]] = r
    return recs


def mt_score(r):
    if r["top"]:
        vals = [(int(t.strip()), math.exp(lp)) for t, lp in r["top"] if t.strip().isdigit() and 0 <= int(t.strip()) <= 100]
        mass = sum(p for _, p in vals)
        if mass >= 0.5:
            return sum(v * p for v, p in vals) / mass
    m = re.search(r"\d+(?:\.\d+)?", r["text"] or "")
    return float(np.clip(float(m.group()), 0, 100)) if m else np.nan


def p_a(r):
    if r["top"]:
        pa = sum(math.exp(lp) for t, lp in r["top"] if t.strip() == "A"); pb = sum(math.exp(lp) for t, lp in r["top"] if t.strip() == "B")
        if pa + pb >= 0.5:
            return pa / (pa + pb)
    m = re.search(r"\b([AB])\b", r["text"] or "")
    return (1.0 if m.group(1) == "A" else 0.0) if m else 0.5


for lp in ("ende", "zhen"):
    try:
        R = load(f"mt_{lp}")
    except FileNotFoundError:
        continue
    rows = [dict(seg_id=int(k.split("|")[0]) if k.split("|")[0].isdigit() else k.split("|")[0], system=k.split("|")[1], score=mt_score(r)) for k, r in R.items()]
    d = pd.DataFrame(rows); d.to_parquet(f"{DATA}/mt/{lp}/judge_{name}.parquet", index=False)
    print(lp, len(d), "rows, NaN", d.score.isna().mean().round(4), "quantiles", d.score.quantile([0, .05, .5, .95, 1]).round(1).tolist())
try:
    R = load("arena_v09")
    b = {}
    for k, r in R.items():
        bid, order = k.rsplit("|", 1); b.setdefault(bid, {})[order] = p_a(r)
    d = pd.DataFrame([dict(battle_id=k, p_x_order1=v.get("1", np.nan), p_x_order2=1 - v.get("2", np.nan)) for k, v in b.items()])
    d["p_x"] = d[["p_x_order1", "p_x_order2"]].mean(axis=1)
    d.to_parquet(f"{DATA}/arena/judge_{name}_v09.parquet", index=False)
    print("arena_v09", len(d), "battles, NaN", d.p_x.isna().mean().round(4))
except FileNotFoundError:
    pass
