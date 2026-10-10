# S2 (fixed mtme_COMET-refA) vs S3 (pilot selection by rho), cvq; results/mt/mt_*23_m2_p50_boundary_pair23b??

G = 1 - J50(S3)/J50(S2) per cell, paired over audits (300 per cell, 200 bootstrap draws); positive = selection cheaper. Margin of practical equivalence: 2% (lock v1.2 addendum).

## Pooled, primary: mean over cells; 95% Monte-Carlo interval from the joint resampling of draw indices (fixed benchmark)

| cells   | lp     |   n |   G_mean |   G_lo |   G_hi |   share_G_pos |   D2_mean |   D2_lo |   D2_hi |   D3_mean |   D3_lo |   D3_hi | verdict   |
|:--------|:-------|----:|---------:|-------:|-------:|--------------:|----------:|--------:|--------:|----------:|--------:|--------:|:----------|
| all 60  | pooled |  30 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |
| all 60  | ende23 |  15 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |
| all 60  | zhen23 |  15 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |

## Pooled, sensitivity: decisions as clusters (point = mean over decisions of the within-decision mean; cluster bootstrap over decisions x joint draws)

| cells   | lp     |   n |   G_dec |   G_dec_lo |   G_dec_hi |   D2_dec |   D2_dec_lo |   D2_dec_hi |   D3_dec |   D3_dec_lo |   D3_dec_hi |
|:--------|:-------|----:|--------:|-----------:|-----------:|---------:|------------:|------------:|---------:|------------:|------------:|
| all 60  | pooled |  30 |     nan |        nan |        nan |      nan |         nan |         nan |      nan |         nan |         nan |
| all 60  | ende23 |  15 |     nan |        nan |        nan |      nan |         nan |         nan |      nan |         nan |         nan |
| all 60  | zhen23 |  15 |     nan |        nan |        nan |      nan |         nan |         nan |      nan |         nan |         nan |

## Per-cell interval widths (informative cells, medians)

G: nan; D2 (S2 vs S1): nan; D3 (S3 vs S1): nan
cells with G interval above 0: 0/0; below 0: 0/0; D2 above 0: 0; D3 above 0: 0

## Coverage of the chosen arm's upper bound (nominal 0.90) and wrong certificates, informative cells

| strategy   | ('cover_all', 'mean')   | ('cover_all', 'min')   | ('cover_all', 'max')   | ('cover_min_budget', 'mean')   | ('cover_min_budget', 'min')   | ('cover_min_budget', 'max')   | ('cover_at_J50', 'mean')   | ('cover_at_J50', 'min')   | ('cover_at_J50', 'max')   | ('wrong_at_J50', 'mean')   | ('wrong_at_J50', 'min')   | ('wrong_at_J50', 'max')   | ('wrong_max', 'mean')   | ('wrong_max', 'min')   | ('wrong_max', 'max')   | ('wrong_mean', 'mean')   | ('wrong_mean', 'min')   | ('wrong_mean', 'max')   |
|------------|-------------------------|------------------------|------------------------|--------------------------------|-------------------------------|-------------------------------|----------------------------|---------------------------|---------------------------|----------------------------|---------------------------|---------------------------|-------------------------|------------------------|------------------------|--------------------------|-------------------------|-------------------------|

## Wrong-certificate rate by post-pilot budget, mean over all 30 cells (boundary runs: type-I error, nominal 0.1)

Budgets are expected sampled items (Poisson design); 'cost' is the realised mean number of human labels, pilot included.

