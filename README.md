# What is an LLM judge worth? Human labels saved beyond the best annotation design

Code, pre-registration record and results for a study of how many human labels an LLM judge saves for a concrete
evaluation decision — certifying that a selected system is within ε of the best of a menu — measured against the
cheapest annotation design that uses no judge, in retrieval, machine translation (WMT22 MQM) and open-ended chat (LMArena).

## Main findings (details in `results/HYPOTHESES.md` and the paper)
* **The design dominates.** Decision-aware human sampling saves 41–57% (retrieval) and 8–19% (MT) of the human labels of
  uniform sampling; open judges add 3–20% (retrieval) and ≈ 0 (MT, chat) on top.
* **Judge quality depends on the level at which it is measured.** COMET-22 and Qwen3-8B reach system-level correlations of
  0.97–0.99 with MQM but a decision-level correlation of the paired differences of only 0.17–0.29.
* **A cost law predicts the saving.** HES ≈ [ρ² − (1−ρ²)/P_eff](1 − P/J): over 126 semi-synthetic cells (ρ = 0.1–0.9)
  prediction and realisation correlate 0.975; about ρ ≈ 0.5 is needed to save 10%, ρ ≈ 0.8 to save 30%.
* **Weak judges cost labels** because fitting the control-variate coefficient on a small pilot has a price (estimation
  tax 4–9 points on en→de); break-even ρ ≈ 1/√(P_eff+1).
* **Position bias** of pairwise judges lowers ρ; averaging both presentation orders recovers part of it.

## Layout
| Path | Content |
|---|---|
| `prereg/` | Locks v0.8 (MT, Arena), v0.9 (Arena close pairs), v1.0 (frontier judges, not yet run) and `LOCK_HISTORY.md` (commit order, deviations, corrections) |
| `code/110_unit_audit.py` | Fixed-budget certification audits (designs, pilot-fixed λ control variate, certificates, pilot predictions) |
| `code/111_summarize.py` | J_τ, HES, inflation, selection, pilot-prediction scores with paired bootstrap intervals |
| `code/112–117` | Judge anatomy, cost law, ρ dial, position bias, estimation tax, hypothesis verdicts |
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
* Retrieval: `101_ir_hes.py` reads the per-draw records of the earlier retrieval study (`*_draws.csv`); its outputs are in `results/ir/`.

## Reproduction
```
pip install -r requirements.txt
export JV_DATA=/path/to/data
bash code/RUN_LOCKED.sh mt; bash code/RUN_LOCKED.sh mt_pairs; bash code/RUN_LOCKED.sh arena; bash code/RUN_LOCKED.sh arena_v09; bash code/RUN_LOCKED.sh boundary; bash code/RUN_LOCKED.sh exploratory
python3 code/112_mt_judge_anatomy.py; python3 code/113_cost_law.py; python3 code/114_rho_dial.py
python3 code/115_arena_order.py; python3 code/116_estimation_tax.py; python3 code/117_hypotheses.py
```
Every summary in `results/` is regenerated from the committed per-draw records by `111_summarize.py` without the data.

## Licence
Code: MIT. Results: CC BY 4.0.
