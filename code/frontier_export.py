"""Export the exact judge inputs for frontier-model judges (lock v1.0).

Same prompts and same truncation as the open judges (Arena responses truncated with the Qwen3-8B tokenizer, so every
judge sees identical text). Output: 06_naacl/frontier/inputs/{mt_ende,mt_zhen,arena_v09}.jsonl, one request per line:
  {"id": ..., "task": "mt"|"arena", "user": <user message>, "assistant_prefix": "Score: " (mt only)}
MT: the 6 best WMT submissions per language pair (MBR systems excluded) = the menus of every locked MT analysis.
Arena: lock v0.9 battles, both orders (id = <battle_id>|1 shows x as A, <battle_id>|2 shows y as A).
Run with the vLLM venv (needs transformers): /root/venv_vllm/bin/python -I frontier_export.py
"""
import json, os, sys
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from transformers import AutoTokenizer
import arena_prompt, mt_prompt

OUT = os.path.join(HERE, "..", "frontier", "inputs"); os.makedirs(OUT, exist_ok=True)
MBR = ("bleu_bestmbr", "bleurt_bestmbr", "comet_bestmbr", "chrf_bestmbr")
for lp in ("ende", "zhen"):
    d = pd.read_parquet(f"/root/naacl_data/mt/{lp}/pool.parquet")
    d = d[~d.system.isin(MBR)]
    top6 = d.groupby("system").u.mean().sort_values(ascending=False).index[:6]
    d = d[d.system.isin(top6)].drop_duplicates(["seg_id", "system"])
    with open(os.path.join(OUT, f"mt_{lp}.jsonl"), "w") as f:
        for r in d.itertuples():
            f.write(json.dumps(dict(id=f"{r.seg_id}|{r.system}", task="mt", user=mt_prompt.build_user_message(lp, r.source, r.hyp),
                                    assistant_prefix="Score: "), ensure_ascii=False) + "\n")
    print(lp, len(d), "requests; systems", list(top6))
tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B", revision="b968826d9c46dd6066d109eabc6255188de91218")
p = pd.read_parquet("/root/naacl_data/arena/pool_v09.parquet")
n = 0
with open(os.path.join(OUT, "arena_v09.jsonl"), "w") as f:
    for r in p.itertuples():
        for order, (a, b) in ((1, (r.resp_x, r.resp_y)), (2, (r.resp_y, r.resp_x))):
            f.write(json.dumps(dict(id=f"{r.battle_id}|{order}", task="arena", user=arena_prompt.build_user_message(tok, r.prompt, a, b)),
                               ensure_ascii=False) + "\n"); n += 1
print("arena_v09", n, "requests")
