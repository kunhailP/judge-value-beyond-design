# From System Ranking to Decision Value: how much human evaluation do automatic evaluators actually save?

Code, pre-registration record and results for a study of how many human labels an LLM judge saves for a concrete
evaluation decision — certifying that a selected system is within ε of the best of a menu — measured against the
cheapest annotation design that uses no judge, in retrieval, machine translation (WMT22 MQM) and open-ended chat (LMArena).

## Main findings (details in `results/HYPOTHESES.md`, `results/MTME_VERDICTS.md` and the paper)
* **Evaluator quality depends on the level of measurement.** On WMT22 en→de and zh→en the 31 submitted metrics reach
  system-level Pearson up to 0.99, often rank the four closest systems no better than chance (MetricX-XL/XXL-DA on
  zh→en: Pearson 0.994–0.995, top-4 Kendall 0), and reach a correlation of per-segment paired differences (decision-level ρ)
  of only 0.11–0.38. Part of this is label noise: on en→de two raters' paired differences correlate only
  0.31–0.41 (3-rater re-annotation), so a perfect evaluator would reach ρ ≈ 0.59 against the single ratings the audits use
  (`code/124_human_ceiling.py`, `results/HUMAN_CEILING.md`).
* **The design takes most of the saving.** Against the best fixed judge-free design (skip known-zero differences, label
  shared outputs once, sample by a label-free proxy of |D|), the best of the 31 metrics, chosen post hoc, adds at most 7%
  with the pilot-fixed coefficient (refitted on all labels: up to 15% in one cell, `results/LOCKED_VARIANTS.md`);
  the design itself saves 8–16% (MT) and 41–57% (retrieval) of uniform sampling's human labels (pre-registered H1, H8: 4/4).
* **Committing to the coefficient early has a price, not the evaluator.** Fitting the correction coefficient on a 50-item
  pilot and freezing it costs 4.3 [3.5, 5.2] (en→de) and 2.5 [2.0, 3.1] (zh→en) points over the 31 metrics (H9).
  Refitting it on all labels (exploratory, analogous to standard PPI++) removes this tax in our simulations, with average coverage
  of the upper bounds near nominal; cross-fitting recovers it only partly (`results/ROBUSTNESS.md`).
* **Across 30 two-system decisions (exploratory; `code/RUN_PAIRS_MTME.sh`, `code/122_decisions.py`, `results/DECISIONS.md`).**
  In the 33 informative decision × ε cells (19 decisions) the judge-free design saves a median 5.5% and beats the mean
  of 34 evaluators in 82–94% of cells; at 300 audits the post-hoc best evaluator's lead is within selection noise, at
  2,000 audits it exceeds it in 72% of cells (`results/DECISIONS_n2000.md`). Refitted HES follows the tax-free
  approximation ρ²(1 − P/J), which is below 5% in 94% of decision–evaluator pairs.
* **Pre-submission checks (2026-10-09; `results/VARIANTS.md`, `results/LOCKED_VARIANTS.md`, `results/EXCLUSION.md`).**
  The weighted design's dissimilarity bins are three, not four (description corrected; `prereg/LOCK_HISTORY.md`); a
  four-quartile variant, pilots of 10 and 25 segments, 2,000 audits per cell and the same-design comparison of all 31
  metric variants in the locked cells are reported there. With 2,000 audits per cell the one-sided 95% upper bound of an
  evaluator's refitted HES over the design is below 5% in 64% and below 10% in 94% of decision–evaluator pairs (29% / 88%
  for the ten strongest evaluators); with pilots of 25 and 10 segments the mean evaluator adds 0.7% and 0.3% refitted
  (−2.7% and −7.7% with a frozen coefficient) against a design saving of 4.3–4.4%; four bins change the summary by ≤ 0.4 points.
* **The design saving in MT is mostly deduplication** (not re-rating identical outputs): 13%/6% of uniform-sampling labels on
  en→de and all of the 8% on zh→en.
  It does not rest on averaging the separate WMT22 ratings of identical strings: sharing one random rating instead gives
  a median design saving of 5.2% (vs 5.5%) over the 33 informative cells and 8.5–17% in the locked cells
  (`results/DECISIONS_SENSITIVITY.md`). The 33-cell summary is also unchanged for informativeness thresholds 0.2–0.5
  and for the ten evaluators with the highest system-level correlation.
