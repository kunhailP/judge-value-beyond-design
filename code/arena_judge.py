"""Run a pairwise vLLM judge on the arena pool, both orders. Usage: arena_judge.py {qwen3_8b|mistral_7b} [n_limit]"""
import sys, time, math, json
sys.path.insert(0, "/root/judge-audit-certification/06_naacl/code")
import numpy as np, pandas as pd
from arena_prompt import build_user_message
from vllm import LLM, SamplingParams

MODELS = {
    "qwen3_8b": ("Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218", {"enable_thinking": False}),
    "mistral_7b": ("mistralai/Mistral-7B-Instruct-v0.3", "c170c708c41dac9275d15a8fff4eca08d52bab71", {}),
}
name = sys.argv[1]; limit = int(sys.argv[2]) if len(sys.argv) > 2 else None
repo, rev, tmpl_kw = MODELS[name]
pool = pd.read_parquet("/root/naacl_data/arena/pool.parquet")
if limit: pool = pool.head(limit)

t0 = time.time()
llm = LLM(model=repo, revision=rev, tokenizer_revision=rev, dtype="bfloat16", max_model_len=4096,
          gpu_memory_utilization=0.9, seed=0, enable_prefix_caching=True)
tok = llm.get_tokenizer()
t_load = time.time() - t0

def chat(u):
    return tok.apply_chat_template([{"role": "user", "content": u}], tokenize=False, add_generation_prompt=True, **tmpl_kw)

prompts = []
for r in pool.itertuples():
    prompts.append(chat(build_user_message(tok, r.prompt, r.resp_x, r.resp_y)))  # order1: x = A
    prompts.append(chat(build_user_message(tok, r.prompt, r.resp_y, r.resp_x)))  # order2: y = A
lens = [len(tok.encode(p, add_special_tokens=False)) for p in prompts]
print(f"prompt tokens: max {max(lens)}, p50 {int(np.median(lens))}, >4095: {sum(l > 4095 for l in lens)}", flush=True)

sp = SamplingParams(temperature=0.0, max_tokens=1, logprobs=20, seed=0)
t1 = time.time()
outs = llm.generate(prompts, sp)
t_gen = time.time() - t1

def pa(o):
    """Return (P(A) renormalised over {A,B}, top token text)."""
    lp = o.outputs[0].logprobs[0]
    pA = pB = 0.0
    for tid, L in lp.items():
        s = (L.decoded_token or "").replace("▁", " ").strip()
        if s == "A": pA += math.exp(L.logprob)
        elif s == "B": pB += math.exp(L.logprob)
    top = o.outputs[0].text
    return (pA / (pA + pB) if pA + pB > 0 else float("nan")), top, pA + pB

res = [pa(o) for o in outs]
p1 = np.array([res[2 * i][0] for i in range(len(pool))])          # P(A | x first) = P(x)
p2 = np.array([1 - res[2 * i + 1][0] for i in range(len(pool))])  # P(B | y first) = P(x)
mass = np.array([r[2] for r in res])
tops = pd.Series([r[1] for r in res]).value_counts().head(8).to_dict()
out = pd.DataFrame(dict(battle_id=pool.battle_id.values, p_x_order1=p1, p_x_order2=p2, p_x=(p1 + p2) / 2))
out.to_parquet(f"/root/naacl_data/arena/judge_{name}.parquet" if not limit else f"/root/naacl_data/arena/judge_{name}_test.parquet", index=False)

import vllm
meta = dict(judge=name, repo=repo, revision=rev, vllm=vllm.__version__, n_battles=len(pool), n_prompts=len(prompts),
            load_s=round(t_load, 1), gen_s=round(t_gen, 1),
            nan_order1=float(np.isnan(p1).mean()), nan_order2=float(np.isnan(p2).mean()), nan_px=float(out.p_x.isna().mean()),
            AB_mass_quantiles=np.nanquantile(mass, [0, .01, .5]).round(4).tolist(), top_first_tokens=tops,
            p_x_quantiles=dict(zip(["0", ".05", ".25", ".5", ".75", ".95", "1"], np.nanquantile(out.p_x, [0, .05, .25, .5, .75, .95, 1]).round(4).tolist())),
            mean_P_first=float(np.nanmean(np.r_[p1, 1 - p2])),  # P(choose A) averaged across both orders
            mean_P_first_order1=float(np.nanmean(p1)), mean_P_first_order2=float(np.nanmean(1 - p2)),
            frac_order_flip=float(np.nanmean((p1 > .5) != (p2 > .5))),
            spearman_order1_order2=float(pd.Series(p1).corr(pd.Series(p2), method="spearman")))
print(json.dumps(meta, indent=1))
if not limit:
    json.dump(meta, open(f"/root/naacl_data/arena/judge_{name}_meta.json", "w"), indent=1)
