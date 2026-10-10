# Auditor strategies fixed on WMT22 and applied to WMT23 (held-out year)

Pre-registered in `prereg/PROSPECTIVE_LOCK_v1.2.md` before the WMT23 records were examined. Code: `code/128_strategies.py`, `code/129_s2_vs_s3.py`, `code/130_decomposition.py`,
`code/RUN_PAIRS_23.sh`, `code/mt_build_pool23.py`, `code/mtme_import23.py`. Development grid: `results/strategies/devgrid/`.

Strategies (one arm per audit, chosen with pilot information only): S1 the judge-free dedup design; S2 dedup + COMET-22
fixed in advance; S3 dedup + the evaluator with the highest pilot rho; S4 = S3 unless that rho < 0.2 (then S1).
Reference points: post-hoc best evaluator (chosen from realised costs), mean evaluator. Cost = J50 (labels at 50%
certification, pilot included); 'excess' = J50 / J50(S1) - 1, negative = cheaper than the judge-free design.

## coefficient refitted on all labels (main)

WMT22: 300 audits per cell, re-run with known-zero differences zeroed (tag `pairmtmez`; every entry within 0.1 point of the
original `pairmtme` run, `results/strategies/STRATEGIES_wmt22_*` vs `STRATEGIES_wmt22z_*`). WMT23: 2,000 audits per cell
(tag `pair23n`, `STRATEGIES_wmt23_n2000_*`; the 300-audit run `pair23` is kept in `STRATEGIES_wmt23_*`).

| | WMT22 (development) | WMT23 (held-out) |
|---|---|---|
| informative cells | 33 (en-de 4, zh-en 29) | 26 (en-de 16, zh-en 10) |
| design saving vs uniform, median | 5.2% | 3.8% |
| pilot share of J50(S1), median | 37% | 54% |
| S2 fixed COMET-22: mean excess over S1 (cheaper in % of cells) | -4.4% (85%) | -3.4% (100%) |
| S3 pilot selection: mean excess over S1 (cheaper in % of cells) | -3.2% (88%) | -3.3% (85%) |
| S4 select or abstain: mean excess over S1 (cheaper in % of cells) | -3.2% (88%) | -3.2% (85%) |
| post-hoc best (reference): mean excess over S1 (cheaper in % of cells) | -7.7% (100%) | -7.0% (100%) |
| mean evaluator (reference): mean excess over S1 (cheaper in % of cells) | -2.0% (85%) | -2.8% (100%) |
| S3: cells costlier than S1 by > 2% | 3% | 8% |
| S4: cells costlier than S1 by > 2% | 3% | 8% |
| S4 abstention share | 3.9% | 1.6% |
| wrong certificates at J50: S1 / S2 / S3 (mean) | 0.003 / 0.003 / 0.003 | 0.007 / 0.006 / 0.006 |
| post-hoc best beyond selection noise (p < 0.05), share of cells | 0% (300 audits) | 81% (2,000 audits; 0% at 300) |

## coefficient fitted on the pilot and frozen

| | WMT22 (development) | WMT23 (held-out) |
|---|---|---|
| informative cells | 33 (en-de 4, zh-en 29) | 26 (en-de 16, zh-en 10) |
| S2 fixed COMET-22: mean excess over S1 (cheaper in % of cells) | -2.2% (76%) | -0.4% (65%) |
| S3 pilot selection: mean excess over S1 (cheaper in % of cells) | +2.3% (27%) | +4.2% (23%) |
| S4 select or abstain: mean excess over S1 (cheaper in % of cells) | +2.2% (27%) | +4.2% (23%) |
| post-hoc best (reference): mean excess over S1 (cheaper in % of cells) | -6.2% (100%) | -3.5% (88%) |
| mean evaluator (reference): mean excess over S1 (cheaper in % of cells) | +0.1% (61%) | -0.0% (62%) |
| S3: cells costlier than S1 by > 2% | 45% | 50% |
| S4: cells costlier than S1 by > 2% | 55% | 54% |
| wrong certificates at J50: S1 / S2 / S3 (mean) | 0.003 / 0.003 / 0.003 | 0.007 / 0.005 / 0.005 |

## Evaluators (pilot rho median over informative cells; mean HES over dedup)

WMT22: 31 metrics, rho max 0.28, none >= 0.3; COMET-22 rank 4 (rho 0.25).  
WMT23: 42 metrics, rho max 0.36, 9 >= 0.3 (MetricX-23 and XCOMET variants); COMET-22 rank 21 (rho 0.21); GEMBA-MQM (GPT-4) rho 0.22.  
Mean refitted HES over evaluators: WMT22 2.0%, WMT23 2.8%; with the frozen coefficient -0.1% and 0.0%.

WMT23 top 10 by pilot rho (2,000 audits):