* **A finite-pilot cost law describes the dependence on ρ.** HES ≈ [ρ² − (1−ρ²)/P_eff](1 − P/J). Under *controlled*
  variation of ρ (semi-synthetic evaluators, ρ = 0.1–0.9, 126 cells; identical strings share one synthetic score) prediction and realisation correlate 0.97; about
  ρ ≈ 0.5 is needed to save 10%, ρ ≈ 0.8 to save 30%. Real evaluators lie at ρ ≤ 0.43, where realised savings are within a
  few points of zero and Monte-Carlo noise dominates cell-level prediction.
* **Chat.** Pairwise LLM judges reach ρ 0.07–0.29 on close LMArena pairs; averaging both presentation orders raises ρ.
* **Held-out year (2026-10-10; `prereg/PROSPECTIVE_LOCK_v1.2.md`, `results/HELDOUT_WMT23.md`).** Four auditor strategies fixed on
  WMT22 and applied unchanged to WMT23 en→de / zh→en (42 metrics, 30 two-system decisions, 26 informative cells, 2,000
  simulated audits per cell): with a refitted coefficient, dedup + a pre-fixed COMET-22 costs 3.4% [2.9, 3.9] less than
  dedup alone (cheaper in all 26 informative cells); choosing the evaluator from the pilot instead changes the cost by
  −0.1% [−0.7, +0.5] in a paired comparison (WMT22: −1.5% [−4.4, +0.3]; Monte-Carlo intervals from one resampling of audit
  indices shared by every cell; treating decisions as clusters widens them to [−1.2, +1.1] and [−8.9, +1.3]), every interval
  below the 2-point margin set after the 300-audit results; with a
  frozen coefficient pilot selection costs 4.2% more. The post-hoc best (−7.0%) is a reference, not a strategy. Coverage of
  every strategy's bound is nominal at the certifying budget (0.89–0.90) and 0.86–0.89 at the worst budget once known-zero
  differences are set to zero (the 300-audit records without it had S2 at 0.45–0.50 at the smallest budgets); in boundary
  stress the type-I error at ten post-pilot labels is 0.18 (S1), 0.17 (S2), 0.12 (S3), nominal from 30–60 labels on, and
  below the human-only design on average (above it at 15–34% of cell–budget points, by over 2 points at 1–3%). The observed
  mean error is at or below 0.10 at every later budget from about 206 (en-de) / 265 (zh-en) labels on, and at or below 0.125
  from about 145 (an observation on this simulation, checked on a second seed; not a calibrated bound). Post-hoc sensitivity
  analysis: a protocol that certifies only from those budgets, same rule for every strategy, on the same 26 cells keeps
  0.4% [0.2, 0.6] of S2's 3.4% saving at the 0.10 cut-off (22 cells certify at the first allowed budget) and 3.0% [2.5, 3.4]
  at the 0.125 cut-off; the strategy ranking is unchanged (`code/129_s2_vs_s3.py --min_budget --cells_from`, `results/strategies/`).
* **Strong evaluators are the exception** (`code/130_decomposition.py`, `results/strategies/DECOMPOSITION_n2000.md`): on the
  same audits, the mean metric adds 1.8–2.5% on dedup (refit), the strongest of each year (MetricX-XXL, XCOMET-XXL)
  3.7–4.7%, as much as the design in a third to over half of the cells; the design still saves more than the mean evaluator
  in 69–79% of cells and than every evaluator with a frozen coefficient.
* **Failed pre-registered hypotheses are reported:** H2 (inflation over uniform), H4 in chat, H5 (pilot-based judge
  selection), H6 (chat savings ≥ 5% in ≥ 3/6 pairs).
* Terminology: "best fixed judge-free baseline" is a benchmark chosen per cell from realised costs, not a procedure an
  auditor selects; menus are built from full human labels only to be deliberately hard.

