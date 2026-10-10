# Auditor strategies (results/mt/mt_*23_m2_p50_pair23??; design=dedup, fixed=mtme_COMET-refA, mode=cvl, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 26 ({'ende23': 16, 'zhen23': 10})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0026 |         -0.0105 |                  0.6154 |                   0.1154 |                    17.5566 |
| S3_select            |                0.0345 |          0.0196 |                  0.1923 |                   0.5    |                  -193.205  |
| S4_select_or_abstain |                0.0353 |          0.0196 |                  0.1538 |                   0.5    |                  -198.085  |
| best_posthoc         |               -0.0552 |         -0.0482 |                  1      |                   0      |                   289.089  |
| mean_judge           |                0.0003 |         -0.0032 |                  0.6154 |                   0.1538 |                    -1.7607 |

### ende23: 16 cells; median design saving vs uniform 0.028

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0122 |  -0.0136 |          0.75   |
| S3_select            |        0.0142 |   0.0127 |          0.25   |
| S4_select_or_abstain |        0.0153 |   0.013  |          0.25   |
| best_posthoc         |       -0.0629 |  -0.0588 |          1      |
| mean_judge           |       -0.0078 |  -0.0069 |          0.8125 |

### zhen23: 10 cells; median design saving vs uniform 0.053

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |        0.0127 |   0.0128 |             0.4 |
| S3_select            |        0.0668 |   0.0395 |             0.1 |
| S4_select_or_abstain |        0.0673 |   0.0427 |             0   |
| best_posthoc         |       -0.0429 |  -0.0328 |             1   |
| mean_judge           |        0.0134 |   0.0048 |             0.3 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0077 | 0.0267 |
| S2_fixed             |  0.0059 | 0.0267 |
| S3_select            |  0.0056 | 0.0233 |
| S4_select_or_abstain |  0.0056 | 0.0233 |

Abstention share (S4), mean over informative cells: 0.017

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.00 of informative cells

## Per informative cell

