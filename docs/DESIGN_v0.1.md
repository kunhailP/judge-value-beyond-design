# NAACL 2027 (ARR October 2026, deadline 2026-10-12) — design v0.1

Target: ARR Soundness 4 / Excitement 4. A new 8-page paper built from the TMLR artefact (desk-rejected for novelty), not a
shortened version of it.

## 1. Thesis

> LLM judges are usually credited with the human labels they save over *uniform* annotation. Measured against the best
> annotation design that uses no judge, most of that saving belongs to the design, and what remains is specific to the
> decision being made.

Three claims, each tested in three domains (retrieval, machine translation, open-ended chat):

| | Claim | Retrieval (existing + 1 arm) | MT (WMT MQM, new) | Chat (LMArena 55k, new) |
|---|---|---|---|---|
| C1 | Decision-aware human allocation saves more than the judge adds on top of it | 40–56% vs 3–20% (Table 2) | skip identical outputs, share labels across comparisons, weight by output dissimilarity | — (no structural lever; stated) |
| C2 | Judge value measured over uniform sampling is inflated relative to its value over the best human design | needs `uniform_cvl` arm (pools bundle) | uniform+CV vs weighted+CV | — |
| C3 | Judge value is decision-conditional: it varies across system pairs, and label accuracy does not predict it | query-level per-pair gains (existing) | per-pair HES, 5 judges | per-pair HES, 4 judges |
| C4 | A small pilot predicts the relative cost of designs but not near-threshold judge adoption | cost law r = 0.95; NeuCLIR lock | prospective lock (this doc §6) | prospective lock |

Positioning (must be explicit in the paper): PPI/PPI++ (Angelopoulos et al.), active inference (Zrnic & Candès),
Chen et al. ICML 2026 (efficient noisy-judge inference), Boyeau et al. (AutoEval, Arena), Chatzi et al. (PPR, Arena),
Gao et al. 2608.26638 (PPSR: annotation saved by metrics, MT) and Dorner et al. ICLR 2025 (≤2× bound). We propose no
estimator. PPSR and AutoEval measure savings over a fixed (uniform) design; C1/C2 say that baseline is the wrong one.

## 2. Metric

For decision d (a menu of systems and a tolerance ε), design s and judge f:
`J_τ(s, f; d)` = unique human labels, pilot included, at which a pre-committed budget certifies with probability τ
(τ = 0.5 primary; 0.8 reported where reachable; certification-curve AUC as a τ-free check).

* **HES over base design s**: `HES_s(f; d) = 1 − J_τ(s, f; d) / J_τ(s, ∅; d)`.
* **Judge-value inflation**: `HES_uniform(f) − HES_best(f)` with `best` the cheapest judge-free design.
* **Selection regret**: `(J_τ(selected) − J_τ(oracle)) / J_τ(best, ∅)`.

## 3. Inference

Pilot-fixed λ everywhere (already so in the document-level IR code, `81_sampling_baselines.py: lam_pair`): λ ∈ [0, 1] in the IR code; **in the MT/Arena code (`110_unit_audit.py`) λ = max(0, Cov/Var) without an upper clip, because judge scores are on their own scale (correction added after v0.1)**
estimated on the fully labelled pilot, frozen, control variate `λ·ĵ` on the post-pilot sample. Estimand: mean over the
finite population of the domain (pilot part known exactly, rest a without-replacement sample). Candidate chosen on the
pilot; certificate = one-sided t bounds for every competitor, Bonferroni over the menu; α = 0.10. Validity reported as
the observed wrong-certificate rate and boundary stress (runner-up forced as candidate, ε = 0.9 × true regret).
The query-level cross-fitted analyses of the TMLR paper are kept only as the C3 retrieval evidence, labelled as such.

## 4. Domains

### 4.1 Retrieval (existing)
ANTIQUE, CAsT 2019, DBpedia-Entity, DL 21–23 (+ TREC-COVID, Touché, NeuCLIRBench held-out). Judges Qwen3-8B, Qwen3-Reranker,
inverted. New arm `uniform_cvl` (uniform sampling + pilot-λ judge CV) for C2 — requires the pools bundle (not on this
machine). Without it C2 is tested in MT only.

### 4.2 Machine translation (WMT MQM)
* Data: Google WMT MQM human evaluation (Freitag et al.), WMT22 en→de and zh→en (fallback WMT23/WMT21 if WMT22 incomplete).
  Unit = one (segment, system) output; human label = its MQM score (Google weights: minor 1, major 5, non-translation 25,
  minor punctuation 0.1); utility `u = −min(MQM, 25)/25`.
