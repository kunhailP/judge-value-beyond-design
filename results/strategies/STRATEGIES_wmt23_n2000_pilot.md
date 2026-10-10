# Auditor strategies (results/mt/mt_*23_m2_p50_pair23n??; design=dedup, fixed=mtme_COMET-refA, mode=cvl, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 26 ({'ende23': 16, 'zhen23': 10})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0036 |         -0.0082 |                  0.6538 |                   0.1154 |                    25.2383 |
| S3_select            |                0.0419 |          0.0204 |                  0.2308 |                   0.5    |                  -209.261  |
| S4_select_or_abstain |                0.042  |          0.0218 |                  0.2308 |                   0.5385 |                  -209.723  |
| best_posthoc         |               -0.0351 |         -0.034  |                  0.8846 |                   0      |                   178.605  |
| mean_judge           |               -0.0002 |         -0.0029 |                  0.6154 |                   0.1154 |                     3.9819 |

### ende23: 16 cells; median design saving vs uniform 0.036

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0145 |  -0.0166 |           0.875 |
| S3_select            |        0.0116 |   0.0117 |           0.375 |
| S4_select_or_abstain |        0.012  |   0.0119 |           0.375 |
| best_posthoc         |       -0.0417 |  -0.0368 |           1     |
| mean_judge           |       -0.0068 |  -0.0058 |           0.75  |

### zhen23: 10 cells; median design saving vs uniform 0.041

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |        0.014  |   0.0154 |             0.3 |
| S3_select            |        0.0904 |   0.0435 |             0   |
| S4_select_or_abstain |        0.0901 |   0.0442 |             0   |
| best_posthoc         |       -0.0246 |  -0.0256 |             0.7 |
| mean_judge           |        0.0105 |   0.0083 |             0.4 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0065 | 0.0215 |
| S2_fixed             |  0.0054 | 0.0165 |
| S3_select            |  0.0047 | 0.0185 |
| S4_select_or_abstain |  0.0047 | 0.0185 |

Abstention share (S4), mean over informative cells: 0.016

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.69 of informative cells

## Per informative cell

