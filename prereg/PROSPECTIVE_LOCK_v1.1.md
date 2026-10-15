# PROSPECTIVE LOCK v1.1 — all WMT22 submitted metrics as judges (MT block)

Committed before any HES, J50 or certification outcome of these metrics has been computed.

## Why
Gao et al. (arXiv 2608.26638, "PPSR") measure, on the same WMT22 en-de and zh-en MQM data, how much human annotation each
submitted metric saves under prediction-powered evaluation: uniform random labelling, λ estimated on the same labels,
savings = labels to 80% power, PPSR ≈ mean squared correlation of paired differences (top metrics ≈ 0.09–0.15).
Under v0.8 our open judges saved nothing distinguishable from zero. v1.1 asks whether the strongest metrics of WMT22
save labels for a close-system certification once (i) a judge-free decision-aware design is credited and (ii) λ is fitted
on a fixed pilot (valid inference, at an estimation cost).

## What had been seen
Everything in LOCK_HISTORY.md up to this commit, including the exploratory cost law, estimation tax and ρ-dial results.
The published WMT22 metric meta-evaluation (system- and segment-level correlations) and the PPSR paper (values above).
For the imported metric files only their value ranges were inspected (all higher-is-better); none was joined with MQM.

## Fixed elements
* Judges: the 31 WMT22 metrics of `code/mtme_import.py` (refA reference-based and -src QE variants) from
  mt-metrics-eval-v2 (data.statmt.org/wmt26), segment line i ↔ seg_id i+1 (verified by string match, 100%).
* Audit: `110_unit_audit.py` at this commit, MT top-4 menus (as v0.8), pilot 50, ε ∈ {0.01, 0.02}, 300 draws, seed 20261007,
  `--oracle` (population-λ diagnostic arms); summaries by `111_summarize.py`.
* Population quantities per metric: ρ̄ = mean over the menu's 6 pairs of the correlation of paired differences over all
  segments (the PPSR-style quantity; ρ̄² is its asymptotic saving), and system-level Pearson over the 11 WMT submissions.

## Hypotheses (primary cells: 2 language pairs × ε ∈ {0.01, 0.02}; J50; "best human" as in v0.8)
* **H8 (design vs the best metric)**: in ≥ 3 of 4 cells, the saving of the best human design over uniform sampling is at
  least the HES of the best metric (largest realised HES over the best human design).
* **H9 (estimation tax)**: in each language pair, the mean over metrics of HES(oracle λ) − HES(pilot λ) on the weighted
  design is > 0, with a 95% bootstrap interval over metrics excluding 0.
* **H10 (correlation overstates realised saving)**: for the 5 metrics with the largest ρ̄², the realised HES over uniform
  sampling (pilot λ) is below ρ̄² in every primary cell.
* **H11 (level of measurement)**: across metrics, Spearman(realised HES over the best human design, ρ̄) >
  Spearman(realised HES over the best human design, system-level Pearson), in each language pair (pooled over ε).
* Validity as v0.8.
All outcomes are reported.
