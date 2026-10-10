#!/usr/bin/env bash
# Held-out year: every two-system decision among the top-6 systems of WMT23 en-de / zh-en (15 pairs x 2 LPs) with every
# WMT23 submitted metric (refA / src variants; mtme_import23.py) and chrF, the same audit parameters, eps and coefficient
# arms as the WMT22 decisions (RUN_PAIRS_MTME.sh): pilot 50, eps 0.01 0.02, --extra --oracle.
# usage: [DRAWS=300] [TAG=pair23] [PROCS=128] RUN_PAIRS_23.sh
set -euo pipefail; cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
DRAWS=${DRAWS:-300}; TAG=${TAG:-pair23}
for lp in ${LPS:-ende23 zhen23}; do
  SYS=$(python3 -c "
import sys; sys.path.insert(0,'.'); from mt_common import load_pool
d=load_pool('$lp'); print(' '.join(d.groupby('system').u.mean().sort_values(ascending=False).index[:6]))")
  read -ra S <<< "$SYS"
  J=$(grep "^$lp" "${JV_DATA:-../data}/mt/MTME_METRICS23.txt" | cut -f2)
  PAIRS=""; for ((i=0;i<6;i++)); do for ((j=i+1;j<6;j++)); do PAIRS="$PAIRS $i$j"; done; done
  [ "${REV:-0}" = 1 ] && PAIRS=$(echo $PAIRS | tr ' ' '\n' | tac | tr '\n' ' ')     # REV=1: a second runner works from the other end
  for ij in $PAIRS; do i=${ij:0:1}; j=${ij:1:1}
    stem=../results/mt/mt_${lp}_m2_p50_${TAG}${i}${j}
    [ -f ${stem}_info.json ] && continue
    python3 110_unit_audit.py mt $lp --menu "${S[$i]}" "${S[$j]}" --judges $J chrf --pilot 50 --eps 0.01 0.02 --draws $DRAWS --extra --oracle --procs ${PROCS:-128} --tag "_${TAG}${i}${j}" > /dev/null
  done
done
