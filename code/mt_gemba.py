"""GEMBA-DA expected-score judge via vLLM. Usage: mt_gemba.py {qwen3_8b|mistral_7b} [limit]  (runs ende and zhen)

Scoring (exact definition):
  base = chat template(user = GEMBA prompt) + generation prompt (Qwen3: enable_thinking=False, i.e. empty <think></think>),
         + assistant prefix tokens encode("Score:") + [single whitespace token], so the next token is the first digit
         (same rule for both models; without it Qwen3 starts with "**Score: " and Mistral with a bare whitespace token).
  Step 1: top-20 next-token probs at base; P1[d] for single-digit tokens d=0..9; D1 = sum.  q1 = P1/D1.
  Step 2: for each d in 1..9 with q1[d] >= 1e-3: top-20 at base+[d]; P2[e] for digits e, stop = 1 - sum_e P2[e]
          (any non-digit = end of number). V[d] = stop*d + sum_e P2[e]*(10d+e), except for d=1,e=0 where
  Step 3: (if q1[1]*P2[1][0] >= 1e-4) top-20 at base+[1,0]: value(10..) = P3[0]*100 + (1-P3[0])*10.
  V[0] = 0. Score = sum_{d in kept} q1[d] V[d] / sum_{d in kept} q1[d]  (kept = d=0 plus expanded digits).
  Decimals ("85.5") are treated as stop (-> 85). Digits outside the top-20 count as probability 0.
  Fallback: if D1 < 0.01, greedy decode (max 8 tokens) and parse the first integer (clipped 0-100); flagged in the diag file.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import DATA
import sys, time, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from mt_prompt import build_user_message
from vllm import LLM, SamplingParams

MODELS = {
    "qwen3_8b": ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218", {"enable_thinking": False}),
    "mistral_7b": ("mistralai/Mistral-7B-Instruct-v0.3", "c170c708c41dac9275d15a8fff4eca08d52bab71", {}),
}
name = sys.argv[1]; limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
repo, rev, tmpl_kw = MODELS[name]
t0 = time.time()
llm = LLM(model=repo, revision=rev, tokenizer_revision=rev, dtype="bfloat16", max_model_len=4096,
          gpu_memory_utilization=0.9, seed=0, enable_prefix_caching=True)
tok = llm.get_tokenizer()
load_s = time.time() - t0
DIG = [tok.convert_tokens_to_ids(str(d)) for d in range(10)]
assert len(set(DIG)) == 10 and all(tok.decode([i]) == str(d) for d, i in enumerate(DIG)), DIG
WS = tok.encode(" ", add_special_tokens=False)
WS = [t for t in WS if tok.decode([t]).strip() == ""][-1:]  # single whitespace token id
SP1 = SamplingParams(temperature=0.0, max_tokens=1, logprobs=20, seed=0)

def topk(ids_list):
    outs = llm.generate([{"prompt_token_ids": ids} for ids in ids_list], SP1, use_tqdm=False)
    return [{tid: math.exp(L.logprob) for tid, L in o.outputs[0].logprobs[0].items()} for o in outs]

def digits(p):
    return np.array([p.get(i, 0.0) for i in DIG])

PREFIX = tok.encode("Score:", add_special_tokens=False) + WS
print("assistant prefix tokens:", [tok.decode([t]) for t in PREFIX], flush=True)

def bases(lp, d):
    msgs = [build_user_message(lp, s, h) for s, h in zip(d.source, d.hyp)]
    return [list(tok.apply_chat_template([{"role": "user", "content": m}], tokenize=True, add_generation_prompt=True, **tmpl_kw)) + PREFIX for m in msgs]

pools = {lp: pd.read_parquet(f"{DATA}/mt/{lp}/pool.parquet", columns=["seg_id", "system", "source", "hyp"]) for lp in ("ende", "zhen")}
if limit: pools = {k: v.head(limit) for k, v in pools.items()}

meta_all = dict(judge=name, repo=repo, revision=rev, load_s=round(load_s, 1), assistant_prefix="Score: ")
for lp, d in pools.items():
    t = time.time()
    B = bases(lp, d)
    P1 = [digits(p) for p in topk(B)]
    # step 2
    req2 = [(i, k) for i, p in enumerate(P1) if p.sum() >= 0.01 for k in range(1, 10) if p[k] / p.sum() >= 1e-3]
    P2 = dict(zip(req2, (digits(p) for p in topk([B[i] + [DIG[k]] for i, k in req2]))))
    req3 = [i for (i, k) in req2 if k == 1 and (P1[i][1] / P1[i].sum()) * P2[(i, 1)][0] >= 1e-4]
    P3 = dict(zip(req3, (digits(p)[0] for p in topk([B[i] + [DIG[1], DIG[0]] for i in req3]))))
    scores, method, mass = [], [], []
    for i, p in enumerate(P1):
        D1 = p.sum(); mass.append(D1)
        if D1 < 0.01:
            scores.append(np.nan); method.append("greedy"); continue
        q = p / D1; num = 0.0; den = q[0]
        for k in range(1, 10):
            if (i, k) not in P2: continue
            p2 = P2[(i, k)]; stop = max(0.0, 1 - p2.sum())
            v = stop * k + sum(p2[e] * (10 * k + e) for e in range(10))
            if k == 1:
                p30 = P3.get(i, 0.0)
                v += p2[0] * (p30 * 100 + (1 - p30) * 10) - p2[0] * 10
            num += q[k] * v; den += q[k]
        scores.append(num / den); method.append("expected")
    gi = [i for i, m in enumerate(method) if m == "greedy"]
    if gi:
        go = llm.generate([{"prompt_token_ids": B[i]} for i in gi], SamplingParams(temperature=0.0, max_tokens=8, seed=0), use_tqdm=False)
        for i, o in zip(gi, go):
            m = re.search(r"\d+", o.outputs[0].text)
            scores[i] = float(min(100, max(0, int(m.group())))) if m else np.nan
    dt = time.time() - t
    sc = np.array(scores, dtype=float)
    res = pd.DataFrame(dict(seg_id=d.seg_id.values, system=d.system.values, score=sc))
    sfx = "" if not limit else "_test"
    res.to_parquet(f"{DATA}/mt/{lp}/judge_{name}{sfx}.parquet", index=False)
    pd.DataFrame(dict(seg_id=d.seg_id.values, system=d.system.values, digit_mass_step1=mass, method=method)).to_parquet(
        f"{DATA}/mt/{lp}/judge_{name}_diag{sfx}.parquet", index=False)
    m = dict(n=len(res), seconds=round(dt, 1), n_step2=len(req2), n_step3=len(req3), nan=float(np.isnan(sc).mean()),
             n_greedy=len(gi), digit_mass_q=np.quantile(mass, [0, .01, .5]).round(4).tolist(),
             n_distinct_scores=int(pd.Series(sc).round(3).nunique()),
             q=dict(zip(["0", ".05", ".25", ".5", ".75", ".95", "1"], np.nanquantile(sc, [0, .05, .25, .5, .75, .95, 1]).round(3).tolist())))
    meta_all[lp] = m
    print(lp, json.dumps(m), flush=True)
import vllm; meta_all["vllm"] = vllm.__version__
print(json.dumps(meta_all, indent=1))
if not limit:
    json.dump(meta_all, open(f"{DATA}/mt/judge_{name}_meta.json", "w"), indent=1)
