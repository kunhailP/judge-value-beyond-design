# Auditor strategies (results/mt/mt_*23_m2_p50_boundary_pair23b??; design=dedup, fixed=mtme_COMET-refA, mode=cvq, stat=rho, r0=0.2, s0=-1.0)

Cells: 30; informative (1 - P/J50_uniform >= 0.0): 0 ({})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |                   nan |             nan |                     nan |                      nan |                          0 |
| S3_select            |                   nan |             nan |                     nan |                      nan |                          0 |
| S4_select_or_abstain |                   nan |             nan |                     nan |                      nan |                          0 |
| best_posthoc         |                   nan |             nan |                     nan |                      nan |                          0 |
| mean_judge           |                   nan |             nan |                     nan |                      nan |                          0 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |   max |
|:---------------------|--------:|------:|
| S1_design            |     nan |   nan |
| S2_fixed             |     nan |   nan |
| S3_select            |     nan |   nan |
| S4_select_or_abstain |     nan |   nan |

Abstention share (S4), mean over informative cells: nan

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in nan of informative cells

## Per informative cell

| lp   | pair   | eps   | N   | pilot_cost   | J_uniform   | save_design   | excess_S2_fixed   | excess_S3_select   | excess_S4_select_or_abstain   | abstain_share   | excess_best_posthoc   | best_posthoc   | excess_mean_judge   | p_best_vs_noise   |
|------|--------|-------|-----|--------------|-------------|---------------|-------------------|--------------------|-------------------------------|-----------------|-----------------------|----------------|---------------------|-------------------|

## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)

| judge   | rho   | HES_pilot   | HES_refit   | cells   |
|---------|-------|-------------|-------------|---------|