# Prospective lock v1.2 — auditor strategies on a held-out year (WMT23 en→de, zh→en)

Written 2026-10-10 after the WMT22 development analysis below and before any WMT23 audit record was examined
(the WMT23 audits were running at the time of writing; `code/RUN_PAIRS_23.sh`).

## Question
After a judge-free annotation design is credited, does choosing or using an automatic evaluator help an auditor who must
decide *before* the audit, with rules fixed on another year's data?

## Held-out data
WMT23 MQM en→de (460 segments rated for all 11 non-reference systems; paragraph-level segments) and zh→en (1,177 × 14),
official mt-metrics-eval MQM scores (= Google's merged ratings, verified: 100% / 98.5% equal to the sum of error weights;
single rater per item). References and the BLEU-MBR system excluded, as `*_bestmbr` in WMT22. `code/mt_build_pool23.py`.
Evaluators: every WMT23 submitted metric with a refA or src variant (42 per language pair; synthetic-reference variants and
the random baseline excluded), `code/mtme_import23.py`. Decisions: the 15 two-system menus among the top-6 systems by
MQM per language pair, pilot 50, ε ∈ {0.01, 0.02}, 300 audits per cell, the same arms as `RUN_PAIRS_MTME.sh`
(`--extra --oracle`). Informative cell: 1 − P/J50(uniform) ≥ 0.3, as in the paper.

## Strategies (per audit, pilot information only; `code/128_strategies.py`)
* S1 design: dedup. Fixed on WMT22: over the 33 informative development cells dedup is cheaper than weighted in 83% (zh→en)
  and 75% (en→de) of cells and in total labels (10,685 vs 11,205), `ana/wmt22_design_J50.csv`.
* S2 fixed evaluator: COMET-22 (WMT23 name `COMET-refA`), the WMT22 evaluator with the highest decision-level ρ among those
  submitted under the same name in both years (MetricX-22 has no WMT23 counterpart).
* S3 pilot selection: the evaluator with the highest pilot ρ (pilot statistic fixed on WMT22: ρ and the predicted-label
  statistic gave the same development result; ρ is the paper's "first number").
* S4 select-or-abstain: S3 unless the chosen evaluator's pilot ρ is below 0.2, the cost law's break-even for a 50-item MT
  pilot (ρ² < 1/(P_eff + 1), P_eff ≈ 25); then S1. A predicted-saving threshold (5%) was also tried on WMT22 and only
  removed gains; it is not used.
* Coefficient rule: refitted on all labels (main, `cvq`) and pilot-fixed (secondary, `cvl`).
* Reference points, not strategies: post-hoc best evaluator on dedup, mean evaluator, selection-noise test.

## Development result (WMT22, 33 informative cells, 300 audits; `ana/dev/`)
Cost relative to S1 (negative = cheaper): refit — S2 −4.4% (cheaper in 85% of cells), S3 −3.2% (88%), S4 −3.2%,
post-hoc best −7.7%, mean evaluator −2.0%; pilot-fixed — S2 −2.2% (76%), S3 +2.3% (27%), S4 +2.2%.
So on the development year: with a frozen coefficient pilot selection loses; with refitting a pre-fixed strong evaluator
is as good as or better than pilot selection; abstention does not help.

## Pre-specified held-out outcomes
1. Does S2 (fixed COMET-22) beat S1 in most informative WMT23 cells with refitting? (dev: 85%)
2. Does S3 (pilot selection) beat S1 with refitting (dev: 88%) and lose with the frozen coefficient (dev: 27%)?
3. Is the post-hoc best evaluator's lead over S2 within selection noise, and does S3 reach it?
4. Share of informative cells where S3 / S4 cost more than S1 by over 2% (selection failures; dev refit: 3%, frozen: 45%).
5. Wrong-certificate rate at J50 of every strategy ≤ the human-only design's plus Monte-Carlo noise.
6. Decision-level ρ of the strongest new judges (XCOMET-XXL, MetricX-23, GEMBA-MQM, CometKiwi-XXL) and their HES
   over dedup, against the ρ ≤ 0.43 of the WMT22 metrics.
The WMT23 numbers were not seen when this file was written; they are reported whatever they are.
