# Pre-registration record

Commits are listed in order; hashes are those of this repository (its history was extracted, with commit dates
unchanged, from the development repository in which the work started). Commit timestamps are self-reported evidence.

| Commit | Time (UTC) | Event |
|---|---|---|
| `a6ba3a3` | 2026-10-06 07:03 | **Lock v0.8** (MT and Arena hypotheses H1–H5, validity). Before any LLM or COMET judgment was joined with a human label. Human-only MT designs and the chrF judge had been examined in development (stated in the lock). |
| `0bd64f2` | 07:43 | Deviation: Arena pair id parsed as an integer (type fix; no analysis change). |
| `47dffcd` | 08:03 | Deviation: Arena pilot charged one vote per battle instead of two (accounting fix; v0.8 Arena rerun). |
| `73a7695` | 08:05 | **Lock v0.9**: the v0.8 Arena decision was uninformative (gaps 0.10–0.56 ≫ ε); six close pairs chosen on human votes only. No judge output existed for these battles. Adds H6. |
| `520c889`, `80fd0f1` | 09:07 | **Lock v1.0**: frontier-model judges; inputs exported and hashed, scoring fixed, H2′ and H7. No frontier request had been made. Not yet run. |
| `1811c18` | 09:31 | Exploratory (post-lock) analyses: judge anatomy, estimation tax, position bias, semi-synthetic ρ dial, cost law. Labelled exploratory everywhere. |

| `a014725` | 11:07 | **Lock v1.1**: all 31 WMT22 submitted metrics as MT judges; H8–H11. Before any HES/J50 of these metrics was computed. |
| `d7bb23a` | — | v1.1 results. Post-lock corrections: H9 interval as a metric-level bootstrap (the two ε of a metric are not independent); H10 additionally reported with PPSR's mean of squared correlations (locked: squared mean). Both leave the verdicts unchanged. |

| `cebe5ec` | 2026-10-10 06:17 | **Lock v1.2** (held-out year): four auditor strategies S1–S4 fixed on the WMT22 development grid, applied unchanged to WMT23 en→de / zh→en. The lock file states that no WMT23 number had been seen when it was written; it was committed in the same commit as the first (300-audit) WMT23 results, so the ordering within that session is self-reported. |
| `2122ece` | 07:37 | **Addendum to v1.2** (declared after the 300-audit WMT23 results, before the runs it names): paired S2 vs S3 comparison, a 2-point margin (post hoc, not pre-registered), 2,000-audit and boundary-stress re-runs, coverage of every strategy. Post-lock code change, applied to every run from here on: known-zero differences set to 0 for every evaluator (`--zero_known 1`, default); the earlier records (`pair23`, `pairmtme`) keep the metrics' small non-zero scores on identical outputs. |
| `c4851d3` | 12:16 | 2,000-audit WMT23 results replace the 300-audit ones in the paper; WMT22 re-run with zeroing (`pairmtmez`) agrees with the original within 0.1 point; the under-coverage of the refitted bound at small budgets is traced to the non-zeroed records. |
| `b83d3e5` | 13:27 | Correction of the S2 vs S3 interval: the point estimate (mean over cells) and the interval (previously a cluster bootstrap over decisions) now use the same statistic; one resampling of audit indices shared by every cell (common random numbers) is the primary Monte-Carlo interval, the cluster bootstrap a sensitivity analysis. Boundary stress of the strategies reported by budget; a restricted protocol (minimum budget) added as a post-hoc sensitivity analysis. |
| `97d1e1e` | 14:28 | Correction of the restricted protocol: J50 interpolated over the allowed budgets only (the first version interpolated across the disallowed ones); cell sets fixed across protocols; the budget cut-offs read off the observed mean boundary error with joint-resampling intervals (a pooled binomial test over dependent audits removed) and checked on a second seed (`pair23c`). |

Corrections to the lock documents themselves:
* The lock files were written with the date 2026-10-07 in their file names; they were committed on 2026-10-06
  (table above). The files were renamed without the date; their content is unchanged.

Description corrected after submission review (2026-10-09; code unchanged):
* The weighted design's `bin_index` + `np.maximum(., 1)` in `110_unit_audit.py` folds the dissimilarities below the
  first quartile into the first bin, so the positive dissimilarities fall into three bins (below the median, third
  quartile, fourth quartile), not the four quartile bins an earlier manuscript draft described. This has been the
  behaviour since lock v0.8 (`a6ba3a3`); no lock specifies the number of bins. The locked runs are unchanged and the
  manuscript now describes three bins. A four-quartile variant (`--bins 4`) is reported as a sensitivity check
  (`results/LOCKED_VARIANTS.md`, `results/VARIANTS.md`).

Judge prompt changes made before any full run (format only, decided without looking at human labels):
* Arena prompt: final line changed to "Even if both responses are similar, you must pick one. Answer with exactly one
  letter, A or B, and nothing else." after a 100-battle smoke test in which Mistral-7B's first token was mostly " Both".
* MT GEMBA-DA: the assistant turn is pre-filled with "Score: " for both models so that the next token is the number.

Outcomes (reported in the paper whatever they are): see `results/HYPOTHESES.md`.
