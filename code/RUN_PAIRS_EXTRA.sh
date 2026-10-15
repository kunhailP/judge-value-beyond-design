#!/usr/bin/env bash
# Exploratory (post-lock, pre-submission): the 30 two-system MT decisions under variations of the audit's fixed
# parameters, with the same evaluators, menus, eps and coefficient rules as RUN_PAIRS_MTME.sh.
#   PILOT=10|25|50   pilot size (paper: 50)
#   DRAWS=300|2000   simulated audits per cell (paper: 300)
#   BINS=3|4         positive dissimilarity bins of the weighted design (3 = the locked runs; 4 = quartiles)
#   TAG=<suffix>     output tag: files results/mt/mt_<lp>_m2_p<PILOT>_pairmtme<TAG><ij>_*
#   JUDGES="..."     evaluators (default: the 31 mt-metrics-eval variants of the locked v1.1 run, plus comet22, qwen3_8b
#                    and mistral_7b when their judge files exist under $JV_DATA/mt/<lp>/)
# usage: PILOT=25 DRAWS=300 BINS=3 TAG=p25 [LPS="ende zhen"] [PROCS=120] RUN_PAIRS_EXTRA.sh
set -euo pipefail; cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
PILOT=${PILOT:-50}; DRAWS=${DRAWS:-300}; BINS=${BINS:-3}; TAG=${TAG:?set TAG}
for lp in ${LPS:-ende zhen}; do
  SYS=$(python3 -c "
import sys; sys.path.insert(0,'.'); from mt_common import load_pool
d=load_pool('$lp'); d=d[~d.system.str.endswith('_bestmbr')]; print(' '.join(d.groupby('system').u.mean().sort_values(ascending=False).index[:6]))")
  read -ra S <<< "$SYS"
  MTJ=$(python3 -c "import json;print(' '.join(json.load(open('../results/mt/mt_${lp}_m4_p50_mtme_info.json'))['judges']))")
  OWN=""; for j in comet22 qwen3_8b mistral_7b; do [ -f "${JV_DATA:-../data}/mt/$lp/judge_$j.parquet" ] && OWN="$OWN $j"; done
  J=${JUDGES:-"$MTJ$OWN"}
  for ((i=0;i<6;i++)); do for ((j=i+1;j<6;j++)); do
    stem=../results/mt/mt_${lp}_m2_p${PILOT}_pairmtme${TAG}${i}${j}
    [ -f ${stem}_info.json ] && continue
    python3 110_unit_audit.py mt $lp --menu "${S[$i]}" "${S[$j]}" --judges $J --pilot $PILOT --eps 0.01 0.02 --draws $DRAWS --bins $BINS --extra --oracle --procs ${PROCS:-120} --tag "_pairmtme${TAG}${i}${j}"
    [ "${SUMMARIZE:-0}" = 1 ] && python3 111_summarize.py $stem --boot 100 > ${stem}_summary.txt || true
  done; done
done
