#!/usr/bin/env bash
# Locked runs of PROSPECTIVE_LOCK_v0.8 (MT + Arena). Usage: RUN_LOCKED.sh {mt|arena|mt_pairs|boundary}
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1
MTJ="comet22 qwen3_8b mistral_7b inv_comet22 chrf"
ARJ="qwen3_8b mistral_7b longer inv_qwen3_8b"
case "$1" in
  exploratory) ;;
  arena_v09) ;;
  mt)
    for lp in ende zhen; do for p in 50 100; do
      python3 110_unit_audit.py mt $lp --judges $MTJ --pilot $p --procs 128
      python3 111_summarize.py ../results/mt/mt_${lp}_m4_p${p} --boot 200 > ../results/mt/mt_${lp}_m4_p${p}_summary.txt
    done; done ;;
  mt_pairs)
    for lp in ende zhen; do
      SYS=$(python3 -c "
import sys; sys.path.insert(0,'.'); from mt_common import load_pool
d=load_pool('$lp'); d=d[~d.system.str.endswith('_bestmbr')]; print(' '.join(d.groupby('system').u.mean().sort_values(ascending=False).index[:6]))")
      read -ra S <<< "$SYS"
      for ((i=0;i<6;i++)); do for ((j=i+1;j<6;j++)); do
        python3 110_unit_audit.py mt $lp --menu "${S[$i]}" "${S[$j]}" --judges $MTJ --pilot 50 --eps 0.01 0.02 --procs 128 --tag "_pair${i}${j}"
        python3 111_summarize.py ../results/mt/mt_${lp}_m2_p50_pair${i}${j} --boot 100 > ../results/mt/mt_${lp}_m2_p50_pair${i}${j}_summary.txt
      done; done
    done ;;
  arena)
    for pid in 0 1 2 3 4 5; do for p in 50 25; do
      python3 110_unit_audit.py arena $pid --judges $ARJ --pilot $p --eps 0.02 0.05 --procs 128
      python3 111_summarize.py ../results/arena/arena_${pid}_m2_p${p} --boot 200 > ../results/arena/arena_${pid}_m2_p${p}_summary.txt
    done; done ;;
  boundary)
    for lp in ende zhen; do python3 110_unit_audit.py mt $lp --judges $MTJ --pilot 50 --boundary --procs 128; done
    for pid in 0 1 2 3 4 5; do python3 110_unit_audit.py arena $pid --judges $ARJ --pilot 50 --boundary --procs 128; done ;;
esac
# lock v0.9: close Arena pairs (pair ids 10-15)
if [ "$1" = "arena_v09" ]; then
  for pid in 10 11 12 13 14 15; do for p in 50 25; do
    python3 110_unit_audit.py arena $pid --judges $ARJ --pilot $p --eps 0.02 0.05 0.1 --procs 128
    python3 111_summarize.py ../results/arena/arena_${pid}_m2_p${p} --boot 200 > ../results/arena/arena_${pid}_m2_p${p}_summary.txt
  done; done
  python3 110_unit_audit.py arena 10 --judges $ARJ --pilot 50 --boundary --procs 128 || true
fi
# ---- exploratory (post-lock) runs: oracle lambda, single presentation order, semi-synthetic rho dial
if [ "$1" = "exploratory" ]; then
  for lp in ende zhen; do
    python3 110_unit_audit.py mt $lp --judges comet22 qwen3_8b mistral_7b chrf --pilot 50 --oracle --procs 128 --tag _diag
    python3 111_summarize.py ../results/mt/mt_${lp}_m4_p50_diag --boot 100 > ../results/mt/mt_${lp}_m4_p50_diag_summary.txt
  done
  for pid in 10 11 12 13 14 15; do
    python3 110_unit_audit.py arena $pid --judges qwen3_8b qwen3_8b@o1 qwen3_8b@o2 mistral_7b mistral_7b@o1 mistral_7b@o2 longer --pilot 50 --eps 0.02 0.05 0.1 --oracle --procs 64 --tag _diag
    python3 111_summarize.py ../results/arena/arena_${pid}_m2_p50_diag --boot 100 > ../results/arena/arena_${pid}_m2_p50_diag_summary.txt
  done
  SYN="syn0.1 syn0.2 syn0.3 syn0.4 syn0.5 syn0.6 syn0.7 syn0.8 syn0.9"
  for lp in ende zhen; do for p in 50 100; do
    python3 110_unit_audit.py mt $lp --judges $SYN --pilot $p --eps 0.01 0.02 --procs 96 --tag _syn
    python3 111_summarize.py ../results/mt/mt_${lp}_m4_p${p}_syn --boot 50 > ../results/mt/mt_${lp}_m4_p${p}_syn_summary.txt
  done; done
  for pid in 10 13 15; do
    python3 110_unit_audit.py arena $pid --judges $SYN --pilot 50 --eps 0.05 0.1 --procs 96 --tag _syn
    python3 111_summarize.py ../results/arena/arena_${pid}_m2_p50_syn --boot 50 > ../results/arena/arena_${pid}_m2_p50_syn_summary.txt
  done
fi
