# PROSPECTIVE LOCK v1.0 — frontier-model judges (MT and Arena v0.9)

Committed before any frontier-model judgment has been requested.

## Why
Under v0.8/v0.9 the open judges (Qwen3-8B, Mistral-7B, COMET-22) saved nothing distinguishable from zero on top of the
best human design in MT (HES −8% to +5%), and their saving over uniform sampling was also near zero, so H2 (inflation)
could not be observed. A judge that does save labels over uniform sampling is needed to test H2, and frontier judges
answer the objection that only weak judges were tried.

## What had been seen
All v0.8 MT results (open judges), v0.8 Arena results, and part of the v0.9 Arena results (open judges).

## Fixed elements
* Inputs: `frontier/inputs/{mt_ende,mt_zhen,arena_v09}.jsonl` produced by `frontier_export.py` at this commit
  (identical prompts and truncation to the open judges; MT: top-6 WMT submissions per language pair; Arena: both orders).
* Requests: `run_frontier.py`, temperature 0, max 8 tokens; OpenAI-style endpoints with top-20 logprobs where available.
* Scoring: `frontier_to_parquet.py` (expected value over first-token alternatives when logprobs carry ≥ 0.5 mass,
  otherwise the parsed text). Judges: the frontier models the authors run (names recorded in the output file names);
  each is analysed under the same code, menus, pilots, ε grids and seeds as lock v0.8 (MT) and v0.9 (Arena).
* All hypotheses of v0.8 (H1–H5, validity) and v0.9 (H6) apply with the frontier judges added to the judge set.
* **H2′ (MT, primary test of inflation)**: for the frontier judge with the largest HES over uniform sampling,
  in ≥ 3 of the 4 primary MT cells (2 language pairs × ε ∈ {0.01, 0.02}, pilot 50):
  (a) HES_uniform ≥ 0.05, and (b) inflation = HES_uniform − HES_best ≥ 0.03.
* **H7**: in each domain, the best frontier judge's HES over the best human design is smaller than the best human
  design's saving over uniform sampling (the design dominates even with a frontier judge).
Requests that fail after retries are reported; cells are analysed only if ≥ 99% of requests succeeded.