|   budget |   S1_design |   S2_fixed |   S3_select |   S4_select_or_abstain |
|---------:|------------:|-----------:|------------:|-----------------------:|
|       10 |       0.182 |      0.172 |       0.123 |                  0.122 |
|       13 |       0.141 |      0.13  |       0.116 |                  0.116 |
|       14 |       0.146 |      0.141 |       0.106 |                  0.106 |
|       17 |       0.124 |      0.114 |       0.104 |                  0.104 |
|       20 |       0.139 |      0.143 |       0.108 |                  0.108 |
|       23 |       0.114 |      0.112 |       0.097 |                  0.097 |
|       29 |       0.121 |      0.118 |       0.109 |                  0.109 |
|       31 |       0.107 |      0.096 |       0.088 |                  0.088 |
|       41 |       0.124 |      0.112 |       0.103 |                  0.103 |
|       42 |       0.108 |      0.107 |       0.095 |                  0.095 |
|       55 |       0.092 |      0.088 |       0.082 |                  0.082 |
|       61 |       0.101 |      0.103 |       0.085 |                  0.085 |
|       73 |       0.094 |      0.084 |       0.086 |                  0.086 |
|       88 |       0.087 |      0.086 |       0.08  |                  0.08  |
|       98 |       0.083 |      0.076 |       0.075 |                  0.074 |
|      127 |       0.085 |      0.085 |       0.076 |                  0.076 |
|      130 |       0.067 |      0.063 |       0.067 |                  0.068 |
|      174 |       0.048 |      0.05  |       0.048 |                  0.048 |
|      183 |       0.055 |      0.054 |       0.052 |                  0.052 |
|      231 |       0.05  |      0.051 |       0.048 |                  0.047 |
|      263 |       0.052 |      0.05  |       0.045 |                  0.045 |
|      308 |       0.034 |      0.028 |       0.031 |                  0.031 |
|      378 |       0.035 |      0.036 |       0.027 |                  0.026 |
|      410 |       0     |      0     |       0     |                  0     |
|      544 |       0.024 |      0.024 |       0.022 |                  0.022 |
|      783 |       0.012 |      0.011 |       0.01  |                  0.011 |
|     1127 |       0     |      0     |       0     |                  0     |

Per-cell maximum over budgets, mean / max over cells:

| strategy             |   mean |   max |
|:---------------------|-------:|------:|
| S1_design            |  0.184 | 0.243 |
| S2_fixed             |  0.175 | 0.24  |
| S3_select            |  0.133 | 0.2   |
| S4_select_or_abstain |  0.133 | 0.2   |

### Pooled rate per budget and language pair (one-sided binomial test of rate > alpha over cells x draws; * = from this budget on, no later budget is significantly above alpha)

