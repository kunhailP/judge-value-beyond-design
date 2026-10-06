#!/usr/bin/env python3
"""Run a frontier judge over the exported inputs (lock v1.0). Resumable: ids already in the output file are skipped.

  python3 run_frontier.py --provider openai    --model gpt-4o-2024-08-06            --task mt_ende
  python3 run_frontier.py --provider anthropic --model claude-sonnet-4-5            --task arena_v09
  python3 run_frontier.py --provider openai    --model <id> --base_url <OpenAI-compatible endpoint> --task mt_zhen
Keys: OPENAI_API_KEY / ANTHROPIC_API_KEY (or --api_key_env). temperature 0, max_tokens 8.
Output: 06_naacl/frontier/outputs/<task>__<judge_name>.jsonl, one line per request:
  {"id", "text", "top": [[token, logprob], ...] (first generated token, OpenAI only), "error"}
Scoring is done afterwards by frontier_to_parquet.py (the rule is fixed in lock v1.0), never here.
"""
import argparse, asyncio, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "..", "frontier", "inputs"); OUTD = os.path.join(HERE, "..", "frontier", "outputs")


async def call_openai(client, model, req, logprobs):
    msgs = [{"role": "user", "content": req["user"]}]
    kw = dict(model=model, messages=msgs, temperature=0, max_tokens=8)
    if logprobs:
        kw.update(logprobs=True, top_logprobs=20)
    r = await client.chat.completions.create(**kw)
    ch = r.choices[0]
    top = []
    if logprobs and ch.logprobs and ch.logprobs.content:
        top = [[t.token, t.logprob] for t in ch.logprobs.content[0].top_logprobs]
    return ch.message.content or "", top


async def call_anthropic(client, model, req):
    msgs = [{"role": "user", "content": req["user"]}]
    if req.get("assistant_prefix"):
        msgs.append({"role": "assistant", "content": req["assistant_prefix"].rstrip()})
    r = await client.messages.create(model=model, messages=msgs, temperature=0, max_tokens=8)
    return "".join(b.text for b in r.content if getattr(b, "type", "") == "text"), []


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["openai", "anthropic"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--name", default=None, help="judge name used in file names (default: model id)")
    ap.add_argument("--task", choices=["mt_ende", "mt_zhen", "arena_v09"], required=True)
    ap.add_argument("--base_url", default=None)
    ap.add_argument("--api_key_env", default=None)
    ap.add_argument("--no_logprobs", action="store_true", help="for OpenAI-compatible endpoints without logprobs")
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None, help="smoke test on the first N requests")
    a = ap.parse_args()
    name = (a.name or a.model).replace("/", "_")
    os.makedirs(OUTD, exist_ok=True)
    out = os.path.join(OUTD, f"{a.task}__{name}.jsonl")
    reqs = [json.loads(l) for l in open(os.path.join(IN, f"{a.task}.jsonl"))]
    if a.limit:
        reqs = reqs[:a.limit]
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["id"] for l in open(out) if '"error": null' in l}
    todo = [r for r in reqs if r["id"] not in done]
    print(f"{len(reqs)} requests, {len(done)} done, {len(todo)} to run -> {out}")
    if a.provider == "openai":
        from openai import AsyncOpenAI
        client = AsyncOpenAI(base_url=a.base_url, api_key=os.environ.get(a.api_key_env or "OPENAI_API_KEY"))
    else:
        from anthropic import AsyncAnthropic
        client = AsyncAnthropic(api_key=os.environ.get(a.api_key_env or "ANTHROPIC_API_KEY"))
    sem = asyncio.Semaphore(a.concurrency); lock = asyncio.Lock(); n = [0]
    f = open(out, "a")

    async def one(req):
        async with sem:
            for attempt in range(6):
                try:
                    if a.provider == "openai":
                        text, top = await call_openai(client, a.model, req, not a.no_logprobs)
                    else:
                        text, top = await call_anthropic(client, a.model, req)
                    rec = dict(id=req["id"], text=text, top=top, error=None); break
                except Exception as e:                      # rate limits / transient errors: back off and retry
                    rec = dict(id=req["id"], text="", top=[], error=repr(e)[:300])
                    await asyncio.sleep(min(60, 2 ** attempt + random.random()))
            async with lock:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n"); f.flush(); n[0] += 1
                if n[0] % 500 == 0:
                    print(n[0], "written", flush=True)

    await asyncio.gather(*(one(r) for r in todo))
    f.close()
    errs = sum(1 for l in open(out) if '"error": null' not in l)
    print("finished; lines with errors (rerun the same command to retry them):", errs)


if __name__ == "__main__":
    asyncio.run(main())