* Menu: the 4 systems with the best human mean MQM (closest decisions); also every pair of the top 6 for C3.
* Cost: unique (segment, system) ratings, pilot included. An output string identical to one already rated for the same
  segment is not re-rated (the rating is copied) — the MT analogue of a zero-weight document.
* Human-only designs: `uniform` (sample segments uniformly, rate every menu output); `dedup` (same, identical outputs
  rated once); `weighted` (segments sampled ∝ pilot-fitted sd of the paired difference as a function of a label-free
  output dissimilarity, chrF distance between outputs; identical outputs weight 0; dedup).
* Judge designs: `uniform_cvl`, `weighted_cvl` (pilot-λ CV), `active_cvl` (π ∝ dissimilarity weight × pilot residual sd).
* Judges (5): Qwen3-8B and Mistral-7B-Instruct-v0.3 (GEMBA-DA 0–100 prompt, expected score), COMET-22
  (`Unbabel/wmt22-comet-da`, reference-based), chrF vs reference (label-free), inverted COMET (adversarial).
* Pilot: 100 segments (primary), 50 (ablation). ε grid {0.005, 0.01, 0.02}; the primary ε of each language pair is fixed by
  rule: the smallest ε at which `weighted` reaches J50 within the largest budget.

### 4.3 Open-ended chat (LMArena)
* Data: `lmarena-ai/arena-human-preference-55k`, English single-turn; the 6 model pairs with ≥ 300 decisive battles,
  ties kept as 0.5. Unit = battle; human label = vote; estimand = win rate of the pilot-preferred model minus 0.5.
* Decision: the pilot-preferred model is within ε of the other, ε ∈ {0.02, 0.05}.
* Judges (4): Qwen3-8B, Mistral-7B (pairwise prompt, both orders averaged, P(A better) from the token distribution),
  "longer response wins" (label-free), inverted Qwen.
* Designs: `uniform`, `uniform_cvl`, `active_cvl` (π ∝ pilot residual sd by judge-confidence bin). No structural
  human-only lever exists here; C1 is not claimed for chat.

## 5. Experiments → figures

| Fig/Tab | Content | Status |
|---|---|---|
| Fig 1 | Waterfall per domain: uniform → best human design → + best judge | IR done; MT new |
| Fig 2 | HES over uniform vs HES over best design (inflation), per judge × cell | MT new; IR needs bundle |
| Fig 3 | Judge × decision HES heatmap (MT pairs, Arena pairs) + accuracy vs HES scatter | new |
| Tab 1 | Judge selection: accuracy / ρ / pilot-HES / global-best / human-only / oracle — regret, harm rate | IR done (trivial: Qwen everywhere), MT + Arena new |
| Fig 4 | Pilot-predicted vs realised cost ratios, all domains, locked cells marked | IR done; MT + Arena new |
| Tab 2 | Validity: wrong-certificate and boundary type-I per domain | IR done; new |

## 6. Pre-registration for MT and Arena (to be frozen as `PROSPECTIVE_LOCK_v0.8` before judge outputs are joined with human labels)

* H1 (MT): in ≥ 3 of 4 (language pair × {primary ε, ε/2}) cells, `1 − J50(best human)/J50(uniform)` exceeds
  `HES_best(best judge)`.
* H2 (MT): in ≥ 3 of 4 cells, `HES_uniform − HES_best` ≥ 0.05 for the judge with the largest HES_uniform.
* H3 (MT + Arena): over judge × pair cells, Spearman(HES, pilot ρ) > Spearman(HES, pilot accuracy); and the oracle judge
  differs between at least two pairs of the same domain.
* H4: correlation between pilot-predicted and realised post-pilot cost ratios ≥ 0.80 in each new domain.
* H5: mean selection regret of the pilot-HES selector ≤ that of the accuracy selector, each domain.
* Validity: Clopper–Pearson upper limit of the wrong-certificate rate ≤ 0.15 in every cell.
All five are reported whatever the outcome; failures go in the main text.

## 7. Schedule (6 days)

| Day | Work |
|---|---|
| 10-06/07 | design + lock text; vLLM env; Arena pool + judges; MT data + judges; IR re-analysis from draw records |
| 10-08 | lock v0.8 committed; MT and Arena audit grids (CPU) |
| 10-09 | analysis, figures; `uniform_cvl` IR arm if the bundle arrives |
| 10-10/11 | paper (8 pp), appendix, limitations, ethics, ARR checklist |
| 10-12 | submit |
