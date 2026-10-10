# Auditor strategies (results/mt/mt_*23_m2_p50_pair23??; design=dedup, fixed=mtme_COMET-refA, mode=cvq, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 26 ({'ende23': 16, 'zhen23': 10})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0313 |         -0.0309 |                  0.9231 |                   0      |                    156.609 |
| S3_select            |               -0.0328 |         -0.0258 |                  0.8462 |                   0.0385 |                    155.01  |
| S4_select_or_abstain |               -0.0305 |         -0.0234 |                  0.8462 |                   0.0385 |                    142.913 |
| best_posthoc         |               -0.079  |         -0.07   |                  1      |                   0      |                    422.323 |
| mean_judge           |               -0.0254 |         -0.0236 |                  0.8846 |                   0      |                    126.495 |

### ende23: 16 cells; median design saving vs uniform 0.028

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0317 |  -0.0337 |          0.9375 |
| S3_select            |       -0.0372 |  -0.0303 |          0.8125 |
| S4_select_or_abstain |       -0.0348 |  -0.0248 |          0.8125 |
| best_posthoc         |       -0.0878 |  -0.0834 |          1      |
| mean_judge           |       -0.0272 |  -0.0262 |          0.875  |

### zhen23: 10 cells; median design saving vs uniform 0.053

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0306 |  -0.0267 |             0.9 |
| S3_select            |       -0.0259 |  -0.0258 |             0.9 |
| S4_select_or_abstain |       -0.0236 |  -0.0209 |             0.9 |
| best_posthoc         |       -0.0649 |  -0.0592 |             1   |
| mean_judge           |       -0.0225 |  -0.0212 |             0.9 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0077 | 0.0267 |
| S2_fixed             |  0.0064 | 0.0267 |
| S3_select            |  0.0071 | 0.0267 |
| S4_select_or_abstain |  0.0071 | 0.0267 |

Abstention share (S4), mean over informative cells: 0.017

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.00 of informative cells

## Per informative cell