| lp     |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                |   excess_mean_judge |   p_best_vs_noise |
|:-------|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:----------------------------|--------------------:|------------------:|
| ende23 |     01 |  0.01 |  460 |       97.258 |     560.426 |         0.051 |            -0.011 |              0.022 |                         0.022 |           0.022 |                -0.036 | mtme_XCOMET-Ensemble-refA   |              -0.005 |             0     |
| ende23 |     01 |  0.02 |  460 |       97.258 |     286.323 |         0.038 |            -0.009 |              0.038 |                         0.042 |           0.022 |                -0.032 | mtme_MetricX-23-QE-c-src    |              -0.001 |             0.035 |
| ende23 |     02 |  0.01 |  460 |       97.898 |     189.081 |         0.012 |            -0.018 |              0.005 |                         0.005 |           0.002 |                -0.038 | mtme_MetricX-23-refA        |              -0.002 |             0.015 |
| ende23 |     02 |  0.02 |  460 |       97.898 |     153.841 |         0.003 |            -0.016 |              0.008 |                         0.008 |           0.002 |                -0.024 | mtme_MetricX-23-b-refA      |              -0.003 |             0.02  |
| ende23 |     12 |  0.01 |  460 |       96.414 |     207.692 |         0.038 |            -0.024 |             -0.005 |                        -0.005 |           0.005 |                -0.054 | mtme_XCOMET-Ensemble-refA   |              -0.016 |             0.005 |
| ende23 |     12 |  0.02 |  460 |       96.414 |     168.26  |         0.028 |            -0.046 |             -0.026 |                        -0.025 |           0.005 |                -0.087 | mtme_XCOMET-Ensemble-refA   |              -0.025 |             0.01  |
| ende23 |     23 |  0.01 |  460 |       94.932 |     215.365 |         0.07  |            -0.002 |              0.058 |                         0.059 |           0.012 |                -0.043 | mtme_XCOMET-Ensemble-refA   |               0.008 |             0.125 |
| ende23 |     23 |  0.02 |  460 |       94.932 |     158.608 |         0.034 |             0.013 |              0.024 |                         0.024 |           0.012 |                -0.007 | mtme_XCOMET-Ensemble-refA   |               0.004 |             0.41  |
| ende23 |     24 |  0.01 |  460 |       94.796 |     193.204 |         0.084 |            -0.023 |              0.016 |                         0.016 |           0.002 |                -0.035 | mtme_XCOMET-Ensemble-refA   |              -0.007 |             0.03  |
| ende23 |     24 |  0.02 |  460 |       94.796 |     148.858 |         0.037 |            -0.022 |              0.025 |                         0.025 |           0.002 |                -0.033 | mtme_XCOMET-Ensemble-refA   |              -0.007 |             0     |
| ende23 |     34 |  0.01 |  460 |       94.72  |     537.568 |         0.127 |             0.01  |              0.056 |                         0.055 |           0.076 |                -0.001 | mtme_chrF-refA              |               0.01  |             0.49  |
| ende23 |     34 |  0.02 |  460 |       94.72  |     259.225 |         0.054 |            -0.012 |              0.048 |                         0.048 |           0.076 |                -0.022 | mtme_BLEURT-20-refA         |               0.003 |             0.105 |
| ende23 |     35 |  0.01 |  460 |       97.72  |     185.875 |         0.026 |            -0.029 |             -0.017 |                        -0.016 |           0.019 |                -0.052 | mtme_XCOMET-Ensemble-refA   |              -0.018 |             0.015 |
| ende23 |     35 |  0.02 |  460 |       97.72  |     152.417 |         0.007 |            -0.022 |             -0.018 |                        -0.017 |           0.019 |                -0.06  | mtme_MetricX-23-b-refA      |              -0.016 |             0     |
| ende23 |     45 |  0.01 |  460 |       97.044 |     188.355 |         0.036 |            -0.02  |             -0.041 |                        -0.042 |           0.009 |                -0.07  | mtme_XCOMET-Ensemble-refA   |              -0.021 |             0     |
| ende23 |     45 |  0.02 |  460 |       97.044 |     152.711 |         0.022 |            -0.003 |             -0.007 |                        -0.007 |           0.009 |                -0.072 | mtme_XCOMET-Ensemble-refA   |              -0.014 |             0     |
| zhen23 |     01 |  0.01 | 1177 |       95.981 |     294.778 |         0.099 |             0.017 |              0.234 |                         0.229 |           0.016 |                 0     | mtme_instructscore-refA     |               0.027 |             0.735 |
| zhen23 |     01 |  0.02 | 1177 |       95.981 |     150.217 |         0.04  |             0.029 |              0.09  |                         0.091 |           0.016 |                -0.007 | mtme_XCOMET-XXL-refA        |               0.016 |             0.33  |
| zhen23 |     24 |  0.01 | 1177 |       64.878 |     197.953 |         0.489 |             0.038 |              0.217 |                         0.217 |           0.021 |                 0.009 | mtme_Calibri-COMET22-QE-src |               0.043 |             0.025 |
| zhen23 |     25 |  0.01 | 1177 |       96.168 |     208.233 |         0.032 |            -0.016 |              0.015 |                         0.015 |           0.008 |                -0.063 | mtme_MetricX-23-QE-b-src    |              -0.016 |             0.045 |
| zhen23 |     25 |  0.02 | 1177 |       96.168 |     140.99  |         0.027 |             0.014 |              0.046 |                         0.048 |           0.008 |                -0.023 | mtme_MetricX-23-QE-b-src    |               0.012 |             0.025 |
| zhen23 |     34 |  0.01 | 1177 |       65.662 |     218.749 |         0.484 |             0.046 |              0.211 |                         0.21  |           0.013 |                 0.015 | mtme_prismSrc-src           |               0.041 |             0.22  |
| zhen23 |     35 |  0.01 | 1177 |       96.206 |     217.129 |         0.039 |            -0.008 |              0.019 |                         0.021 |           0.011 |                -0.06  | mtme_XCOMET-QE-Ensemble-src |              -0.008 |             0     |
| zhen23 |     35 |  0.02 | 1177 |       96.206 |     148.502 |         0.025 |             0.002 |              0.017 |                         0.015 |           0.011 |                -0.028 | mtme_MetricX-23-QE-c-src    |              -0.002 |             0.04  |
| zhen23 |     45 |  0.01 | 1177 |       95.958 |     209.768 |         0.071 |            -0.001 |              0.013 |                         0.013 |           0.01  |                -0.058 | mtme_XCOMET-Ensemble-refA   |              -0.013 |             0.04  |
| zhen23 |     45 |  0.02 | 1177 |       95.958 |     139.293 |         0.042 |             0.017 |              0.041 |                         0.041 |           0.01  |                -0.03  | mtme_MetricX-23-QE-c-src    |               0.005 |             0.09  |

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