## Layout
| Path | Content |
|---|---|
| `docs/DESIGN_v0.1.md` | Initial study design (superseded by the locks) |
| `prereg/` | Locks v0.8 (MT, Arena), v0.9 (Arena close pairs), v1.0 (frontier judges, not yet run), v1.1 (all 31 WMT22 metrics), v1.2 (held-out year, with addendum) and `LOCK_HISTORY.md` |
| `docs/` | Design log and the revision notes of 2026-10-09 and 2026-10-10 (internal; excluded from the supplementary archive) |
| `code/110_unit_audit.py` | Fixed-budget certification audits (designs, pilot-fixed λ control variate, certificates, pilot predictions) |
| `code/111_summarize.py` | J_τ, HES, inflation, selection, pilot-prediction scores with paired bootstrap intervals |
| `code/121_robustness.py`, `code/122_decisions.py`, `code/RUN_PAIRS_MTME.sh`, `code/RUN_ARENA_ROBUST2.sh` | Exploratory: coefficient rules (pilot / refit / cross-fit / oracle), 30 two-system decisions, coverage, selection-noise test |
| `code/123_decision_sensitivity.py`, `code/124_human_ceiling.py` | Exploratory: informativeness threshold, evaluator set and identical-string label (`--ident pick`) sensitivity; human noise ceiling for decision-level ρ |
| `code/mt_build_pool23.py`, `code/mtme_import23.py`, `code/RUN_PAIRS_23.sh`, `code/128_strategies.py`, `code/129_s2_vs_s3.py`, `code/130_decomposition.py` | Held-out year: WMT23 pools and metrics, the 30 WMT23 decisions, pre-fixed auditor strategies (dev grid `results/strategies/devgrid/`), paired S2 vs S3 comparison with coverage, same-condition A–B–C–D decomposition (Figure 1) |
| `code/125_exclusion.py`, `code/126_variants.py`, `code/127_locked_variants.py`, `code/RUN_PAIRS_EXTRA.sh` | Pre-submission: one-sided upper bounds on evaluator savings (what the decisions rule out), the 30 decisions with pilots 10/25, four bins and 2,000 audits (`--bins`, `--draws`), matched-base comparison of all 31 metrics in the locked cells |
| `code/112–120`, `mtme_import.py` | Judge anatomy, cost law, ρ dial, position bias, estimation tax, hypothesis verdicts, boundary calibration, v1.1 verdicts, figures; WMT22 metric import |
| `code/101_ir_hes.py` | Retrieval block: J_τ, HES and selection from the per-draw records of an earlier retrieval study |
| `code/mt_*.py`, `code/arena_*.py` | Pool builders (WMT22 MQM, LMArena 55k) and judges (COMET-22, GEMBA-DA, pairwise LLM judge) |
| `code/frontier_*.py`, `code/run_frontier.py` | Frontier-judge export, runner and scoring (lock v1.0) |
| `code/RUN_LOCKED.sh` | Every locked run |
| `results/` | Per-draw records (`*_draws.parquet`), pilot predictions, summaries, verdicts; `results/strategies/` holds the held-out-year strategy, S2-vs-S3, boundary, restricted-protocol and decomposition outputs |
| `paper/` | ACL-format manuscript, figures, checklist |
| `submission/` | Compiled manuscript of the tagged submission commit (`submission/README.md`) |
| `make_supplementary.sh` | Builds the anonymised supplementary archive from the committed tree |

## Data
Pools and judge outputs live under `$JV_DATA` (default `./data`) and are not redistributed:
* WMT22 MQM: `github.com/google/wmt-mqm-human-evaluation` @ `29acd69` → `code/mt_build_pool.py` → `$JV_DATA/mt/{ende,zhen}/pool.parquet`
* LMArena: `lmarena-ai/arena-human-preference-55k` → `code/arena_pool.py`, `code/arena_pool_v09.py` → `$JV_DATA/arena/pool*.parquet`
* Judges: `code/mt_comet.py`, `code/mt_gemba.py`, `code/arena_judge.py` (one 24 GB GPU; models and revisions in the scripts)
* WMT22 metric scores: mt-metrics-eval-v2 (`https://data.statmt.org/wmt26/mt-metrics-eval-v2.tgz`) extracted to `$JV_DATA/mtme/` → `code/mtme_import.py`
* WMT23 (held-out): the same archive's `wmt23/` (human-scores, system-outputs, references, metric-scores) → `code/mt_build_pool23.py`, `code/mtme_import23.py`
* Retrieval: `101_ir_hes.py` reads the per-draw records of the earlier retrieval study (`*_draws.csv`); its outputs are in `results/ir/`.

