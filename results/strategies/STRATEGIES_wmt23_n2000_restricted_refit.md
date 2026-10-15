# Auditor strategies (results/mt/mt_*23_m2_p50_pair23n??; design=dedup, fixed=mtme_COMET-refA, mode=cvq, stat=rho, r0=0.2, s0=-1.0)

Cells: 60; informative (1 - P/J50_uniform >= 0.3): 60 ({'ende23': 30, 'zhen23': 30})

## Over informative cells: cost relative to S1 (negative = cheaper than the judge-free design)

| strategy             |   mean_excess_over_S1 |   median_excess |   share_cheaper_than_S1 |   share_costlier_by_2pct |   labels_saved_vs_S1_total |
|:---------------------|----------------------:|----------------:|------------------------:|-------------------------:|---------------------------:|
| S2_fixed             |               -0.0016 |               0 |                  0.0667 |                        0 |                    32.7813 |
| S3_select            |               -0.0009 |               0 |                  0.05   |                        0 |                    22.0092 |
| S4_select_or_abstain |               -0.0008 |               0 |                  0.05   |                        0 |                    19.7688 |
| best_posthoc         |               -0.003  |               0 |                  0.0667 |                        0 |                    66.2778 |
| mean_judge           |               -0.0011 |               0 |                  0.3667 |                        0 |                    24.1065 |

### ende23: 30 cells; median design saving vs uniform 0.000

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |       -0.0031 |        0 |          0.1333 |
| S3_select            |       -0.0024 |        0 |          0.1    |
| S4_select_or_abstain |       -0.0021 |        0 |          0.1    |
| best_posthoc         |       -0.006  |        0 |          0.1333 |
| mean_judge           |       -0.0023 |        0 |          0.2667 |

### zhen23: 30 cells; median design saving vs uniform -0.000

| strategy             |   mean_excess |   median |   share_cheaper |
|:---------------------|--------------:|---------:|----------------:|
| S2_fixed             |        0      |        0 |          0      |
| S3_select            |        0.0007 |        0 |          0      |
| S4_select_or_abstain |        0.0006 |        0 |          0      |
| best_posthoc         |        0      |        0 |          0      |
| mean_judge           |       -0      |        0 |          0.4667 |

## Wrong-certificate rate at the budget nearest J50 (mean over informative cells)

| strategy             |   wrong |    max |
|:---------------------|--------:|-------:|
| S1_design            |  0.0021 | 0.02   |
| S2_fixed             |  0.0019 | 0.0185 |
| S3_select            |  0.0019 | 0.0175 |
| S4_select_or_abstain |  0.0019 | 0.0175 |

Abstention share (S4), mean over informative cells: 0.011

Post-hoc best evaluator distinguishable from selection noise (p < 0.05) in 0.07 of informative cells

## Per informative cell

