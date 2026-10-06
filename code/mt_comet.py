"""COMET-22 (Unbabel/wmt22-comet-da, reference-based) on every row of the MT pools. Usage: mt_comet.py ende zhen"""
import sys, time, json
import pandas as pd, numpy as np
from comet import load_from_checkpoint
from huggingface_hub import snapshot_download
REV = "2760a223ac957f30acfb18c8aa649b01cf1d75f2"
path = snapshot_download("Unbabel/wmt22-comet-da", revision=REV)
model = load_from_checkpoint(path + "/checkpoints/model.ckpt")
for lp in sys.argv[1:]:
    d = pd.read_parquet(f"/root/naacl_data/mt/{lp}/pool.parquet", columns=["seg_id", "system", "source", "hyp", "reference"])
    data = [dict(src=s, mt=h, ref=r) for s, h, r in zip(d.source, d.hyp, d.reference)]
    t = time.time()
    out = model.predict(data, batch_size=64, gpus=1, progress_bar=False)
    dt = time.time() - t
    res = pd.DataFrame(dict(seg_id=d.seg_id.values, system=d.system.values, score=np.asarray(out.scores, dtype=float)))
    res.to_parquet(f"/root/naacl_data/mt/{lp}/judge_comet22.parquet", index=False)
    meta = dict(judge="comet22", lp=lp, repo="Unbabel/wmt22-comet-da", revision=REV, n=len(res), seconds=round(dt, 1),
                nan=float(res.score.isna().mean()),
                q=dict(zip(["0", ".05", ".25", ".5", ".75", ".95", "1"], np.nanquantile(res.score, [0, .05, .25, .5, .75, .95, 1]).round(4).tolist())))
    print(json.dumps(meta)); json.dump(meta, open(f"/root/naacl_data/mt/{lp}/judge_comet22_meta.json", "w"), indent=1)