| lp     |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                |   excess_mean_judge |   p_best_vs_noise |
|:-------|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:----------------------------|--------------------:|------------------:|
| ende23 |     01 |  0.01 |  460 |       97.16  |     551.616 |         0.039 |            -0.016 |              0.055 |                         0.055 |           0.023 |                -0.058 | mtme_MetricX-23-QE-c-src    |              -0.015 |             0.37  |
| ende23 |     01 |  0.02 |  460 |       97.16  |     313.593 |         0.027 |            -0.025 |              0.028 |                         0.028 |           0.023 |                -0.122 | mtme_MetricX-23-QE-c-src    |              -0.007 |             0.455 |
| ende23 |     02 |  0.01 |  460 |       97.877 |     190.768 |         0.02  |            -0.024 |              0.032 |                         0.032 |           0     |                -0.147 | mtme_MetricX-23-refA        |              -0.006 |             0.295 |
| ende23 |     02 |  0.02 |  460 |       97.877 |     153.55  |         0.001 |            -0.012 |              0.008 |                         0.008 |           0     |                -0.024 | mtme_XCOMET-Ensemble-refA   |              -0.007 |             0.345 |
| ende23 |     12 |  0.01 |  460 |       96.257 |     202.765 |         0.048 |            -0.006 |              0.023 |                         0.023 |           0.003 |                -0.037 | mtme_XCOMET-Ensemble-refA   |              -0.004 |             0.765 |
| ende23 |     12 |  0.02 |  460 |       96.257 |     168.835 |         0.027 |             0.002 |              0.007 |                         0.009 |           0.003 |                -0.06  | mtme_MetricX-23-QE-c-src    |              -0.009 |             0.175 |
| ende23 |     23 |  0.01 |  460 |       94.783 |     227.685 |         0.096 |             0.013 |              0.07  |                         0.071 |           0.013 |                -0.014 | mtme_MaTESe-refA            |               0.025 |             0.56  |
| ende23 |     23 |  0.02 |  460 |       94.783 |     162.977 |         0.062 |             0.005 |              0.017 |                         0.017 |           0.013 |                -0.015 | mtme_XCOMET-Ensemble-refA   |              -0.001 |             0.8   |
| ende23 |     24 |  0.01 |  460 |       94.597 |     191.606 |         0.065 |            -0.058 |             -0.037 |                        -0.037 |           0.007 |                -0.086 | mtme_XCOMET-Ensemble-refA   |              -0.033 |             0.47  |
| ende23 |     24 |  0.02 |  460 |       94.597 |     142.975 |         0.028 |            -0.016 |              0.009 |                         0.009 |           0.007 |                -0.022 | mtme_XCOMET-Ensemble-refA   |               0.003 |             0.83  |
| ende23 |     34 |  0.01 |  460 |       94.673 |     536.55  |         0.151 |             0.018 |              0.069 |                         0.068 |           0.09  |                -0.014 | mtme_tokengram_F-refA       |               0.018 |             0.185 |
| ende23 |     34 |  0.02 |  460 |       94.673 |     268.329 |        -0.001 |            -0.008 |              0.024 |                         0.033 |           0.09  |                -0.045 | mtme_MetricX-23-b-refA      |              -0.011 |             0.49  |
| ende23 |     35 |  0.01 |  460 |       97.663 |     189.156 |         0.008 |            -0.015 |             -0.019 |                        -0.019 |           0.02  |                -0.061 | mtme_XCOMET-XXL-refA        |              -0.016 |             0.44  |
| ende23 |     35 |  0.02 |  460 |       97.663 |     151.792 |         0.012 |            -0.012 |              0.001 |                         0.006 |           0.02  |                -0.095 | mtme_XCOMET-XXL-refA        |              -0.002 |             0.225 |
| ende23 |     45 |  0.01 |  460 |       97.03  |     200.781 |         0.042 |            -0.017 |             -0.052 |                        -0.052 |           0.003 |                -0.07  | mtme_XCOMET-XXL-refA        |              -0.025 |             0.18  |
| ende23 |     45 |  0.02 |  460 |       97.03  |     152.144 |         0.007 |            -0.024 |             -0.007 |                        -0.007 |           0.003 |                -0.138 | mtme_XCOMET-Ensemble-refA   |              -0.036 |             0.275 |
| zhen23 |     01 |  0.01 | 1177 |       95.787 |     311.904 |         0.116 |             0.06  |              0.166 |                         0.166 |           0.013 |                -0.02  | mtme_sescoreX-refA          |               0.063 |             0.4   |
| zhen23 |     01 |  0.02 | 1177 |       95.787 |     146.222 |         0.024 |             0.012 |              0.031 |                         0.038 |           0.013 |                -0.021 | mtme_XCOMET-QE-Ensemble-src |               0.006 |             0.645 |
| zhen23 |     24 |  0.01 | 1177 |       64.983 |     178.174 |         0.411 |             0.021 |              0.131 |                         0.131 |           0.013 |                -0.014 | mtme_Calibri-COMET22-QE-src |               0.022 |             0.43  |
| zhen23 |     25 |  0.01 | 1177 |       96.087 |     218.099 |         0.05  |            -0.018 |              0.002 |                         0.002 |           0.003 |                -0.025 | mtme_BLEURT-20-refA         |               0.002 |             0.9   |
| zhen23 |     25 |  0.02 | 1177 |       96.087 |     149.761 |         0.011 |             0.013 |              0.003 |                         0.003 |           0.003 |                -0.087 | mtme_MetricX-23-c-refA      |               0.003 |             0.4   |
| zhen23 |     34 |  0.01 | 1177 |       65.677 |     226.17  |         0.52  |             0.066 |              0.216 |                         0.206 |           0.027 |                -0.024 | mtme_MaTESe-refA            |               0.042 |             0.43  |
| zhen23 |     35 |  0.01 | 1177 |       96.147 |     216.66  |         0.05  |            -0.015 |             -0.003 |                         0.001 |           0.01  |                -0.04  | mtme_docWMT22CometDA-refA   |              -0.006 |             0.44  |
| zhen23 |     35 |  0.02 | 1177 |       96.147 |     157.105 |         0.025 |            -0.018 |              0.001 |                         0.001 |           0.01  |                -0.051 | mtme_docWMT22CometDA-refA   |              -0.012 |             0.48  |
| zhen23 |     45 |  0.01 | 1177 |       95.843 |     209.492 |         0.061 |            -0.009 |              0.048 |                         0.048 |           0.01  |                -0.056 | mtme_MetricX-23-QE-src      |              -0.001 |             0.53  |
| zhen23 |     45 |  0.02 | 1177 |       95.843 |     155.798 |         0.055 |             0.015 |              0.072 |                         0.076 |           0.01  |                -0.091 | mtme_MetricX-23-c-refA      |               0.014 |             0.575 |

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