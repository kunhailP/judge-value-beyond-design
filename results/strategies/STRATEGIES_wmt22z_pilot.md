# Auditor strategies (results/mt/mt_*_m2_p50_pairmtmez??; design=dedup, fixed=mtme_COMET-22-refA, mode=cvl, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 33 ({'zhen': 29, 'ende': 4})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0224 |         -0.0142 |                  0.7576 |                   0.0909 |                   232.951  |
| S3_select            |                0.023  |          0.0191 |                  0.2727 |                   0.4545 |                  -109.822  |
| S4_select_or_abstain |                0.0222 |          0.0224 |                  0.2727 |                   0.5455 |                  -107.391  |
| best_posthoc         |               -0.0616 |         -0.0535 |                  1      |                   0      |                   661.574  |
| mean_judge           |                0.0014 |         -0.0024 |                  0.6061 |                   0.1515 |                    17.0092 |

### ende: 4 cells; median design saving vs uniform 0.155

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0899 |  -0.0686 |            0.75 |
| S3_select            |        0.0484 |   0.0609 |            0    |
| S4_select_or_abstain |        0.0484 |   0.0609 |            0    |
| best_posthoc         |       -0.1175 |  -0.109  |            1    |
| mean_judge           |        0.0166 |   0.0223 |            0.5  |

### zhen: 29 cells; median design saving vs uniform 0.047

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0131 |  -0.0142 |          0.7586 |
| S3_select            |        0.0195 |   0.0138 |          0.3103 |
| S4_select_or_abstain |        0.0186 |   0.0205 |          0.3103 |
| best_posthoc         |       -0.0539 |  -0.0535 |          1      |
| mean_judge           |       -0.0008 |  -0.0024 |          0.6207 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0025 | 0.0267 |
| S2_fixed             |  0.0027 | 0.0267 |
| S3_select            |  0.0027 | 0.0267 |
| S4_select_or_abstain |  0.0026 | 0.0267 |

Abstention share (S4), mean over informative cells: 0.039

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.03 of informative cells

## Per informative cell

