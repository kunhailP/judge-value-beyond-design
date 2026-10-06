# From System Ranking to Decision Value: how much human evaluation do automatic evaluators actually save?

Code, pre-registration record and results for a study of how many human labels an LLM judge saves for a concrete
evaluation decision — certifying that a selected system is within ε of the best of a menu — measured against the
cheapest annotation design that uses no judge, in retrieval, machine translation (WMT22 MQM) and open-ended chat (LMArena).

## Main findings (details in `results/HYPOTHESES.md`, `results/MTME_VERDICTS.md` and the paper)
* **Evaluator quality depends on the level of measurement.** On WMT22 en→de and zh→en the 31 submitted metrics reach
  system-level Pearson up to 0.99, often rank the four closest systems no better than chance (MetricX-XL/XXL-DA on
  zh→en: Pearson 0.994–0.995, top-4 Kendall 0), and reach a correlation of per-segment paired differences (decision-level ρ)
  of only 0.15–0.38.
* **The design takes most of the saving.** Against the best fixed judge-free design (skip known-zero differences, label
  shared outputs once, sample by a label-free proxy of |D|), the best of the 31 metrics, chosen post hoc, adds at most 7%;
  the design itself saves 8–16% (MT) and 41–57% (retrieval) of uniform sampling's human labels (pre-registered H1, H8: 4/4).
* **Committing to the coefficient early has a price, not the evaluator.** Fitting the correction coefficient on a 50-item
  pilot and freezing it costs 4.3 [3.5, 5.2] (en→de) and 2.5 [2.0, 3.1] (zh→en) points over the 31 metrics (H9).
  Refitting it on all labels (exploratory, analogous to standard PPI++) removes this tax with nominal coverage of the
  upper bounds in our simulations; cross-fitting recovers it only partly (`results/ROBUSTNESS.md`).
* **Across 30 two-system decisions (exploratory; `code/RUN_PAIRS_MTME.sh`, `code/122_decisions.py`, `results/DECISIONS.md`).**
  In the 33 informative decision × ε cells (19 decisions) the judge-free design saves a median 5.5% and beats the mean
  of 34 evaluators in 82–94% of cells; the post-hoc best evaluator's lead is within selection noise. Refitted HES
  follows the tax-free ceiling ρ²(1 − P/J), which is below 5% in 94% of decision–evaluator pairs.
* **The design saving in MT is mostly deduplication** (not re-rating identical outputs): 13%/6% of uniform-sampling labels on
  en→de and all of the 8% on zh→en.
* **A finite-pilot cost law describes the dependence on ρ.** HES ≈ [ρ² − (1−ρ²)/P_eff](1 − P/J). Under *controlled*
  variation of ρ (semi-synthetic evaluators, ρ = 0.1–0.9, 126 cells) prediction and realisation correlate 0.975; about
  ρ ≈ 0.5 is needed to save 10%, ρ ≈ 0.8 to save 30%. Real evaluators lie at ρ ≤ 0.38, where realised savings are within a
  few points of zero and Monte-Carlo noise dominates cell-level prediction.
* **Chat.** Pairwise LLM judges reach ρ 0.07–0.29 on close LMArena pairs; averaging both presentation orders raises ρ.
* **Failed pre-registered hypotheses are reported:** H2 (inflation over uniform), H4 in chat, H5 (pilot-based judge
  selection), H6 (chat savings ≥ 5% in ≥ 3/6 pairs).
* Terminology: "best fixed judge-free baseline" is a benchmark chosen per cell from realised costs, not a procedure an
  auditor selects; menus are built from full human labels only to be deliberately hard.

## Layout
| Path | Content |
|---|---|
| `prereg/` | Locks v0.8 (MT, Arena), v0.9 (Arena close pairs), v1.0 (frontier judges, not yet run), v1.1 (all 31 WMT22 metrics) and `LOCK_HISTORY.md` |
| `code/110_unit_audit.py` | Fixed-budget certification audits (designs, pilot-fixed λ control variate, certificates, pilot predictions) |
| `code/111_summarize.py` | J_τ, HES, inflation, selection, pilot-prediction scores with paired bootstrap intervals |
| `code/121_robustness.py`, `code/122_decisions.py`, `code/RUN_PAIRS_MTME.sh`, `code/RUN_ARENA_ROBUST2.sh` | Exploratory: coefficient rules (pilot / refit / cross-fit / oracle), thirty two-system decisions, coverage, selection-noise test |
| `code/112–120`, `mtme_import.py` | Judge anatomy, cost law, ρ dial, position bias, estimation tax, hypothesis verdicts, boundary calibration, v1.1 verdicts, figures; WMT22 metric import |
| `code/101_ir_hes.py` | Retrieval block: J_τ, HES and selection from the per-draw records of an earlier retrieval study |
| `code/mt_*.py`, `code/arena_*.py` | Pool builders (WMT22 MQM, LMArena 55k) and judges (COMET-22, GEMBA-DA, pairwise LLM judge) |
| `code/frontier_*.py`, `code/run_frontier.py` | Frontier-judge export, runner and scoring (lock v1.0) |
| `code/RUN_LOCKED.sh` | Every locked run |
| `results/` | Per-draw records (`*_draws.parquet`), pilot predictions, summaries, verdicts |
| `paper/` | ACL-format manuscript |

## Data
Pools and judge outputs live under `$JV_DATA` (default `./data`) and are not redistributed:
* WMT22 MQM: `github.com/google/wmt-mqm-human-evaluation` @ `29acd69` → `code/mt_build_pool.py` → `$JV_DATA/mt/{ende,zhen}/pool.parquet`
* LMArena: `lmarena-ai/arena-human-preference-55k` → `code/arena_pool.py`, `code/arena_pool_v09.py` → `$JV_DATA/arena/pool*.parquet`
* Judges: `code/mt_comet.py`, `code/mt_gemba.py`, `code/arena_judge.py` (one 24 GB GPU; models and revisions in the scripts)
* WMT22 metric scores: mt-metrics-eval-v2 (`https://data.statmt.org/wmt26/mt-metrics-eval-v2.tgz`) extracted to `$JV_DATA/mtme/` → `code/mtme_import.py`
* Retrieval: `101_ir_hes.py` reads the per-draw records of the earlier retrieval study (`*_draws.csv`); its outputs are in `results/ir/`.

## Reproduction
```
pip install -r requirements.txt
export JV_DATA=/path/to/data
bash code/RUN_LOCKED.sh mt; bash code/RUN_LOCKED.sh mt_pairs; bash code/RUN_LOCKED.sh arena; bash code/RUN_LOCKED.sh arena_v09; bash code/RUN_LOCKED.sh boundary; bash code/RUN_LOCKED.sh exploratory
python3 code/112_mt_judge_anatomy.py; python3 code/113_cost_law.py; python3 code/114_rho_dial.py
python3 code/115_arena_order.py; python3 code/116_estimation_tax.py; python3 code/117_hypotheses.py
python3 code/118_boundary_calibration.py; python3 code/mtme_import.py; python3 code/119_mtme_verdicts.py; python3 code/120_figures.py
```
Every summary in `results/` is regenerated from the committed per-draw records by `111_summarize.py` without the data.

## Licence
Code: MIT. Results: CC BY 4.0.