| lp     | strategy             |   budget |   cost |   rate |   p_above | from_here_on   |
|:-------|:---------------------|---------:|-------:|-------:|----------:|:---------------|
| ende23 | S1_design            |       10 |  116.2 |  0.18  |     0     |                |
| ende23 | S1_design            |       13 |  123.4 |  0.141 |     0     |                |
| ende23 | S1_design            |       17 |  130.6 |  0.124 |     0     |                |
| ende23 | S1_design            |       23 |  143.9 |  0.114 |     0.002 |                |
| ende23 | S1_design            |       31 |  158.4 |  0.107 |     0.06  |                |
| ende23 | S1_design            |       41 |  178.7 |  0.124 |     0     |                |
| ende23 | S1_design            |       55 |  206.3 |  0.092 |     0.966 | *              |
| ende23 | S1_design            |       73 |  244.4 |  0.094 |     0.915 |                |
| ende23 | S1_design            |       98 |  291   |  0.083 |     1     |                |
| ende23 | S1_design            |      130 |  357.7 |  0.067 |     1     |                |
| ende23 | S1_design            |      174 |  443.3 |  0.048 |     1     |                |
| ende23 | S1_design            |      231 |  558.7 |  0.05  |     1     |                |
| ende23 | S1_design            |      308 |  713.5 |  0.034 |     1     |                |
| ende23 | S1_design            |      410 |  867.1 |  0     |     1     |                |
| ende23 | S2_fixed             |       10 |  116.2 |  0.16  |     0     |                |
| ende23 | S2_fixed             |       13 |  123.4 |  0.13  |     0     |                |
| ende23 | S2_fixed             |       17 |  130.6 |  0.114 |     0.001 |                |
| ende23 | S2_fixed             |       23 |  143.9 |  0.112 |     0.005 |                |
| ende23 | S2_fixed             |       31 |  158.4 |  0.096 |     0.846 |                |
| ende23 | S2_fixed             |       41 |  178.7 |  0.112 |     0.004 |                |
| ende23 | S2_fixed             |       55 |  206.3 |  0.088 |     0.998 | *              |
| ende23 | S2_fixed             |       73 |  244.4 |  0.084 |     1     |                |
| ende23 | S2_fixed             |       98 |  291   |  0.076 |     1     |                |
| ende23 | S2_fixed             |      130 |  357.7 |  0.063 |     1     |                |
| ende23 | S2_fixed             |      174 |  443.3 |  0.05  |     1     |                |
| ende23 | S2_fixed             |      231 |  558.7 |  0.051 |     1     |                |
| ende23 | S2_fixed             |      308 |  713.5 |  0.028 |     1     |                |
| ende23 | S2_fixed             |      410 |  867.1 |  0     |     1     |                |
| ende23 | S3_select            |       10 |  116.2 |  0.119 |     0     |                |
| ende23 | S3_select            |       13 |  123.4 |  0.116 |     0     |                |
| ende23 | S3_select            |       17 |  130.6 |  0.104 |     0.192 | *              |
| ende23 | S3_select            |       23 |  143.9 |  0.097 |     0.748 |                |
| ende23 | S3_select            |       31 |  158.4 |  0.088 |     0.997 |                |
| ende23 | S3_select            |       41 |  178.7 |  0.103 |     0.25  |                |
| ende23 | S3_select            |       55 |  206.3 |  0.082 |     1     |                |
| ende23 | S3_select            |       73 |  244.4 |  0.086 |     0.999 |                |
| ende23 | S3_select            |       98 |  291   |  0.075 |     1     |                |
| ende23 | S3_select            |      130 |  357.7 |  0.067 |     1     |                |
| ende23 | S3_select            |      174 |  443.3 |  0.048 |     1     |                |
| ende23 | S3_select            |      231 |  558.7 |  0.048 |     1     |                |
| ende23 | S3_select            |      308 |  713.5 |  0.031 |     1     |                |
| ende23 | S3_select            |      410 |  867.1 |  0     |     1     |                |
| ende23 | S4_select_or_abstain |       10 |  116.2 |  0.118 |     0     |                |
| ende23 | S4_select_or_abstain |       13 |  123.4 |  0.116 |     0     |                |
| ende23 | S4_select_or_abstain |       17 |  130.6 |  0.104 |     0.192 | *              |
| ende23 | S4_select_or_abstain |       23 |  143.9 |  0.097 |     0.763 |                |
| ende23 | S4_select_or_abstain |       31 |  158.4 |  0.088 |     0.997 |                |
| ende23 | S4_select_or_abstain |       41 |  178.7 |  0.103 |     0.266 |                |
| ende23 | S4_select_or_abstain |       55 |  206.3 |  0.082 |     1     |                |
| ende23 | S4_select_or_abstain |       73 |  244.4 |  0.086 |     0.999 |                |
| ende23 | S4_select_or_abstain |       98 |  291   |  0.074 |     1     |                |
| ende23 | S4_select_or_abstain |      130 |  357.7 |  0.068 |     1     |                |
| ende23 | S4_select_or_abstain |      174 |  443.3 |  0.048 |     1     |                |
| ende23 | S4_select_or_abstain |      231 |  558.7 |  0.047 |     1     |                |
| ende23 | S4_select_or_abstain |      308 |  713.5 |  0.031 |     1     |                |
| ende23 | S4_select_or_abstain |      410 |  867.1 |  0     |     1     |                |
| zhen23 | S1_design            |       10 |  110.2 |  0.184 |     0     |                |
| zhen23 | S1_design            |       14 |  118.6 |  0.146 |     0     |                |
| zhen23 | S1_design            |       20 |  130.8 |  0.139 |     0     |                |
| zhen23 | S1_design            |       29 |  148.4 |  0.121 |     0     |                |
| zhen23 | S1_design            |       42 |  174.6 |  0.108 |     0.032 |                |
| zhen23 | S1_design            |       61 |  211   |  0.101 |     0.39  | *              |
| zhen23 | S1_design            |       88 |  265.3 |  0.087 |     0.998 |                |
| zhen23 | S1_design            |      127 |  342.7 |  0.085 |     1     |                |
| zhen23 | S1_design            |      183 |  459.3 |  0.055 |     1     |                |
| zhen23 | S1_design            |      263 |  607   |  0.052 |     1     |                |
| zhen23 | S1_design            |      378 |  809.3 |  0.035 |     1     |                |
| zhen23 | S1_design            |      544 | 1076.1 |  0.024 |     1     |                |
| zhen23 | S1_design            |      783 | 1461.3 |  0.012 |     1     |                |
| zhen23 | S1_design            |     1127 | 1924.5 |  0     |     1     |                |
| zhen23 | S2_fixed             |       10 |  110.2 |  0.185 |     0     |                |
| zhen23 | S2_fixed             |       14 |  118.6 |  0.141 |     0     |                |
| zhen23 | S2_fixed             |       20 |  130.8 |  0.143 |     0     |                |
| zhen23 | S2_fixed             |       29 |  148.4 |  0.118 |     0     |                |
| zhen23 | S2_fixed             |       42 |  174.6 |  0.107 |     0.072 | *              |
| zhen23 | S2_fixed             |       61 |  211   |  0.103 |     0.282 |                |
| zhen23 | S2_fixed             |       88 |  265.3 |  0.086 |     0.999 |                |
| zhen23 | S2_fixed             |      127 |  342.7 |  0.085 |     1     |                |
| zhen23 | S2_fixed             |      183 |  459.3 |  0.054 |     1     |                |
| zhen23 | S2_fixed             |      263 |  607   |  0.05  |     1     |                |
| zhen23 | S2_fixed             |      378 |  809.3 |  0.036 |     1     |                |
| zhen23 | S2_fixed             |      544 | 1076.1 |  0.024 |     1     |                |
| zhen23 | S2_fixed             |      783 | 1461.3 |  0.011 |     1     |                |
| zhen23 | S2_fixed             |     1127 | 1924.5 |  0     |     1     |                |
| zhen23 | S3_select            |       10 |  110.2 |  0.126 |     0     |                |
| zhen23 | S3_select            |       14 |  118.6 |  0.106 |     0.112 |                |
| zhen23 | S3_select            |       20 |  130.8 |  0.108 |     0.04  |                |
| zhen23 | S3_select            |       29 |  148.4 |  0.109 |     0.026 |                |
| zhen23 | S3_select            |       42 |  174.6 |  0.095 |     0.869 | *              |
| zhen23 | S3_select            |       61 |  211   |  0.085 |     1     |                |
| zhen23 | S3_select            |       88 |  265.3 |  0.08  |     1     |                |
| zhen23 | S3_select            |      127 |  342.7 |  0.076 |     1     |                |
| zhen23 | S3_select            |      183 |  459.3 |  0.052 |     1     |                |
| zhen23 | S3_select            |      263 |  607   |  0.045 |     1     |                |
| zhen23 | S3_select            |      378 |  809.3 |  0.027 |     1     |                |
| zhen23 | S3_select            |      544 | 1076.1 |  0.022 |     1     |                |
| zhen23 | S3_select            |      783 | 1461.3 |  0.01  |     1     |                |
| zhen23 | S3_select            |     1127 | 1924.5 |  0     |     1     |                |
| zhen23 | S4_select_or_abstain |       10 |  110.2 |  0.126 |     0     |                |
| zhen23 | S4_select_or_abstain |       14 |  118.6 |  0.106 |     0.112 |                |
| zhen23 | S4_select_or_abstain |       20 |  130.8 |  0.108 |     0.04  |                |
| zhen23 | S4_select_or_abstain |       29 |  148.4 |  0.109 |     0.029 |                |
| zhen23 | S4_select_or_abstain |       42 |  174.6 |  0.095 |     0.869 | *              |
| zhen23 | S4_select_or_abstain |       61 |  211   |  0.085 |     1     |                |
| zhen23 | S4_select_or_abstain |       88 |  265.3 |  0.08  |     1     |                |
| zhen23 | S4_select_or_abstain |      127 |  342.7 |  0.076 |     1     |                |
| zhen23 | S4_select_or_abstain |      183 |  459.3 |  0.052 |     1     |                |
| zhen23 | S4_select_or_abstain |      263 |  607   |  0.045 |     1     |                |
| zhen23 | S4_select_or_abstain |      378 |  809.3 |  0.026 |     1     |                |
| zhen23 | S4_select_or_abstain |      544 | 1076.1 |  0.022 |     1     |                |
| zhen23 | S4_select_or_abstain |      783 | 1461.3 |  0.011 |     1     |                |
| zhen23 | S4_select_or_abstain |     1127 | 1924.5 |  0     |     1     |                |

