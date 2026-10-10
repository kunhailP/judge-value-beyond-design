# Auditor strategies fixed on WMT22 and applied to WMT23 (held-out year)

Pre-registered in `prereg/PROSPECTIVE_LOCK_v1.2.md` before the WMT23 records were examined. Code: `code/128_strategies.py`,
`code/RUN_PAIRS_23.sh`, `code/mt_build_pool23.py`, `code/mtme_import23.py`. Development grid: `results/strategies/devgrid/`.

Strategies (one arm per audit, chosen with pilot information only): S1 the judge-free dedup design; S2 dedup + COMET-22
fixed in advance; S3 dedup + the evaluator with the highest pilot rho; S4 = S3 unless that rho < 0.2 (then S1).
Reference points: post-hoc best evaluator (chosen from realised costs), mean evaluator. Cost = J50 (labels at 50%
certification, pilot included); 'excess' = J50 / J50(S1) - 1, negative = cheaper than the judge-free design.

## coefficient refitted on all labels (main)

| | WMT22 (development) | WMT23 (held-out) |
|---|---|---|
| informative cells | 33 (en-de 4, zh-en 29) | 26 (en-de 16, zh-en 10) |
| design saving vs uniform, median | 5.2% | 4.1% |
| pilot share of J50(S1), median | 37% | 53% |
| S2 fixed COMET-22: mean excess over S1 (cheaper in % of cells) | -4.4% (85%) | -3.1% (92%) |
| S3 pilot selection: mean excess over S1 (cheaper in % of cells) | -3.2% (88%) | -3.3% (85%) |
| S4 select or abstain: mean excess over S1 (cheaper in % of cells) | -3.2% (88%) | -3.1% (85%) |
| post-hoc best (reference): mean excess over S1 (cheaper in % of cells) | -7.7% (100%) | -7.9% (100%) |
| mean evaluator (reference): mean excess over S1 (cheaper in % of cells) | -2.0% (85%) | -2.5% (88%) |
| S3: cells costlier than S1 by > 2% | 3% | 4% |
| S4: cells costlier than S1 by > 2% | 3% | 4% |
| S4 abstention share | 3.9% | 1.7% |
| wrong certificates at J50: S1 / S2 / S3 (mean) | 0.003 / 0.003 / 0.003 | 0.008 / 0.006 / 0.007 |
| post-hoc best beyond selection noise (p < 0.05), share of cells | 0% | 0% |

## coefficient fitted on the pilot and frozen

| | WMT22 (development) | WMT23 (held-out) |
|---|---|---|
| informative cells | 33 (en-de 4, zh-en 29) | 26 (en-de 16, zh-en 10) |
| design saving vs uniform, median | 5.2% | 4.1% |
| pilot share of J50(S1), median | 37% | 53% |
| S2 fixed COMET-22: mean excess over S1 (cheaper in % of cells) | -2.2% (76%) | -0.3% (62%) |
| S3 pilot selection: mean excess over S1 (cheaper in % of cells) | +2.3% (27%) | +3.4% (19%) |
| S4 select or abstain: mean excess over S1 (cheaper in % of cells) | +2.2% (27%) | +3.5% (15%) |
| post-hoc best (reference): mean excess over S1 (cheaper in % of cells) | -6.2% (100%) | -5.5% (100%) |
| mean evaluator (reference): mean excess over S1 (cheaper in % of cells) | +0.1% (61%) | +0.0% (62%) |
| S3: cells costlier than S1 by > 2% | 45% | 50% |
| S4: cells costlier than S1 by > 2% | 55% | 50% |
| S4 abstention share | 3.9% | 1.7% |
| wrong certificates at J50: S1 / S2 / S3 (mean) | 0.003 / 0.003 / 0.003 | 0.008 / 0.006 / 0.006 |
| post-hoc best beyond selection noise (p < 0.05), share of cells | 3% | 0% |

## Evaluators (pilot rho median over informative cells; mean HES over dedup)

WMT22: 31 metrics, rho max 0.28, none >= 0.3; COMET-22 rank 4 (rho 0.25).  
WMT23: 42 metrics, rho max 0.36, 8 >= 0.3 (MetricX-23 and XCOMET variants); COMET-22 rank 20 (rho 0.22); GEMBA-MQM (GPT-4) rho 0.20.  
Mean refitted HES over evaluators: WMT22 2.0%, WMT23 2.5%; with the frozen coefficient -0.1% and -0.0%.

WMT23 top 10 by pilot rho:

| judge                       |   rho |   refit |   pilot |
|:----------------------------|------:|--------:|--------:|
| mtme_MetricX-23-QE-b-src    | 0.356 |   0.046 |   0.013 |
| mtme_XCOMET-Ensemble-refA   | 0.35  |   0.051 |   0.017 |
| mtme_MetricX-23-QE-src      | 0.344 |   0.044 |   0.011 |
| mtme_XCOMET-XXL-refA        | 0.33  |   0.056 |   0.017 |
| mtme_XCOMET-QE-Ensemble-src | 0.329 |   0.039 |   0.013 |
| mtme_MetricX-23-QE-c-src    | 0.318 |   0.05  |   0.023 |
| mtme_XCOMET-XL-refA         | 0.314 |   0.042 |   0.01  |
| mtme_MetricX-23-b-refA      | 0.305 |   0.035 |   0.004 |
| mtme_MetricX-23-refA        | 0.3   |   0.038 |   0.014 |
| mtme_cometoid22-wmt22-src   | 0.251 |   0.037 |  -0.003 |

## Reading

* The development pattern reproduces on the held-out year: with refitting, a strong evaluator fixed in advance and pilot
  selection both save about 3% of labels over the judge-free design (cheaper in 85-92% of cells); with a frozen
  coefficient pilot selection costs labels (cheaper in 19-27% of cells, costlier by over 2% in 45-50%).
* Abstaining on weak pilot evidence (rho < 0.2) changes little: the rule abstains in 2-4% of audits.
* Pilot selection does not reach the post-hoc best (-7.7% / -7.9%), whose lead over S2 is within selection noise at 300
  audits in every cell; the new strong judges (XCOMET, MetricX-23) raise decision-level rho to 0.36 and the best
  refitted HES to 5-6%, still below the WMT22 design saving in most cells.
* What an auditor should do, by these two years: use the dedup design; add one strong evaluator and refit its
  coefficient; do not spend the pilot on choosing the evaluator, and do not freeze the coefficient.