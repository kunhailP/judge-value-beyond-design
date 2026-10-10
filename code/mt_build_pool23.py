"""Build $JV_DATA/mt/{ende23,zhen23}/pool.parquet (held-out year) from mt-metrics-eval-v2/wmt23.

Run:  JV_DATA=... python3 -I code/mt_build_pool23.py
Inputs (untrusted, read-only): $JV_DATA/mtme/mt-metrics-eval-v2/wmt23/
  human-scores/{lp}.mqm.seg.score      Google MQM per segment and system (score = -MQM, mean over raters; "None" = unrated)
  human-scores/{lp}.mqm.rater*.seg.rating   per-rater error lists (used for n_raters and a check of the MQM weights)
  system-outputs/{lp}/{system}.txt, sources/{lp}.txt, references/{lp}.refA.txt, documents/{lp}.docs
Same columns and conventions as mt_build_pool.py (WMT22): segments rated for every kept system; references and the
metric-optimised MBR system excluded; u = -min(MQM, 25)/25; sentence chrF against refA.
"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
from concurrent.futures import ProcessPoolExecutor
import numpy as np, pandas as pd
from mt_common import MT_ROOT, utility, chrf

W = f"{DATA}/mtme/mt-metrics-eval-v2/wmt23"
LPS23 = {"ende23": "en-de", "zhen23": "zh-en"}
EXCLUDE = {"refA", "synthetic_ref", "NLLB_MBR_BLEU"}     # references and the BLEU-MBR system (as *_bestmbr in WMT22)


def _chrf_batch(pairs):
    return [chrf(h, r) for h, r in pairs]


def read_score(path):
    rows = []; cnt = {}
    for line in open(path, encoding="utf8"):
        p = line.rstrip("\n").split("\t"); s = p[0]; i = cnt.get(s, 0) + 1; cnt[s] = i
        rows.append((s, i, p[1]))
    return pd.DataFrame(rows, columns=["system", "seg_id", "raw"])


def build(ours, lp):
    h = read_score(f"{W}/human-scores/{lp}.mqm.seg.score")
    h = h[h.raw != "None"].assign(score=lambda d: d.raw.astype(float)).drop(columns="raw")
    h = h[~h.system.isin(EXCLUDE)]
    keep = sorted(h.system.unique())
    full = h.groupby("seg_id").system.nunique(); segs = sorted(full[full == len(keep)].index)
    h = h[h.seg_id.isin(segs)]
    print(f"[{ours}] systems {len(keep)}: {keep}; segments rated for all of them: {len(segs)}")
    # per-rater error lists: n_raters and a check that the summed error scores reproduce the MQM score
    rr = []
    for f in glob.glob(f"{W}/human-scores/{lp}.mqm.rater*.seg.rating"):
        r = read_score(f); r = r[r.raw != "None"]
        r["mqm_r"] = [sum(e["score"] for e in json.loads(x)["errors"]) for x in r.raw]
        rr.append(r.drop(columns="raw"))
    rr = pd.concat(rr).groupby(["system", "seg_id"]).agg(n_raters=("mqm_r", "size"), mqm_r=("mqm_r", "mean")).reset_index()
    # the rater files repeat the merged rating under every rater id (WMT23 main set: one rater per item); n_raters := 1
    h = h.merge(rr, on=["system", "seg_id"], how="left")
    mg = read_score(f"{W}/human-scores/{lp}.mqm.merged.seg.rating"); mg = mg[mg.raw != "None"]
    mg["mqm_m"] = [sum(e["score"] for e in json.loads(x)["errors"]) for x in mg.raw]
    h = h.merge(mg[["system", "seg_id", "mqm_m"]], on=["system", "seg_id"], how="left")
    chk = np.abs(h.mqm_m + h.score); print(f"[{ours}] merged error-weight sum == -seg.score: {(chk < 1e-6).mean():.4f} (max |diff| {chk.max():.3f})")
    outs = {s: open(f"{W}/system-outputs/{lp}/{s}.txt", encoding="utf8").read().split("\n") for s in keep}
    src = open(f"{W}/sources/{lp}.txt", encoding="utf8").read().split("\n"); ref = open(f"{W}/references/{lp}.refA.txt", encoding="utf8").read().split("\n")
    docs = [l.split("\t") for l in open(f"{W}/documents/{lp}.docs", encoding="utf8").read().split("\n")]
    pool = pd.DataFrame({
        "seg_id": h.seg_id.values, "doc_id": [docs[i - 1][1] for i in h.seg_id], "domain": [docs[i - 1][0] for i in h.seg_id],
        "system": h.system.values, "source": [src[i - 1] for i in h.seg_id], "reference": [ref[i - 1] for i in h.seg_id],
        "ref_b": np.nan, "hyp": [outs[s][i - 1] for s, i in zip(h.system, h.seg_id)], "mqm": -h.score.values, "n_raters": 1})
    pool["u"] = utility(pool.mqm)
    pairs = list(zip(pool.hyp, pool.reference)); chunks = [pairs[i:i + 500] for i in range(0, len(pairs), 500)]
    with ProcessPoolExecutor(64) as ex:
        pool["chrf"] = [v for c in ex.map(_chrf_batch, chunks) for v in c]
    pool = pool.sort_values(["seg_id", "system"]).reset_index(drop=True)
    os.makedirs(f"{MT_ROOT}/{ours}", exist_ok=True); pool.to_parquet(f"{MT_ROOT}/{ours}/pool.parquet", index=False)
    g = pool.groupby(["seg_id", "hyp"]).system.transform("size")
    print(f"[{ours}] wrote pool: {pool.seg_id.nunique()} segs x {pool.system.nunique()} systems = {len(pool)} rows; rows sharing a string with another system: {(g > 1).mean():.3f}; mean MQM {pool.mqm.mean():.2f}")
    print(pool.groupby("system").u.mean().sort_values(ascending=False).round(4).to_string())
    return pool


if __name__ == "__main__":
    for ours, lp in LPS23.items():
        build(ours, lp)
