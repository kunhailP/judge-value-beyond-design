#!/usr/bin/env bash
# Exploratory (post-lock): the 31 mt-metrics-eval variants + COMET-22 and the two GEMBA judges on every two-system
# decision among the top-6 systems of each language pair (15 pairs x 2 LPs), with refit / cross-fit / oracle arms.
# usage: [LPS="ende zhen"] [PROCS=120] [IDENT=pick] RUN_PAIRS_MTME.sh
# IDENT=pick: identical strings share one random rating instead of their mean (sensitivity; tag _pairmtmepick<ij>)
set -euo pipefail; cd "$(dirname "$0")"
for lp in ${LPS:-ende zhen}; do
  SYS=$(python3 -c "
import sys; sys.path.insert(0,'.'); from mt_common import load_pool
d=load_pool('$lp'); d=d[~d.system.str.endswith('_bestmbr')]; print(' '.join(d.groupby('system').u.mean().sort_values(ascending=False).index[:6]))")
  read -ra S <<< "$SYS"
  MTJ=$(python3 -c "import json;print(' '.join(json.load(open('../results/mt/mt_${lp}_m4_p50_mtme_info.json'))['judges']))")
  for ((i=0;i<6;i++)); do for ((j=i+1;j<6;j++)); do
    V=${IDENT:+$IDENT}; [ "${IDENT:-mean}" = mean ] && V=""
    stem=../results/mt/mt_${lp}_m2_p50_pairmtme${V}${i}${j}
    [ -f ${stem}_summary.csv ] && continue
    [ "${SUMMARIZE:-1}" = 0 ] && [ -f ${stem}_info.json ] && continue
    if [ ! -f ${stem}_info.json ]; then
    python3 110_unit_audit.py mt $lp --menu "${S[$i]}" "${S[$j]}" --judges $MTJ comet22 qwen3_8b mistral_7b --pilot 50 --eps 0.01 0.02 --extra --oracle --procs ${PROCS:-120} --ident ${IDENT:-mean} --tag "_pairmtme${V}${i}${j}"; fi
    [ "${SUMMARIZE:-1}" = 1 ] && python3 111_summarize.py $stem --boot 100 > ${stem}_summary.txt || true
  done; done
done
