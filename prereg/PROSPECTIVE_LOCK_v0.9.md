# PROSPECTIVE LOCK v0.9 — Arena: close model pairs (replaces the uninformative v0.8 Arena decision)

## Why
Under v0.8 the six Arena pairs had win-rate gaps of 0.10–0.56, far above ε ∈ {0.02, 0.05}: every design certified right
after the pilot and no judge could save anything (HES 0–4%). The v0.8 Arena result is reported as run, labelled
uninformative for C1–C4. v0.9 defines a decision that a human budget does not settle at once.

## What had been seen
v0.8 Arena results, including pilot ρ and pairwise accuracy of every judge on the v0.8 pairs (Qwen3-8B ρ 0.12–0.35,
Mistral-7B 0.06–0.34, "longer" 0.08–0.21) and the position bias of the Qwen3-8B judge (order-1/order-2 Spearman 0.62).
The judges, prompt and scoring are those of v0.8 and are not changed. **No judge output exists for any v0.9 battle when
this lock is committed.**

## Fixed elements
* Pool: `code/arena_pool_v09.py` → `$JV_DATA/arena/pool_v09.parquet`: English single-turn battles of
  lmarena-ai/arena-human-preference-55k; pairs with ≥ 300 battles (ties kept) not used in v0.8; the 6 with the smallest
  |win-rate gap| (selected on human votes only): pair ids 10–15 =
  gpt-4-0314/gpt-4-0613 (472, gap .011), llama-2-70b-chat/vicuna-33b (377, .021), gpt-3.5-turbo-0613/vicuna-33b (375, .048),
  claude-instant-1/gpt-3.5-turbo-1106 (395, .071), mistral-medium/mixtral-8x7b-instruct-v0.1 (312, .080),
  gpt-3.5-turbo-0613/gpt-4-0613 (311, .084).
* Judges, prompt, both-order averaging: identical to v0.8 (`arena_judge.py`, `arena_prompt.py`), outputs `judge_*_v09.parquet`.
* Audit: `110_unit_audit.py` at this commit, pilot 50 (primary) and 25, ε ∈ {0.02, 0.05, 0.1} (primary: 0.05 and 0.1),
  300 draws, seed 20261007; boundary stress on pair 10. Cost: one vote per battle.
* Hypotheses: H3, H4, H5 and validity of v0.8 apply unchanged to the v0.9 pairs (Arena has no structural human design, so
  H1/H2 are not tested here). Additionally **H6**: in ≥ 3 of the 6 pairs at ε = 0.05, the best non-adversarial judge has
  HES ≥ 0.05 with a bootstrap interval excluding 0.