| lp     |   pair |   eps |    N |   pilot_cost |   J_uniform |   save_design |   excess_S2_fixed |   excess_S3_select |   excess_S4_select_or_abstain |   abstain_share |   excess_best_posthoc | best_posthoc                |   excess_mean_judge |   p_best_vs_noise |
|:-------|-------:|------:|-----:|-------------:|------------:|--------------:|------------------:|-------------------:|------------------------------:|----------------:|----------------------:|:----------------------------|--------------------:|------------------:|
| ende23 |     01 |  0.01 |  460 |       97.258 |     560.426 |         0.051 |            -0.03  |             -0.034 |                        -0.034 |           0.022 |                -0.058 | mtme_XCOMET-XL-refA         |              -0.023 |             0     |
| ende23 |     01 |  0.02 |  460 |       97.258 |     286.323 |         0.038 |            -0.032 |             -0.029 |                        -0.027 |           0.022 |                -0.059 | mtme_XCOMET-Ensemble-refA   |              -0.025 |             0.035 |
| ende23 |     02 |  0.01 |  460 |       97.898 |     207.158 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| ende23 |     02 |  0.02 |  460 |       97.898 |     207.158 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| ende23 |     03 |  0.01 |  460 |       97.808 |     207.068 |         0.001 |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     03 |  0.02 |  460 |       97.808 |     207.068 |         0.001 |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     04 |  0.01 |  460 |       97.497 |     206.757 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     04 |  0.02 |  460 |       97.497 |     206.757 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     05 |  0.01 |  460 |       98.241 |     207.501 |         0     |             0     |              0     |                         0     |           0     |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     05 |  0.02 |  460 |       98.241 |     207.501 |         0     |             0     |              0     |                         0     |           0     |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     12 |  0.01 |  460 |       96.414 |     207.692 |         0.01  |             0     |              0     |                         0     |           0.005 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     12 |  0.02 |  460 |       96.414 |     205.674 |         0     |             0     |              0     |                         0     |           0.005 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     13 |  0.01 |  460 |       97.164 |     206.424 |         0     |             0     |              0     |                         0     |           0.05  |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     13 |  0.02 |  460 |       97.164 |     206.424 |         0     |             0     |              0     |                         0     |           0.05  |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     14 |  0.01 |  460 |       96.537 |     205.797 |         0     |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     14 |  0.02 |  460 |       96.537 |     205.797 |         0     |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     15 |  0.01 |  460 |       98.565 |     207.825 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| ende23 |     15 |  0.02 |  460 |       98.565 |     207.825 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| ende23 |     23 |  0.01 |  460 |       94.932 |     215.365 |         0.051 |             0     |              0     |                         0     |           0.012 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     23 |  0.02 |  460 |       94.932 |     204.192 |        -0     |             0     |              0     |                         0     |           0.012 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     24 |  0.01 |  460 |       94.796 |     204.056 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     24 |  0.02 |  460 |       94.796 |     204.056 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     25 |  0.01 |  460 |       97.701 |     206.961 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     25 |  0.02 |  460 |       97.701 |     206.961 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     34 |  0.01 |  460 |       94.72  |     537.568 |         0.127 |            -0     |              0.006 |                         0.007 |           0.076 |                -0.017 | mtme_Calibri-COMET22-QE-src |              -0.001 |             0.04  |
| ende23 |     34 |  0.02 |  460 |       94.72  |     259.225 |         0.054 |            -0.033 |             -0.015 |                        -0.009 |           0.076 |                -0.047 | mtme_XCOMET-Ensemble-refA   |              -0.02  |             0.005 |
| ende23 |     35 |  0.01 |  460 |       97.72  |     206.98  |        -0     |             0     |              0     |                         0     |           0.019 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     35 |  0.02 |  460 |       97.72  |     206.98  |        -0     |             0     |              0     |                         0     |           0.019 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     45 |  0.01 |  460 |       97.044 |     206.304 |        -0     |             0     |              0     |                         0     |           0.009 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| ende23 |     45 |  0.02 |  460 |       97.044 |     206.304 |        -0     |             0     |              0     |                         0     |           0.009 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     01 |  0.01 | 1177 |       95.981 |     294.778 |         0.08  |             0     |              0.02  |                         0.017 |           0.016 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     01 |  0.02 | 1177 |       95.981 |     271.209 |         0.001 |             0     |              0     |                         0     |           0.016 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     02 |  0.01 | 1177 |       97.984 |     273.212 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     02 |  0.02 | 1177 |       97.984 |     273.212 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     03 |  0.01 | 1177 |       97.982 |     273.21  |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     03 |  0.02 | 1177 |       97.982 |     273.21  |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     04 |  0.01 | 1177 |       97.824 |     273.052 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     04 |  0.02 | 1177 |       97.824 |     273.052 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     05 |  0.01 | 1177 |       98.278 |     273.506 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     05 |  0.02 | 1177 |       98.278 |     273.506 |         0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     12 |  0.01 | 1177 |       98.822 |     274.05  |        -0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     12 |  0.02 | 1177 |       98.822 |     274.05  |        -0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     13 |  0.01 | 1177 |       98.822 |     274.05  |        -0     |             0     |              0     |                         0     |           0.006 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     13 |  0.02 | 1177 |       98.822 |     274.05  |        -0     |             0     |              0     |                         0     |           0.006 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     14 |  0.01 | 1177 |       98.788 |     274.016 |        -0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     14 |  0.02 | 1177 |       98.788 |     274.016 |        -0     |             0     |              0     |                         0     |           0.002 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     15 |  0.01 | 1177 |       98.822 |     274.05  |         0     |             0     |              0     |                         0     |           0.004 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     15 |  0.02 | 1177 |       98.822 |     274.05  |         0     |             0     |              0     |                         0     |           0.004 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     23 |  0.01 | 1177 |       58.362 |     233.59  |        -0.002 |             0     |              0     |                         0     |           0.011 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     23 |  0.02 | 1177 |       58.362 |     233.59  |        -0.002 |             0     |              0     |                         0     |           0.011 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     24 |  0.01 | 1177 |       64.878 |     240.106 |        -0.001 |             0     |              0     |                         0     |           0.021 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     24 |  0.02 | 1177 |       64.878 |     240.106 |        -0.001 |             0     |              0     |                         0     |           0.021 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     25 |  0.01 | 1177 |       96.168 |     271.396 |        -0     |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     25 |  0.02 | 1177 |       96.168 |     271.396 |        -0     |             0     |              0     |                         0     |           0.008 |                 0     | mtme_BERTscore-refA         |              -0     |             1     |
| zhen23 |     34 |  0.01 | 1177 |       65.662 |     240.89  |         0.001 |             0     |              0     |                         0     |           0.013 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     34 |  0.02 | 1177 |       65.662 |     240.89  |         0.001 |             0     |              0     |                         0     |           0.013 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     35 |  0.01 | 1177 |       96.206 |     271.434 |        -0     |             0     |              0     |                         0     |           0.011 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     35 |  0.02 | 1177 |       96.206 |     271.434 |        -0     |             0     |              0     |                         0     |           0.011 |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     45 |  0.01 | 1177 |       95.958 |     271.186 |        -0     |             0     |              0     |                         0     |           0.01  |                 0     | mtme_BERTscore-refA         |               0     |             1     |
| zhen23 |     45 |  0.02 | 1177 |       95.958 |     271.186 |        -0     |             0     |              0     |                         0     |           0.01  |                 0     | mtme_BERTscore-refA         |               0     |             1     |