## Reproduction
```
pip install -r requirements.txt
export JV_DATA=/path/to/data
bash code/RUN_LOCKED.sh mt; bash code/RUN_LOCKED.sh mt_pairs; bash code/RUN_LOCKED.sh arena; bash code/RUN_LOCKED.sh arena_v09; bash code/RUN_LOCKED.sh boundary; bash code/RUN_LOCKED.sh exploratory
python3 code/112_mt_judge_anatomy.py; python3 code/113_cost_law.py; python3 code/114_rho_dial.py
python3 code/115_arena_order.py; python3 code/116_estimation_tax.py; python3 code/117_hypotheses.py
python3 code/118_boundary_calibration.py; python3 code/mtme_import.py; python3 code/119_mtme_verdicts.py; python3 code/120_figures.py
# exploratory: 30 two-system decisions, chat robustness, sensitivity, human noise ceiling
bash code/RUN_PAIRS_MTME.sh; bash code/RUN_ARENA_ROBUST2.sh; python3 code/122_decisions.py
IDENT=pick bash code/RUN_PAIRS_MTME.sh; DECISIONS_VARIANT=pick python3 code/122_decisions.py
for s in 0 1 2; do for lp in ende zhen; do python3 code/110_unit_audit.py mt $lp --pilot 50 --eps 0.01 0.02 --ident pick --ident_seed $s --tag _pick$s; done; done
python3 code/123_decision_sensitivity.py; python3 code/124_human_ceiling.py
# pre-submission: what the decisions rule out; pilot 25 / 10, four bins, 2,000 audits; locked cells with --extra arms and four bins
python3 code/125_exclusion.py
for v in "25 300 3 p25" "10 300 3 p10" "50 300 4 b4" "50 2000 3 n2000"; do set -- $v; PILOT=$1 DRAWS=$2 BINS=$3 TAG=$4 bash code/RUN_PAIRS_EXTRA.sh; python3 code/125_exclusion.py --variant $4; done
python3 code/126_variants.py
for lp in ende zhen; do for v in "3 _mtmex" "4 _mtmeb4"; do set -- $v; python3 code/110_unit_audit.py mt $lp --judges $(python3 -c "import json;print(' '.join(json.load(open('results/mt/mt_${lp}_m4_p50_mtme_info.json'))['judges']))") --pilot 50 --eps 0.01 0.02 --oracle --extra --bins $1 --tag $2; done; done
python3 code/127_locked_variants.py
# held-out year: WMT23 pools, 30 decisions, strategies fixed on WMT22 (per-draw records regenerable; ~2 min per cell on 128 cores)
python3 -I code/mt_build_pool23.py; python3 -I code/mtme_import23.py; bash code/RUN_PAIRS_23.sh                     # 300 audits (tag pair23)
DRAWS=2000 TAG=pair23n bash code/RUN_PAIRS_23.sh; TAG=pair23b EXTRA_ARGS=--boundary bash code/RUN_PAIRS_23.sh   # 2,000 audits; boundary stress
for m in cvq cvl; do python3 code/128_strategies.py --glob 'results/mt/mt_*_m2_p50_pairmtmez??' --design dedup --fixed mtme_COMET-22-refA --mode $m --stat rho --r0 0.2 --s0 -1 --out results/strategies/STRATEGIES_wmt22z_$( [ $m = cvq ] && echo refit || echo pilot ); python3 code/128_strategies.py --glob 'results/mt/mt_*23_m2_p50_pair23n??' --design dedup --fixed mtme_COMET-refA --mode $m --stat rho --r0 0.2 --s0 -1 --out results/strategies/STRATEGIES_wmt23_n2000_$( [ $m = cvq ] && echo refit || echo pilot ); done
python3 code/129_s2_vs_s3.py --glob 'results/mt/mt_*_m2_p50_pairmtmez??' --fixed mtme_COMET-22-refA --boot 400 --out results/strategies/S2_vs_S3_wmt22z
python3 code/129_s2_vs_s3.py --glob 'results/mt/mt_*23_m2_p50_pair23n??' --fixed mtme_COMET-refA --boot 1000 --out results/strategies/S2_vs_S3_wmt23_n2000
python3 code/129_s2_vs_s3.py --glob 'results/mt/mt_*23_m2_p50_boundary_pair23b??' --fixed mtme_COMET-refA --boot 200 --out results/strategies/S2_vs_S3_wmt23_boundary
python3 code/130_decomposition.py --glob22 'results/mt/mt_*_m2_p50_pairmtmez??' --glob23 'results/mt/mt_*23_m2_p50_pair23n??' --out results/strategies/DECOMPOSITION_n2000
# restricted protocol (post-hoc sensitivity): no certificate below the post-pilot budget from which the observed boundary type-I error stays at or below 0.10 (S2_vs_S3_wmt23_boundary_certification_range.csv); cell sets fixed to the unrestricted run
python3 code/129_s2_vs_s3.py --glob 'results/mt/mt_*23_m2_p50_pair23n??' --fixed mtme_COMET-refA --boot 1000 --min_budget ende23:55 zhen23:88 --cells_from results/strategies/S2_vs_S3_wmt23_n2000.csv --out results/strategies/S2_vs_S3_wmt23_n2000_restricted   # 0.125 cut-off: ende23:23 zhen23:29, _restricted_tol
python3 code/128_strategies.py --glob 'results/mt/mt_*23_m2_p50_pair23n??' --design dedup --fixed mtme_COMET-refA --mode cvq --stat rho --r0 0.2 --s0 -1 --min_budget ende23:55 zhen23:88 --out results/strategies/STRATEGIES_wmt23_n2000_restricted_refit
TAG=pair23c EXTRA_ARGS="--boundary --seed 20261011" bash code/RUN_PAIRS_23.sh; python3 code/129_s2_vs_s3.py --glob 'results/mt/mt_*23_m2_p50_boundary_pair23c??' --fixed mtme_COMET-refA --boot 200 --out results/strategies/S2_vs_S3_wmt23_boundary_seed2   # second seed for the cut-offs
# pairmtmez: the 30 WMT22 decisions re-run with known-zero differences zeroed (110_unit_audit.py --zero_known 1, now the default; the 31 metric variants only: SUFFIX=z bash code/RUN_PAIRS_MTME.sh with the three LLM judges dropped from --judges)
```
Reproduction check (2026-10-09): rebuilding the pools and the 31 metric judges from the public sources above on another
machine (numpy 2.5.3) and re-running `110_unit_audit.py mt zhen --judges <31 metrics> --pilot 50 --eps 0.01 0.02 --oracle`
reproduced `results/mt/mt_zhen_m4_p50_mtme_draws.parquet` exactly (every cost, certificate and pilot quantity).
Every summary in `results/` is regenerated from the committed per-draw records by `111_summarize.py` without the data.

## Paper and submission
`paper/main.tex` compiles with pdflatex + bibtex (ACL style included). The submitted build is `submission/main.pdf`;
the GitHub release `arr-2026-10-submission-v2` carries that PDF and the anonymised supplementary archive produced by
`SUPP_IDENT_REGEX='<identifying strings>' ./make_supplementary.sh supplementary.zip` (the earlier release
`arr-2026-10-submission` is the 2026-10-09 build). Per-draw records of the held-out-year runs (`pair23*`, `pairmtmez`)
are not committed (regenerable with the commands above; ~1,200 CPU-hours); their summaries are in `results/strategies/`.

## Licence
Code: MIT. Results: CC BY 4.0.