### Each strategy against S1 on the same cell and budget (difference of wrong-certificate rates)

| lp     | strategy             |   cells_x_budgets |   mean_diff_vs_S1 |   share_above_S1 |   share_above_S1_by_2pts |   max_diff |
|:-------|:---------------------|------------------:|------------------:|-----------------:|-------------------------:|-----------:|
| ende23 | S2_fixed             |               210 |           -0.0067 |            0.19  |                    0.01  |      0.037 |
| ende23 | S3_select            |               210 |           -0.0138 |            0.186 |                    0.024 |      0.037 |
| ende23 | S4_select_or_abstain |               210 |           -0.014  |            0.176 |                    0.024 |      0.037 |
| zhen23 | S2_fixed             |               210 |           -0.0006 |            0.338 |                    0.019 |      0.027 |
| zhen23 | S3_select            |               210 |           -0.0149 |            0.152 |                    0.029 |      0.037 |
| zhen23 | S4_select_or_abstain |               210 |           -0.0149 |            0.157 |                    0.029 |      0.037 |

## Per cell

| lp     |   pair |   eps | informative   |   J_uniform |   J_S1 |   J_S2 |   J_S3 |   G |   G_lo |   G_hi |   G_sd |   D2 |   D2_lo |   D2_hi |   D3 |   D3_lo |   D3_hi |   n_audits |
|:-------|-------:|------:|:--------------|------------:|-------:|-------:|-------:|----:|-------:|-------:|-------:|-----:|--------:|--------:|-----:|--------:|--------:|-----------:|
| ende23 |     01 | 0.003 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     02 | 0.027 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     03 | 0.049 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     04 | 0.05  | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     05 | 0.078 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     12 | 0.024 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     13 | 0.046 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     14 | 0.047 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     15 | 0.075 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     23 | 0.022 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     24 | 0.023 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     25 | 0.051 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     34 | 0.001 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     35 | 0.029 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| ende23 |     45 | 0.028 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     01 | 0.006 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     02 | 0.043 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     03 | 0.044 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     04 | 0.043 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     05 | 0.058 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     12 | 0.036 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     13 | 0.038 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     14 | 0.037 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     15 | 0.051 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     23 | 0.001 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     24 | 0     | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     25 | 0.015 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     34 | 0.001 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     35 | 0.013 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |
| zhen23 |     45 | 0.015 | False         |         nan |    nan |    nan |    nan | nan |    nan |    nan |    nan |  nan |     nan |     nan |  nan |     nan |     nan |        300 |