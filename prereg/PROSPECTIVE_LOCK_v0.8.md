# PROSPECTIVE LOCK v0.8 — MT (WMT22 MQM) and chat (LMArena 55k) blocks of the NAACL 2027 paper

Committed before any LLM or COMET judgment has been joined with a human label in either domain.

## What had been seen when this lock was written
* MT: the human MQM pools (system means, identical-output rates, paired-difference sd), and development audits of the
  human-only designs (`uniform`, `dedup`, `weighted`) and of the chrF judge at pilots 50 and 100 (outputs
  `06_naacl/results/mt/*_dev*`). chrF is therefore a development judge and is reported as such, not as a test.
  Seen: human designs save about 8–19% of J50 over uniform; chrF saves about 0.
* Arena: pool construction and per-pair battle counts only. No judge output has been compared with a vote.
* One bug was found and fixed during development: the weighted design gave weight 0 to outputs that differ only in
  characters chrF ignores; zero weight is now restricted to identical strings (wrong-certificate rate 0.147 → 0.007).

## Fixed elements
* Code: `06_naacl/code/110_unit_audit.py` and `111_summarize.py` at this commit. α = 0.10, normal bounds with Bonferroni
  over competitors, pilot-fixed λ ≥ 0, finite-population estimand, 300 draws, seed 20261007, budgets = the default grid.
* MT data: WMT22 generalMT MQM (google/wmt-mqm-human-evaluation @ 29acd69), en→de and zh→en, Google weights, u = −min(MQM,25)/25,
  identical strings of a segment share the mean rating. MBR systems excluded. Menu = top-4 WMT submissions by mean u
  (en→de: Online-W, Online-B, JDExploreAcademy, Online-A; zh→en: Lan-Bridge, Online-B, LanguageX, JDExploreAcademy).
  Pilot 50 segments (primary), 100 (ablation). ε ∈ {0.005, 0.01, 0.02}; **primary cells: ε ∈ {0.01, 0.02} × 2 language pairs**.
* MT judges (test): `comet22` (Unbabel/wmt22-comet-da, reference-based), `qwen3_8b` and `mistral_7b` (GEMBA-DA 0–100,
  expected score over the digit distribution, reference-free), `inv_comet22` (adversarial). Development: `chrf`.
* Arena data: lmarena-ai/arena-human-preference-55k, English single-turn, the 6 pairs with the most decisive battles, ties 0.5.
  Pilot 50 battles (primary), 25 (ablation). ε ∈ {0.02, 0.05}; **primary cells: 6 pairs × 2 ε**.
* Arena judges: `qwen3_8b`, `mistral_7b` (pairwise, both orders averaged), `longer` (label-free), `inv_qwen3_8b` (adversarial).
* C3 menus: every 2-system menu among the top-6 WMT submissions of each language pair (15 × 2) and the 6 Arena pairs.

## Hypotheses and criteria (J50 unless stated; "best human" = the cheapest of uniform/dedup/weighted in that cell)
* **H1 (MT)**: in ≥ 3 of the 4 primary cells, the saving of the best human design over uniform exceeds the HES of the best
  test judge over the best human design.
* **H2 (MT)**: in ≥ 3 of 4 primary cells, inflation = HES_uniform − HES_best ≥ 0.05 for the test judge with the largest HES_uniform.
* **H3 (MT, Arena separately)**: over the 2-system menus × non-adversarial test judges, Spearman(HES_best, pilot ρ) >
  Spearman(HES_best, pilot pairwise accuracy) (pilot quantities = draw medians); and the J50-best judge differs between at
  least two menus of the domain.
* **H4**: median over primary cells of corr(log pilot-predicted, log realised post-pilot cost ratio) ≥ 0.80, each domain.
* **H5**: mean selection regret of `sel_pilotcost` ≤ that of `sel_accuracy`, each domain.
* **Validity**: Clopper–Pearson 95% upper limit of the wrong-certificate rate ≤ 0.15 in every cell and design;
  boundary stress (runner-up candidate, ε = 0.9 × its regret) type-I ≤ 0.15.

Every hypothesis is reported with its outcome in the main text whether it holds or not. Any analysis not listed here is
labelled exploratory.