| lp   |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                   |   excess_mean_judge |   p_best_vs_noise |
|:-----|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:-------------------------------|--------------------:|------------------:|
| ende |     12 |  0.01 | 1315 |       88.29  |     196.953 |         0.091 |            -0.131 |              0.058 |                         0.058 |           0.017 |                -0.199 | mtme_metricx_xl_DA_2019-refA   |              -0.035 |             0.44  |
| ende |     34 |  0.01 | 1315 |       86.82  |     230.937 |         0.182 |            -0.236 |              0.066 |                         0.066 |           0.013 |                -0.236 | mtme_COMET-22-refA             |              -0.005 |             0.385 |
| ende |     35 |  0.01 | 1315 |       90.08  |     171.275 |         0.127 |             0.014 |              0.064 |                         0.064 |           0.013 |                -0.016 | mtme_metricx_xl_MQM_2020-refA  |               0.057 |             0.845 |
| ende |     45 |  0.01 | 1315 |       89.893 |     203.627 |         0.272 |            -0.006 |              0.006 |                         0.006 |           0.02  |                -0.019 | mtme_metricx_xxl_MQM_2020-refA |               0.05  |             0.995 |
| zhen |     01 |  0.01 | 1875 |       97.63  |     527.655 |        -0.002 |            -0.056 |             -0.02  |                        -0.023 |           0.037 |                -0.056 | mtme_COMET-22-refA             |              -0.012 |             0.595 |
| zhen |     01 |  0.02 | 1875 |       97.63  |     253.229 |         0.006 |             0.024 |              0.039 |                         0.039 |           0.037 |                -0.017 | mtme_UniTE-src-src             |               0.002 |             0.97  |
| zhen |     02 |  0.01 | 1875 |       96.44  |     465.914 |         0.007 |            -0.014 |              0.001 |                         0.001 |           0.017 |                -0.078 | mtme_UniTE-refA                |              -0.01  |             0.125 |
| zhen |     02 |  0.02 | 1875 |       96.44  |     220.687 |         0.065 |            -0.01  |              0.124 |                         0.124 |           0.017 |                -0.021 | mtme_BLEU-refA                 |               0.015 |             0.875 |
| zhen |     03 |  0.01 | 1875 |       96.723 |     316.963 |         0.024 |            -0.018 |              0.113 |                         0.113 |           0.043 |                -0.054 | mtme_metricx_xxl_MQM_2020-refA |               0.005 |             0.365 |
| zhen |     03 |  0.02 | 1875 |       96.723 |     205.966 |         0.05  |            -0.017 |              0.051 |                         0.048 |           0.043 |                -0.017 | mtme_COMET-22-refA             |               0.024 |             0.525 |
| zhen |     04 |  0.01 | 1875 |       97.653 |     276.501 |         0.019 |            -0.04  |              0.02  |                         0.02  |           0.02  |                -0.093 | mtme_metricx_xxl_MQM_2020-refA |              -0.008 |             0.015 |
| zhen |     04 |  0.02 | 1875 |       97.653 |     197.985 |         0.177 |             0.102 |              0.195 |                         0.149 |           0.02  |                -0.027 | mtme_COMET-QE-src              |               0.032 |             0.995 |
| zhen |     05 |  0.01 | 1875 |       98.767 |     196.007 |         0.031 |            -0.021 |              0.023 |                         0.023 |           0.007 |                -0.077 | mtme_MS-COMET-QE-22-src        |               0.017 |             0.265 |
| zhen |     12 |  0.01 | 1875 |       95.98  |     687.743 |         0.202 |             0.017 |              0.047 |                         0.048 |           0.053 |                -0.035 | mtme_UniTE-src-src             |               0.018 |             0.55  |
| zhen |     12 |  0.02 | 1875 |       95.98  |     298.223 |         0.141 |             0.017 |              0.073 |                         0.06  |           0.053 |                -0.078 | mtme_MATESE-QE-src             |              -0.005 |             0.38  |
| zhen |     13 |  0.01 | 1875 |       97.137 |     647.402 |         0.082 |            -0.035 |              0.025 |                         0.026 |           0.023 |                -0.064 | mtme_UniTE-ref-refA            |              -0.016 |             0.355 |
| zhen |     13 |  0.02 | 1875 |       97.137 |     243.932 |         0.047 |            -0.027 |             -0.012 |                        -0.012 |           0.023 |                -0.065 | mtme_UniTE-ref-refA            |              -0     |             0.23  |
| zhen |     14 |  0.01 | 1875 |       96.323 |     537.148 |         0.046 |            -0.005 |              0.04  |                         0.043 |           0.04  |                -0.039 | mtme_metricx_xxl_DA_2019-refA  |              -0.001 |             0.435 |
| zhen |     14 |  0.02 | 1875 |       96.323 |     262.573 |         0.079 |            -0.007 |              0.012 |                         0.025 |           0.04  |                -0.041 | mtme_MATESE-QE-src             |               0.001 |             0.62  |
| zhen |     15 |  0.01 | 1875 |       97.417 |     321.191 |         0.083 |            -0.056 |              0.019 |                         0.019 |           0.023 |                -0.072 | mtme_metricx_xl_MQM_2020-refA  |              -0.014 |             0.3   |
| zhen |     15 |  0.02 | 1875 |       97.417 |     187.354 |         0.022 |            -0.033 |              0.014 |                         0.023 |           0.023 |                -0.039 | mtme_MEE2-refA                 |              -0.006 |             0.745 |
| zhen |     23 |  0.01 | 1875 |       91.96  |     606.453 |         0.095 |             0.04  |              0.022 |                         0.022 |           0.08  |                -0.017 | mtme_COMET-QE-src              |               0.033 |             0.715 |
| zhen |     23 |  0.02 | 1875 |       91.96  |     280.441 |         0.111 |             0.015 |              0.012 |                         0.01  |           0.08  |                -0.056 | mtme_MATESE-QE-src             |               0     |             0.16  |
| zhen |     24 |  0.01 | 1875 |       95.347 |     622.857 |         0.103 |            -0.094 |             -0.046 |                        -0.046 |           0.05  |                -0.127 | mtme_metricx_xxl_MQM_2020-refA |              -0.022 |             0.325 |
| zhen |     24 |  0.02 | 1875 |       95.347 |     271.88  |         0.055 |            -0.001 |             -0.027 |                        -0.026 |           0.05  |                -0.069 | mtme_metricx_xxl_DA_2019-refA  |              -0.022 |             0.335 |
| zhen |     25 |  0.01 | 1875 |       97.27  |     360.83  |         0.052 |            -0.064 |             -0.003 |                        -0.002 |           0.077 |                -0.064 | mtme_COMET-22-refA             |              -0.009 |             0.23  |
| zhen |     25 |  0.02 | 1875 |       97.27  |     208.539 |         0.047 |            -0.004 |              0.023 |                         0.031 |           0.077 |                -0.036 | mtme_SEScore-refA              |              -0.003 |             0.42  |
| zhen |     34 |  0.01 | 1875 |       96.093 |     697.542 |         0.062 |            -0.002 |             -0.101 |                        -0.101 |           0.07  |                -0.089 | mtme_MS-COMET-QE-22-src        |              -0.002 |             0.065 |
| zhen |     34 |  0.02 | 1875 |       96.093 |     262.343 |         0.041 |             0.014 |              0.014 |                         0.021 |           0.07  |                -0.034 | mtme_HWTSC-TLM-src             |               0.014 |             0.215 |
| zhen |     35 |  0.01 | 1875 |       97.823 |     447.917 |        -0.017 |            -0.061 |             -0.089 |                        -0.089 |           0.05  |                -0.083 | mtme_UniTE-src-src             |              -0.038 |             0.665 |
| zhen |     35 |  0.02 | 1875 |       97.823 |     223.571 |         0.026 |            -0.026 |              0.013 |                         0.013 |           0.05  |                -0.029 | mtme_YiSi-1-refA               |              -0.002 |             0.665 |
| zhen |     45 |  0.01 | 1875 |       97.753 |     585.428 |         0.023 |            -0.003 |             -0.015 |                        -0.015 |           0.03  |                -0.04  | mtme_Cross-QE-src              |              -0.006 |             0.805 |
| zhen |     45 |  0.02 | 1875 |       97.753 |     282     |         0.038 |            -0.018 |             -0.002 |                        -0.002 |           0.03  |                -0.046 | mtme_metricx_xxl_DA_2019-refA  |              -0.006 |             0.475 |

## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)

| judge                          |    rho |   HES_pilot |   HES_refit |   cells |
|:-------------------------------|-------:|------------:|------------:|--------:|
| mtme_metricx_xxl_MQM_2020-refA |  0.275 |       0.018 |       0.051 |      33 |
| mtme_metricx_xl_MQM_2020-refA  |  0.275 |       0.022 |       0.048 |      33 |
| mtme_UniTE-ref-refA            |  0.256 |       0.019 |       0.035 |      33 |
| mtme_COMET-22-refA             |  0.251 |       0.022 |       0.044 |      33 |
| mtme_UniTE-refA                |  0.249 |       0.012 |       0.035 |      33 |
| mtme_metricx_xxl_DA_2019-refA  |  0.239 |       0.015 |       0.034 |      33 |
| mtme_metricx_xl_DA_2019-refA   |  0.235 |       0.023 |       0.036 |      33 |
| mtme_UniTE-src-src             |  0.22  |       0.004 |       0.029 |      33 |
| mtme_COMETKiwi-src             |  0.212 |       0.003 |       0.027 |      33 |
| mtme_BLEURT-20-refA            |  0.208 |       0.008 |       0.021 |      33 |
| mtme_Cross-QE-src              |  0.202 |      -0.004 |       0.029 |      33 |
| mtme_MATESE-refA               |  0.189 |      -0.015 |       0.031 |      33 |
| mtme_MS-COMET-22-refA          |  0.179 |       0.002 |       0.023 |      33 |
| mtme_COMET-20-refA             |  0.174 |      -0     |       0.015 |      33 |
| mtme_COMET-QE-src              |  0.17  |       0.001 |       0.019 |      33 |
| mtme_BERTScore-refA            |  0.15  |      -0.004 |       0.016 |      33 |
| mtme_YiSi-1-refA               |  0.15  |      -0.008 |       0.017 |      33 |
| mtme_MS-COMET-QE-22-src        |  0.149 |      -0.007 |       0.011 |      33 |
| mtme_MATESE-QE-src             |  0.148 |       0.001 |       0.025 |      33 |
| mtme_SEScore-refA              |  0.145 |      -0.007 |       0.018 |      33 |
| mtme_MEE4-refA                 |  0.128 |      -0.003 |       0.008 |      33 |
| mtme_MEE2-refA                 |  0.104 |      -0.016 |       0.009 |      33 |
| mtme_chrF-refA                 |  0.097 |      -0.011 |       0.003 |      33 |
| mtme_f101spBLEU-refA           |  0.089 |      -0.016 |       0.005 |      33 |
| mtme_f200spBLEU-refA           |  0.088 |      -0.007 |       0.009 |      33 |
| mtme_MEE-refA                  |  0.088 |      -0.012 |       0.006 |      33 |
| mtme_HWTSC-Teacher-Sim-src     |  0.077 |      -0.021 |       0.003 |      33 |
| mtme_BLEU-refA                 |  0.068 |      -0.01  |       0.002 |      33 |
| mtme_KG-BERTScore-src          |  0.06  |      -0.011 |       0.003 |      33 |
| mtme_HWTSC-TLM-src             |  0.051 |      -0.026 |      -0.002 |      33 |
| mtme_REUSE-src                 | -0.009 |      -0.014 |      -0     |      33 |