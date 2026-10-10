# Auditor strategies (results/mt/mt_*23_m2_p50_pair23n??; design=dedup, fixed=mtme_COMET-refA, mode=cvq, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 26 ({'ende23': 16, 'zhen23': 10})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0337 |         -0.0315 |                  1      |                   0      |                    168.778 |
| S3_select            |               -0.0327 |         -0.0316 |                  0.8462 |                   0.0769 |                    160.367 |
| S4_select_or_abstain |               -0.0318 |         -0.0302 |                  0.8462 |                   0.0769 |                    155.262 |
| best_posthoc         |               -0.0704 |         -0.0624 |                  1      |                   0      |                    348.924 |
| mean_judge           |               -0.0276 |         -0.025  |                  1      |                   0      |                    135.396 |

### ende23: 16 cells; median design saving vs uniform 0.036

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0418 |  -0.034  |          1      |
| S3_select            |       -0.0419 |  -0.037  |          0.9375 |
| S4_select_or_abstain |       -0.0406 |  -0.0368 |          0.9375 |
| best_posthoc         |       -0.0712 |  -0.0679 |          1      |
| mean_judge           |       -0.0295 |  -0.0292 |          1      |

### zhen23: 10 cells; median design saving vs uniform 0.041

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0206 |  -0.0177 |             1   |
| S3_select            |       -0.0179 |  -0.0192 |             0.7 |
| S4_select_or_abstain |       -0.0175 |  -0.0187 |             0.7 |
| best_posthoc         |       -0.0693 |  -0.0599 |             1   |
| mean_judge           |       -0.0245 |  -0.0209 |             1   |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0065 | 0.0215 |
| S2_fixed             |  0.0057 | 0.018  |
| S3_select            |  0.0057 | 0.019  |
| S4_select_or_abstain |  0.0057 | 0.019  |

Abstention share (S4), mean over informative cells: 0.016

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.81 of informative cells

## Per informative cell

