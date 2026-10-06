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

Corrections to the lock documents themselves:
* The lock files were written with the date 2026-10-07 in their file names; they were committed on 2026-10-06
  (table above). The files were renamed without the date; their content is unchanged.

Judge prompt changes made before any full run (format only, decided without looking at human labels):
* Arena prompt: final line changed to "Even if both responses are similar, you must pick one. Answer with exactly one
  letter, A or B, and nothing else." after a 100-battle smoke test in which Mistral-7B's first token was mostly " Both".
* MT GEMBA-DA: the assistant turn is pre-filled with "Score: " for both models so that the next token is the number.

Outcomes (reported in the paper whatever they are): see `results/HYPOTHESES.md`.
