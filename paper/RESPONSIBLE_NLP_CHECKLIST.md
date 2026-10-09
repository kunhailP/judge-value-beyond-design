# ARR Responsible NLP Research checklist — answers (to be copied into the submission form)

## A. For every submission
* **A1 Limitations.** Yes — section "Limitations" (after the conclusion).
* **A2 Potential risks.** Yes, briefly in Limitations: the paper argues that correlation-based claims of evaluator savings can
  overstate what an audit obtains; misreading its negative results as "automatic evaluators are useless" would be a risk,
  which is why the text states the conditions (close decisions, 20–50-item pilots, ρ ≤ 0.38) under which they hold.
  No new model, dataset or system is released that could be misused.

## B. Did you use or create scientific artifacts? — Yes
* **B1 Cited creators.** Yes — §3 cites WMT22 MQM (Freitag et al. 2021), the WMT22 metrics task and mt-metrics-eval
  (Freitag et al. 2022), COMET-22, GEMBA, Qwen3, Mistral-7B, UMBRELA, LMArena / Chatbot Arena, ANTIQUE, CAsT 2019,
  DBpedia-Entity, TREC DL 2021–23, NeuCLIRBench.
* **B2 Licences.** google/wmt-mqm-human-evaluation: Apache 2.0. mt-metrics-eval: Apache 2.0. lmarena-ai/arena-human-preference-55k:
  Apache 2.0. Qwen3-8B, Qwen3-Reranker-0.6B, Mistral-7B-Instruct-v0.3, Unbabel/wmt22-comet-da: Apache 2.0. Retrieval
  collections: the respective NIST/TREC and dataset terms (used only through relevance judgments, not redistributed).
  Our code: MIT; our result files: CC BY 4.0 (stated in the repository README).
* **B3 Intended use.** Yes — all artifacts are research benchmarks used for evaluation research, consistent with their
  intended use; we release only derived scores and per-audit records, not the source texts.
* **B4 PII / offensive content.** The LMArena prompts are user-written and may contain personal or offensive content;
  we use the public release as distributed (de-identified by its creators), pass it only to local judge models, and do not
  redistribute the texts. MT and retrieval data are published benchmarks.
* **B5 Documentation of artifacts.** Yes — §3 and the repository README (languages: English, German, Chinese; domains:
  news, conversation, e-commerce, social for WMT22; open-ended chat; web, conversational and non-factoid QA retrieval).
* **B6 Statistics.** Yes — §3: 1,315 / 1,875 MQM segments, 31 metric variants, 6 Arena pairs with 311–472 battles,
  retrieval collections with 159–399 queries; pilots of 20/50 items; 300 simulated audits per budget.

## C. Computational experiments — Yes
* **C1 Parameters and compute.** Judges: Qwen3-8B (8B), Mistral-7B (7B), Qwen3-Reranker (0.6B), COMET-22 (~0.6B), run with
  vLLM 0.10.2 / unbabel-comet 2.2.7 on one RTX 3090 (24 GB): about 2 GPU-hours in total. Audits: CPU only, about 20
  CPU-hours on a 256-core machine for the locked and exploratory runs, plus about 500 CPU-hours for the pre-submission
  variants (2,000 audits per cell, pilots of 25 and 10, four bins; `code/RUN_PAIRS_EXTRA.sh`).
* **C2 Experimental setup and hyperparameters.** Yes — §2–§3 and the locks: α = 0.10, ε grids, pilots, budget grids, seeds,
  prompts (repository `code/arena_prompt.py`, `code/mt_prompt.py`), temperature 0, the λ ≥ 0 rule.
* **C3 Descriptive statistics.** Yes — paired-bootstrap 95% intervals over 300 audits per cell; Monte-Carlo checks of the
  bound's calibration (§8); metric-level bootstrap for the estimation tax.
* **C4 Existing packages.** Yes — vLLM, unbabel-comet, sacrebleu (chrF), NumPy/SciPy/pandas; versions in `requirements.txt`.

## D. Human annotators / participants — No new annotation
All human judgments are existing released labels (WMT22 MQM, LMArena votes, TREC/benchmark relevance judgments).
D1–D5: not applicable.

## E. AI assistants in research or writing — Yes
AI assistants were used for coding assistance and language editing. All analyses were run, checked against the
committed results, and the text verified by the authors.