| lp     |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                |   excess_mean_judge |   p_best_vs_noise |
|:-------|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:----------------------------|--------------------:|------------------:|
| ende23 |     01 |  0.01 |  460 |       97.258 |     560.426 |         0.051 |            -0.03  |             -0.034 |                        -0.034 |           0.022 |                -0.058 | mtme_XCOMET-XL-refA         |              -0.023 |             0     |
| ende23 |     01 |  0.02 |  460 |       97.258 |     286.323 |         0.038 |            -0.032 |             -0.029 |                        -0.027 |           0.022 |                -0.059 | mtme_XCOMET-Ensemble-refA   |              -0.025 |             0.035 |
| ende23 |     02 |  0.01 |  460 |       97.898 |     189.081 |         0.012 |            -0.023 |             -0.023 |                        -0.023 |           0.002 |                -0.072 | mtme_MS-COMET-QE-22-src     |              -0.019 |             0     |
| ende23 |     02 |  0.02 |  460 |       97.898 |     153.841 |         0.003 |            -0.022 |             -0.027 |                        -0.027 |           0.002 |                -0.048 | mtme_MS-COMET-QE-22-src     |              -0.017 |             0     |
| ende23 |     12 |  0.01 |  460 |       96.414 |     207.692 |         0.038 |            -0.053 |             -0.06  |                        -0.058 |           0.005 |                -0.078 | mtme_MetricX-23-QE-src      |              -0.039 |             0     |
| ende23 |     12 |  0.02 |  460 |       96.414 |     168.26  |         0.028 |            -0.097 |             -0.082 |                        -0.079 |           0.005 |                -0.119 | mtme_XCOMET-Ensemble-refA   |              -0.057 |             0.005 |
| ende23 |     23 |  0.01 |  460 |       94.932 |     215.365 |         0.07  |            -0.109 |             -0.061 |                        -0.058 |           0.012 |                -0.118 | mtme_CometKiwi-XXL-src      |              -0.043 |             0.05  |
| ende23 |     23 |  0.02 |  460 |       94.932 |     158.608 |         0.034 |            -0.019 |             -0.013 |                        -0.013 |           0.012 |                -0.034 | mtme_CometKiwi-XXL-src      |              -0.012 |             0.02  |
| ende23 |     24 |  0.01 |  460 |       94.796 |     193.204 |         0.084 |            -0.047 |             -0.04  |                        -0.04  |           0.002 |                -0.064 | mtme_MS-COMET-QE-22-src     |              -0.031 |             0.02  |
| ende23 |     24 |  0.02 |  460 |       94.796 |     148.858 |         0.037 |            -0.036 |             -0.034 |                        -0.034 |           0.002 |                -0.054 | mtme_MS-COMET-QE-22-src     |              -0.027 |             0     |
| ende23 |     34 |  0.01 |  460 |       94.72  |     537.568 |         0.127 |            -0     |              0.006 |                         0.007 |           0.076 |                -0.017 | mtme_Calibri-COMET22-QE-src |              -0.001 |             0.04  |
| ende23 |     34 |  0.02 |  460 |       94.72  |     259.225 |         0.054 |            -0.033 |             -0.015 |                        -0.009 |           0.076 |                -0.047 | mtme_XCOMET-Ensemble-refA   |              -0.02  |             0.005 |
| ende23 |     35 |  0.01 |  460 |       97.72  |     185.875 |         0.026 |            -0.048 |             -0.062 |                        -0.061 |           0.019 |                -0.088 | mtme_MetricX-23-QE-b-src    |              -0.039 |             0.015 |
| ende23 |     35 |  0.02 |  460 |       97.72  |     152.417 |         0.007 |            -0.042 |             -0.057 |                        -0.055 |           0.019 |                -0.082 | mtme_MetricX-23-QE-b-src    |              -0.034 |             0.01  |
| ende23 |     45 |  0.01 |  460 |       97.044 |     188.355 |         0.036 |            -0.049 |             -0.075 |                        -0.075 |           0.009 |                -0.095 | mtme_XCOMET-Ensemble-refA   |              -0.045 |             0     |
| ende23 |     45 |  0.02 |  460 |       97.044 |     152.711 |         0.022 |            -0.031 |             -0.066 |                        -0.066 |           0.009 |                -0.107 | mtme_XCOMET-XXL-refA        |              -0.041 |             0.01  |
| zhen23 |     01 |  0.01 | 1177 |       95.981 |     294.778 |         0.099 |            -0     |              0.041 |                         0.039 |           0.016 |                -0.033 | mtme_XCOMET-XXL-refA        |              -0.006 |             0.19  |
| zhen23 |     01 |  0.02 | 1177 |       95.981 |     150.217 |         0.04  |            -0.002 |              0.02  |                         0.023 |           0.016 |                -0.04  | mtme_XCOMET-XXL-refA        |              -0.008 |             0.09  |
| zhen23 |     24 |  0.01 | 1177 |       64.878 |     197.953 |         0.489 |            -0.014 |              0.002 |                         0.001 |           0.021 |                -0.047 | mtme_GEMBA-MQM-src          |              -0.019 |             0.1   |
| zhen23 |     25 |  0.01 | 1177 |       96.168 |     208.233 |         0.032 |            -0.041 |             -0.06  |                        -0.06  |           0.008 |                -0.118 | mtme_MetricX-23-QE-b-src    |              -0.045 |             0.005 |
| zhen23 |     25 |  0.02 | 1177 |       96.168 |     140.99  |         0.027 |            -0.02  |             -0.005 |                        -0.003 |           0.008 |                -0.061 | mtme_MetricX-23-QE-b-src    |              -0.016 |             0.015 |
| zhen23 |     34 |  0.01 | 1177 |       65.662 |     218.749 |         0.484 |            -0.012 |             -0.022 |                        -0.02  |           0.013 |                -0.07  | mtme_MetricX-23-QE-src      |              -0.025 |             0.005 |
| zhen23 |     35 |  0.01 | 1177 |       96.206 |     217.129 |         0.039 |            -0.037 |             -0.045 |                        -0.044 |           0.011 |                -0.102 | mtme_MetricX-23-QE-b-src    |              -0.037 |             0     |
| zhen23 |     35 |  0.02 | 1177 |       96.206 |     148.502 |         0.025 |            -0.015 |             -0.021 |                        -0.022 |           0.011 |                -0.059 | mtme_MetricX-23-QE-b-src    |              -0.021 |             0.045 |
| zhen23 |     45 |  0.01 | 1177 |       95.958 |     209.768 |         0.071 |            -0.042 |             -0.071 |                        -0.071 |           0.01  |                -0.106 | mtme_MetricX-23-QE-b-src    |              -0.048 |             0     |
| zhen23 |     45 |  0.02 | 1177 |       95.958 |     139.293 |         0.042 |            -0.022 |             -0.017 |                        -0.017 |           0.01  |                -0.056 | mtme_MetricX-23-QE-b-src    |              -0.02  |             0.05  |

## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)

