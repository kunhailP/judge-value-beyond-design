#!/usr/bin/env bash
# Exploratory (post-lock): Arena v0.9 close pairs with refit / cross-fit / oracle arms and coverage (tag _robust2).
set -euo pipefail; cd "$(dirname "$0")"
for p in 10 11 12 13 14 15; do
  python3 110_unit_audit.py arena $p --judges qwen3_8b mistral_7b longer --pilot 50 --eps 0.05 0.1 --extra --oracle --tag _robust2 --procs ${PROCS:-128}
  python3 111_summarize.py ../results/arena/arena_${p}_m2_p50_robust2 > /dev/null
done