| judge                       |   rho |   refit |   pilot |
|:----------------------------|------:|--------:|--------:|
| mtme_MetricX-23-QE-b-src    | 0.356 |   0.056 |   0.017 |
| mtme_XCOMET-Ensemble-refA   | 0.347 |   0.057 |   0.028 |
| mtme_MetricX-23-QE-src      | 0.342 |   0.050 |   0.016 |
| mtme_XCOMET-QE-Ensemble-src | 0.330 |   0.054 |   0.023 |
| mtme_MetricX-23-QE-c-src    | 0.323 |   0.049 |   0.018 |
| mtme_XCOMET-XXL-refA        | 0.322 |   0.054 |   0.023 |
| mtme_XCOMET-XL-refA         | 0.321 |   0.052 |   0.019 |
| mtme_MetricX-23-b-refA      | 0.301 |   0.043 |   0.006 |
| mtme_MetricX-23-refA        | 0.300 |   0.039 |   0.009 |
| mtme_cometoid22-wmt22-src   | 0.253 |   0.034 |  -0.002 |

## Direct comparison S2 vs S3, coverage, boundary stress, decomposition (addendum to lock v1.2)
See `results/strategies/S2_vs_S3_wmt23_n2000.md`, `S2_vs_S3_wmt22z.md`, `S2_vs_S3_wmt23_boundary.md`, `DECOMPOSITION_n2000.md`
(the 300-audit WMT23 comparison is kept in `S2_vs_S3_wmt23_n300.md`). Pooled G = 1 − J50(S3)/J50(S2), refitted coefficient:
WMT23 informative −0.1% [−1.3, +1.0], all 60 −0.1% [−0.6, +0.5]; WMT22 informative −1.5% [−9.1, +1.0], all 60 −2.1% [−4.5, +0.2];
every interval excludes the 2-point margin (S2 as good as S3). S2 vs S1 on WMT23: +3.4% [2.1, 4.4]; S3 vs S1: +3.3% [1.5, 4.8].
At 300 audits the WMT23 informative interval was +0.2% [−2.7, +3.3] (undecided). Per-cell widths: 4–6 points at 2,000 audits
(two of 26 cells with G above zero, none below), 13–17 at 300.

Coverage of the chosen arm's bound (nominal 0.90), WMT22 / WMT23: at J50 0.89–0.90 for every strategy; over all budgets
0.90 / 0.90–0.91; at the worst budget of a cell 0.86 / 0.88–0.89, the same as the human-only design. The 300-audit records
without zeroing had S2 at 0.45–0.50 at the smallest budgets (minimum 0.15): identical outputs carry a human difference of
exactly zero and a small non-zero metric difference, and a coefficient fitted on a handful of such labels is off; zeroing
removes it at unchanged costs. Wrong certificates at J50: 0.003 (WMT22), 0.006 (WMT23); maxima over budgets 0.008 and 0.012.

Boundary stress (runner-up as candidate, eps = 0.9 × its regret, 300 audits, tag `pair23b`): every certificate is wrong, so the
certification rate is the type-I error (nominal 0.10). Mean over the 30 cells at 10 post-pilot labels: S1 0.18, S2 0.17,
S3/S4 0.12; 0.10 by about 60 (S1) and 30 (S2–S4) labels, 0.05 by about 200, 0.01–0.02 at the largest budgets; per-cell
maxima average 0.18 / 0.18 / 0.13 (S1 / S2 / S3), at most 0.24. No evaluator strategy exceeds the human-only design.

Strong evaluators (2,000 audits): XCOMET-XXL adds a median 4.7% (mean 5.4%) refitted on WMT23 and the design saves more labels
in only 11/26 cells; for the ten evaluators with the highest pilot rho, 44% of (cell, evaluator) pairs (WMT22: MetricX-XXL
3.7%, 22/33, 67%).

## Reading

* The development pattern reproduces on the held-out year: with refitting, a strong evaluator fixed in advance and pilot
  selection both save about 3% of labels over the judge-free design (cheaper in 85-100% of cells); with a frozen
  coefficient pilot selection costs labels (cheaper in 23-27% of cells, costlier by over 2% in 45-50%).
* Abstaining on weak pilot evidence (rho < 0.2) changes little: the rule abstains in 2-4% of audits.
* Pilot selection does not reach the post-hoc best (-7.7% / -7.0%), a reference chosen from the outcome; the selection-noise
  test compares it with the MEAN evaluator (not with S2): uninformative at 300 audits, beyond noise in 81% of cells at
  2,000, so the evaluators differ but the pilot does not find the best one. The strong judges (XCOMET, MetricX-23) raise
  decision-level rho to 0.36 and add 4-5% refitted, as much as the design in over half of the cells.
* What an auditor should do, by these two years: use the dedup design; add one strong evaluator and refit its
  coefficient; do not spend the pilot on choosing the evaluator, and do not freeze the coefficient.