## Evaluators over informative cells (pilot rho median; mean HES over the dedup design)

| judge                             |   rho |   HES_pilot |   HES_refit |   cells |
|:----------------------------------|------:|------------:|------------:|--------:|
| mtme_MetricX-23-QE-b-src          | 0.388 |       0     |       0.002 |      60 |
| mtme_XCOMET-QE-Ensemble-src       | 0.365 |       0     |       0.002 |      60 |
| mtme_MetricX-23-QE-src            | 0.363 |       0     |       0.002 |      60 |
| mtme_XCOMET-Ensemble-refA         | 0.358 |       0.001 |       0.003 |      60 |
| mtme_MetricX-23-QE-c-src          | 0.344 |       0.001 |       0.002 |      60 |
| mtme_XCOMET-XXL-refA              | 0.344 |       0.001 |       0.002 |      60 |
| mtme_XCOMET-XL-refA               | 0.32  |       0.001 |       0.003 |      60 |
| mtme_MetricX-23-refA              | 0.295 |      -0.001 |       0.001 |      60 |
| mtme_MetricX-23-b-refA            | 0.287 |      -0.001 |       0.001 |      60 |
| mtme_GEMBA-MQM-src                | 0.283 |      -0.001 |       0.001 |      60 |
| mtme_mbr-metricx-qe-src           | 0.282 |      -0     |       0.002 |      60 |
| mtme_cometoid22-wmt22-src         | 0.249 |      -0.001 |       0.002 |      60 |
| mtme_cometoid22-wmt21-src         | 0.243 |      -0     |       0.002 |      60 |
| mtme_CometKiwi-src                | 0.242 |      -0.001 |       0.001 |      60 |
| mtme_cometoid22-wmt23-src         | 0.239 |      -0.001 |       0.002 |      60 |
| mtme_CometKiwi-XXL-src            | 0.238 |      -0.001 |       0.001 |      60 |
| mtme_MetricX-23-c-refA            | 0.237 |      -0.001 |       0.001 |      60 |
| mtme_instructscore-refA           | 0.235 |       0     |       0.001 |      60 |
| mtme_CometKiwi-XL-src             | 0.234 |      -0.001 |       0.001 |      60 |
| mtme_MaTESe-refA                  | 0.234 |      -0.001 |       0.001 |      60 |
| mtme_KG-BERTScore-src             | 0.224 |      -0.001 |       0.001 |      60 |
| mtme_BLEURT-20-refA               | 0.207 |       0     |       0.001 |      60 |
| mtme_COMET-refA                   | 0.205 |       0     |       0.002 |      60 |
| mtme_Calibri-COMET22-QE-src       | 0.195 |      -0     |       0.001 |      60 |
| mtme_sescoreX-refA                | 0.187 |       0     |       0.001 |      60 |
| mtme_MS-COMET-QE-22-src           | 0.183 |      -0.003 |       0.001 |      60 |
| mtme_docWMT22CometKiwiDA-src      | 0.174 |      -0.001 |       0.001 |      60 |
| mtme_docWMT22CometDA-refA         | 0.17  |      -0     |       0.002 |      60 |
| mtme_Calibri-COMET22-refA         | 0.142 |       0     |       0.001 |      60 |
| mtme_prismRef-refA                | 0.131 |      -0.001 |       0     |      60 |
| mtme_YiSi-1-refA                  | 0.1   |      -0.001 |       0     |      60 |
| mtme_mre-score-labse-regular-refA | 0.098 |      -0.001 |       0     |      60 |
| mtme_BERTscore-refA               | 0.075 |      -0     |       0.001 |      60 |
| mtme_chrF-refA                    | 0.049 |      -0     |       0     |      60 |
| mtme_MEE4-refA                    | 0.048 |      -0     |       0.001 |      60 |
| mtme_XLsim-refA                   | 0.046 |      -0     |       0     |      60 |
| mtme_tokengram_F-refA             | 0.043 |      -0     |       0     |      60 |
| mtme_eBLEU-refA                   | 0.039 |      -0     |       0     |      60 |
| mtme_f200spBLEU-refA              | 0.036 |      -0     |       0     |      60 |
| mtme_embed_llama-refA             | 0.034 |       0     |       0.001 |      60 |
| mtme_BLEU-refA                    | 0.027 |      -0     |       0     |      60 |
| mtme_prismSrc-src                 | 0.022 |      -0.001 |       0     |      60 |