| judge                             |   rho |   HES_pilot |   HES_refit |   cells |
|:----------------------------------|------:|------------:|------------:|--------:|
| mtme_MetricX-23-QE-b-src          | 0.356 |       0.017 |       0.056 |      26 |
| mtme_XCOMET-Ensemble-refA         | 0.347 |       0.028 |       0.057 |      26 |
| mtme_MetricX-23-QE-src            | 0.342 |       0.016 |       0.05  |      26 |
| mtme_XCOMET-QE-Ensemble-src       | 0.33  |       0.023 |       0.054 |      26 |
| mtme_MetricX-23-QE-c-src          | 0.323 |       0.018 |       0.049 |      26 |
| mtme_XCOMET-XXL-refA              | 0.322 |       0.023 |       0.054 |      26 |
| mtme_XCOMET-XL-refA               | 0.321 |       0.019 |       0.052 |      26 |
| mtme_MetricX-23-b-refA            | 0.301 |       0.006 |       0.043 |      26 |
| mtme_MetricX-23-refA              | 0.3   |       0.009 |       0.039 |      26 |
| mtme_cometoid22-wmt22-src         | 0.253 |      -0.002 |       0.034 |      26 |
| mtme_cometoid22-wmt21-src         | 0.242 |      -0.004 |       0.033 |      26 |
| mtme_mbr-metricx-qe-src           | 0.241 |      -0.002 |       0.032 |      26 |
| mtme_CometKiwi-XXL-src            | 0.24  |       0.002 |       0.04  |      26 |
| mtme_cometoid22-wmt23-src         | 0.237 |      -0.009 |       0.036 |      26 |
| mtme_instructscore-refA           | 0.235 |       0.003 |       0.026 |      26 |
| mtme_CometKiwi-XL-src             | 0.231 |      -0.002 |       0.035 |      26 |
| mtme_GEMBA-MQM-src                | 0.221 |       0.002 |       0.03  |      26 |
| mtme_CometKiwi-src                | 0.22  |      -0.003 |       0.03  |      26 |
| mtme_MaTESe-refA                  | 0.218 |       0     |       0.029 |      26 |
| mtme_KG-BERTScore-src             | 0.214 |      -0.003 |       0.027 |      26 |
| mtme_COMET-refA                   | 0.213 |       0.004 |       0.034 |      26 |
| mtme_BLEURT-20-refA               | 0.203 |       0.002 |       0.03  |      26 |
| mtme_MetricX-23-c-refA            | 0.2   |      -0.008 |       0.02  |      26 |
| mtme_MS-COMET-QE-22-src           | 0.196 |      -0.019 |       0.035 |      26 |
| mtme_docWMT22CometDA-refA         | 0.181 |      -0.002 |       0.027 |      26 |
| mtme_Calibri-COMET22-QE-src       | 0.175 |      -0.001 |       0.022 |      26 |
| mtme_docWMT22CometKiwiDA-src      | 0.172 |      -0.006 |       0.021 |      26 |
| mtme_sescoreX-refA                | 0.171 |      -0.002 |       0.027 |      26 |
| mtme_Calibri-COMET22-refA         | 0.165 |      -0.004 |       0.017 |      26 |
| mtme_prismRef-refA                | 0.148 |      -0.008 |       0.014 |      26 |
| mtme_YiSi-1-refA                  | 0.128 |      -0.006 |       0.015 |      26 |
| mtme_mre-score-labse-regular-refA | 0.101 |      -0.01  |       0.012 |      26 |
| mtme_BERTscore-refA               | 0.098 |      -0.006 |       0.011 |      26 |
| mtme_XLsim-refA                   | 0.089 |      -0.007 |       0.011 |      26 |
| mtme_MEE4-refA                    | 0.061 |      -0.006 |       0.008 |      26 |
| mtme_chrF-refA                    | 0.054 |      -0.008 |       0.008 |      26 |
| mtme_tokengram_F-refA             | 0.051 |      -0.008 |       0.009 |      26 |
| mtme_BLEU-refA                    | 0.045 |      -0.008 |       0.009 |      26 |
| mtme_prismSrc-src                 | 0.04  |      -0.006 |       0.004 |      26 |
| mtme_eBLEU-refA                   | 0.039 |      -0.009 |       0.006 |      26 |
| mtme_f200spBLEU-refA              | 0.037 |      -0.007 |       0.008 |      26 |
| mtme_embed_llama-refA             | 0.035 |      -0.006 |       0.007 |      26 |