| lp     |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                |   excess_mean_judge |   p_best_vs_noise |
|:-------|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:----------------------------|--------------------:|------------------:|
| ende23 |     01 |  0.01 |  460 |       97.16  |     551.616 |         0.039 |            -0.033 |             -0.052 |                        -0.052 |           0.023 |                -0.089 | mtme_XCOMET-XL-refA         |              -0.027 |             0.09  |
| ende23 |     01 |  0.02 |  460 |       97.16  |     313.593 |         0.027 |            -0.04  |              0.006 |                         0.006 |           0.023 |                -0.207 | mtme_XCOMET-XXL-refA        |              -0.042 |             0.21  |
| ende23 |     02 |  0.01 |  460 |       97.877 |     190.768 |         0.02  |            -0.013 |              0.003 |                         0.003 |           0     |                -0.151 | mtme_MetricX-23-refA        |              -0.022 |             0.345 |
| ende23 |     02 |  0.02 |  460 |       97.877 |     153.55  |         0.001 |            -0.021 |             -0.012 |                        -0.012 |           0     |                -0.036 | mtme_XCOMET-Ensemble-refA   |              -0.016 |             0.24  |
| ende23 |     12 |  0.01 |  460 |       96.257 |     202.765 |         0.048 |            -0.054 |             -0.036 |                        -0.036 |           0.003 |                -0.078 | mtme_MetricX-23-QE-c-src    |              -0.033 |             0.185 |
| ende23 |     12 |  0.02 |  460 |       96.257 |     168.835 |         0.027 |            -0.014 |             -0.04  |                        -0.034 |           0.003 |                -0.069 | mtme_MetricX-23-QE-c-src    |              -0.025 |             0.295 |
| ende23 |     23 |  0.01 |  460 |       94.783 |     227.685 |         0.096 |            -0.025 |              0     |                         0.007 |           0.013 |                -0.035 | mtme_mbr-metricx-qe-src     |               0.003 |             0.575 |
| ende23 |     23 |  0.02 |  460 |       94.783 |     162.977 |         0.062 |            -0.015 |             -0.008 |                        -0.008 |           0.013 |                -0.025 | mtme_XCOMET-XXL-refA        |              -0.01  |             0.5   |
| ende23 |     24 |  0.01 |  460 |       94.597 |     191.606 |         0.065 |            -0.073 |             -0.089 |                        -0.089 |           0.007 |                -0.12  | mtme_MetricX-23-QE-c-src    |              -0.062 |             0.47  |
| ende23 |     24 |  0.02 |  460 |       94.597 |     142.975 |         0.028 |            -0.036 |             -0.022 |                        -0.022 |           0.007 |                -0.058 | mtme_XCOMET-XXL-refA        |              -0.016 |             0.49  |
| ende23 |     34 |  0.01 |  460 |       94.673 |     536.55  |         0.151 |             0.005 |             -0.005 |                        -0.002 |           0.09  |                -0.031 | mtme_cometoid22-wmt21-src   |               0.003 |             0.11  |
| ende23 |     34 |  0.02 |  460 |       94.673 |     268.329 |        -0.001 |            -0.035 |             -0.043 |                        -0.028 |           0.09  |                -0.062 | mtme_MetricX-23-QE-c-src    |              -0.035 |             0.5   |
| ende23 |     35 |  0.01 |  460 |       97.663 |     189.156 |         0.008 |            -0.037 |             -0.071 |                        -0.071 |           0.02  |                -0.091 | mtme_MetricX-23-b-refA      |              -0.031 |             0.565 |
| ende23 |     35 |  0.02 |  460 |       97.663 |     151.792 |         0.012 |            -0.029 |             -0.025 |                        -0.019 |           0.02  |                -0.097 | mtme_XCOMET-XXL-refA        |              -0.019 |             0.27  |
| ende23 |     45 |  0.01 |  460 |       97.03  |     200.781 |         0.042 |            -0.048 |             -0.09  |                        -0.09  |           0.003 |                -0.111 | mtme_XCOMET-XXL-refA        |              -0.041 |             0.215 |
| ende23 |     45 |  0.02 |  460 |       97.03  |     152.144 |         0.007 |            -0.04  |             -0.111 |                        -0.111 |           0.003 |                -0.146 | mtme_XCOMET-XXL-refA        |              -0.061 |             0.205 |
| zhen23 |     01 |  0.01 | 1177 |       95.787 |     311.904 |         0.116 |             0.002 |              0.073 |                         0.073 |           0.013 |                -0.035 | mtme_MetricX-23-b-refA      |               0.016 |             0.725 |
| zhen23 |     01 |  0.02 | 1177 |       95.787 |     146.222 |         0.024 |            -0.002 |             -0.009 |                        -0.004 |           0.013 |                -0.027 | mtme_XCOMET-QE-Ensemble-src |              -0.005 |             0.745 |
| zhen23 |     24 |  0.01 | 1177 |       64.983 |     178.174 |         0.411 |            -0.018 |             -0.042 |                        -0.042 |           0.013 |                -0.061 | mtme_XCOMET-XXL-refA        |              -0.021 |             0.45  |
| zhen23 |     25 |  0.01 | 1177 |       96.087 |     218.099 |         0.05  |            -0.024 |             -0.026 |                        -0.026 |           0.003 |                -0.047 | mtme_GEMBA-MQM-src          |              -0.017 |             0.7   |
| zhen23 |     25 |  0.02 | 1177 |       96.087 |     149.761 |         0.011 |            -0.043 |             -0.065 |                        -0.065 |           0.003 |                -0.097 | mtme_MetricX-23-c-refA      |              -0.043 |             0.66  |
| zhen23 |     34 |  0.01 | 1177 |       65.677 |     226.17  |         0.52  |            -0.024 |             -0.029 |                        -0.017 |           0.027 |                -0.071 | mtme_XCOMET-XXL-refA        |              -0.017 |             0.345 |
| zhen23 |     35 |  0.01 | 1177 |       96.147 |     216.66  |         0.05  |            -0.032 |             -0.021 |                        -0.017 |           0.01  |                -0.054 | mtme_docWMT22CometDA-refA   |              -0.022 |             0.325 |
| zhen23 |     35 |  0.02 | 1177 |       96.147 |     157.105 |         0.025 |            -0.03  |             -0.026 |                        -0.025 |           0.01  |                -0.058 | mtme_docWMT22CometDA-refA   |              -0.032 |             0.705 |
| zhen23 |     45 |  0.01 | 1177 |       95.843 |     209.492 |         0.061 |            -0.061 |             -0.008 |                        -0.008 |           0.01  |                -0.093 | mtme_prismRef-refA          |              -0.037 |             0.2   |
| zhen23 |     45 |  0.02 | 1177 |       95.843 |     155.798 |         0.055 |            -0.074 |             -0.106 |                        -0.106 |           0.01  |                -0.106 | mtme_XCOMET-XXL-refA        |              -0.048 |             0.845 |

## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)

| judge                             |   rho |   HES_pilot |   HES_refit |   cells |
|:----------------------------------|------:|------------:|------------:|--------:|
| mtme_MetricX-23-QE-b-src          | 0.356 |       0.013 |       0.046 |      26 |
| mtme_XCOMET-Ensemble-refA         | 0.35  |       0.017 |       0.051 |      26 |
| mtme_MetricX-23-QE-src            | 0.344 |       0.011 |       0.044 |      26 |
| mtme_XCOMET-XXL-refA              | 0.33  |       0.017 |       0.056 |      26 |
| mtme_XCOMET-QE-Ensemble-src       | 0.329 |       0.013 |       0.039 |      26 |
| mtme_MetricX-23-QE-c-src          | 0.318 |       0.023 |       0.05  |      26 |
| mtme_XCOMET-XL-refA               | 0.314 |       0.01  |       0.042 |      26 |
| mtme_MetricX-23-b-refA            | 0.305 |       0.004 |       0.035 |      26 |
| mtme_MetricX-23-refA              | 0.3   |       0.014 |       0.038 |      26 |
| mtme_cometoid22-wmt22-src         | 0.251 |      -0.003 |       0.037 |      26 |
| mtme_cometoid22-wmt21-src         | 0.248 |      -0.008 |       0.03  |      26 |
| mtme_cometoid22-wmt23-src         | 0.246 |      -0.007 |       0.034 |      26 |
| mtme_CometKiwi-XXL-src            | 0.245 |      -0.008 |       0.029 |      26 |
| mtme_CometKiwi-XL-src             | 0.244 |      -0.01  |       0.027 |      26 |
| mtme_mbr-metricx-qe-src           | 0.241 |      -0.001 |       0.025 |      26 |
| mtme_CometKiwi-src                | 0.239 |      -0.005 |       0.028 |      26 |
| mtme_MaTESe-refA                  | 0.236 |       0     |       0.022 |      26 |
| mtme_KG-BERTScore-src             | 0.234 |      -0.003 |       0.027 |      26 |
| mtme_instructscore-refA           | 0.232 |       0.004 |       0.027 |      26 |
| mtme_COMET-refA                   | 0.216 |       0.003 |       0.031 |      26 |
| mtme_BLEURT-20-refA               | 0.207 |       0.002 |       0.029 |      26 |
| mtme_GEMBA-MQM-src                | 0.202 |       0.004 |       0.029 |      26 |
| mtme_MetricX-23-c-refA            | 0.197 |      -0.005 |       0.021 |      26 |
| mtme_MS-COMET-QE-22-src           | 0.187 |      -0.024 |       0.029 |      26 |
| mtme_docWMT22CometDA-refA         | 0.18  |       0.006 |       0.036 |      26 |
| mtme_Calibri-COMET22-QE-src       | 0.174 |       0.002 |       0.017 |      26 |
| mtme_Calibri-COMET22-refA         | 0.169 |      -0.011 |       0.006 |      26 |
| mtme_docWMT22CometKiwiDA-src      | 0.168 |      -0.001 |       0.026 |      26 |
| mtme_sescoreX-refA                | 0.167 |       0.003 |       0.027 |      26 |
| mtme_prismRef-refA                | 0.149 |      -0.008 |       0.017 |      26 |
| mtme_YiSi-1-refA                  | 0.125 |      -0.008 |       0.012 |      26 |
| mtme_BERTscore-refA               | 0.105 |      -0.007 |       0.011 |      26 |
| mtme_mre-score-labse-regular-refA | 0.099 |      -0.005 |       0.017 |      26 |
| mtme_XLsim-refA                   | 0.086 |      -0.004 |       0.011 |      26 |
| mtme_MEE4-refA                    | 0.063 |      -0.005 |       0.008 |      26 |
| mtme_chrF-refA                    | 0.058 |      -0.006 |       0.008 |      26 |
| mtme_tokengram_F-refA             | 0.056 |      -0.002 |       0.01  |      26 |
| mtme_prismSrc-src                 | 0.051 |      -0.007 |       0.007 |      26 |
| mtme_BLEU-refA                    | 0.041 |      -0.007 |       0.007 |      26 |
| mtme_eBLEU-refA                   | 0.04  |      -0.006 |       0.008 |      26 |
| mtme_embed_llama-refA             | 0.036 |      -0.005 |       0.006 |      26 |
| mtme_f200spBLEU-refA              | 0.033 |      -0.006 |       0.007 |      26 |