# S2 (fixed mtme_COMET-refA) vs S3 (pilot selection by rho), cvq; results/mt/mt_*23_m2_p50_boundary_pair23c??

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
|       10 |       0.179 |      0.163 |       0.122 |                  0.122 |
|       13 |       0.129 |      0.116 |       0.099 |                  0.099 |
|       14 |       0.175 |      0.17  |       0.126 |                  0.126 |
|       17 |       0.134 |      0.124 |       0.109 |                  0.11  |
|       20 |       0.135 |      0.134 |       0.114 |                  0.114 |
|       23 |       0.119 |      0.104 |       0.095 |                  0.095 |
|       29 |       0.119 |      0.114 |       0.096 |                  0.097 |
|       31 |       0.122 |      0.111 |       0.103 |                  0.103 |
|       41 |       0.118 |      0.109 |       0.097 |                  0.098 |
|       42 |       0.121 |      0.122 |       0.105 |                  0.106 |
|       55 |       0.088 |      0.083 |       0.074 |                  0.074 |
|       61 |       0.085 |      0.087 |       0.079 |                  0.078 |
|       73 |       0.086 |      0.085 |       0.082 |                  0.082 |
|       88 |       0.079 |      0.084 |       0.072 |                  0.072 |
|       98 |       0.086 |      0.082 |       0.08  |                  0.079 |
|      127 |       0.082 |      0.08  |       0.069 |                  0.069 |
|      130 |       0.069 |      0.061 |       0.067 |                  0.067 |
|      174 |       0.059 |      0.055 |       0.052 |                  0.052 |
|      183 |       0.062 |      0.058 |       0.056 |                  0.056 |
|      231 |       0.048 |      0.046 |       0.043 |                  0.043 |
|      263 |       0.052 |      0.05  |       0.042 |                  0.042 |
|      308 |       0.033 |      0.032 |       0.03  |                  0.03  |
|      378 |       0.024 |      0.027 |       0.024 |                  0.024 |
|      410 |       0     |      0     |       0     |                  0     |
|      544 |       0.017 |      0.017 |       0.014 |                  0.014 |
|      783 |       0.01  |      0.011 |       0.008 |                  0.008 |
|     1127 |       0     |      0     |       0     |                  0     |

Per-cell maximum over budgets, mean / max over cells:

| strategy             |   mean |   max |
|:---------------------|-------:|------:|
| S1_design            |  0.184 | 0.233 |
| S2_fixed             |  0.17  | 0.243 |
| S3_select            |  0.139 | 0.19  |
| S4_select_or_abstain |  0.139 | 0.19  |

### Mean rate per budget and language pair, 95% Monte-Carlo interval from the joint resampling of draw indices (* = from this budget on, the observed mean rate is at or below 0.1 at every later budget; an observation on this simulation, not a test)

| lp     | strategy             |   budget |   cost |   rate |   mc_lo |   mc_hi | from_here_on   |
|:-------|:---------------------|---------:|-------:|-------:|--------:|--------:|:---------------|
| ende23 | S1_design            |       10 |  117.6 |  0.179 |   0.161 |   0.198 |                |
| ende23 | S1_design            |       13 |  123.4 |  0.129 |   0.111 |   0.145 |                |
| ende23 | S1_design            |       17 |  130.9 |  0.134 |   0.117 |   0.152 |                |
| ende23 | S1_design            |       23 |  141.8 |  0.119 |   0.103 |   0.133 |                |
| ende23 | S1_design            |       31 |  158.9 |  0.122 |   0.105 |   0.136 |                |
| ende23 | S1_design            |       41 |  178.8 |  0.118 |   0.102 |   0.131 |                |
| ende23 | S1_design            |       55 |  207   |  0.088 |   0.075 |   0.1   | *              |
| ende23 | S1_design            |       73 |  244.3 |  0.086 |   0.076 |   0.096 |                |
| ende23 | S1_design            |       98 |  292.8 |  0.086 |   0.074 |   0.1   |                |
| ende23 | S1_design            |      130 |  357   |  0.069 |   0.059 |   0.079 |                |
| ende23 | S1_design            |      174 |  444.6 |  0.059 |   0.05  |   0.073 |                |
| ende23 | S1_design            |      231 |  559.8 |  0.048 |   0.041 |   0.057 |                |
| ende23 | S1_design            |      308 |  710.7 |  0.033 |   0.027 |   0.04  |                |
| ende23 | S1_design            |      410 |  867   |  0     |   0     |   0     |                |
| ende23 | S2_fixed             |       10 |  117.6 |  0.151 |   0.132 |   0.166 |                |
| ende23 | S2_fixed             |       13 |  123.4 |  0.116 |   0.102 |   0.13  |                |
| ende23 | S2_fixed             |       17 |  130.9 |  0.124 |   0.107 |   0.14  |                |
| ende23 | S2_fixed             |       23 |  141.8 |  0.104 |   0.09  |   0.117 |                |
| ende23 | S2_fixed             |       31 |  158.9 |  0.111 |   0.097 |   0.125 |                |
| ende23 | S2_fixed             |       41 |  178.8 |  0.109 |   0.097 |   0.122 |                |
| ende23 | S2_fixed             |       55 |  207   |  0.083 |   0.07  |   0.095 | *              |
| ende23 | S2_fixed             |       73 |  244.3 |  0.085 |   0.074 |   0.096 |                |
| ende23 | S2_fixed             |       98 |  292.8 |  0.082 |   0.069 |   0.094 |                |
| ende23 | S2_fixed             |      130 |  357   |  0.061 |   0.052 |   0.07  |                |
| ende23 | S2_fixed             |      174 |  444.6 |  0.055 |   0.047 |   0.066 |                |
| ende23 | S2_fixed             |      231 |  559.8 |  0.046 |   0.039 |   0.054 |                |
| ende23 | S2_fixed             |      308 |  710.7 |  0.032 |   0.025 |   0.038 |                |
| ende23 | S2_fixed             |      410 |  867   |  0     |   0     |   0     |                |
| ende23 | S3_select            |       10 |  117.6 |  0.124 |   0.109 |   0.138 |                |
| ende23 | S3_select            |       13 |  123.4 |  0.099 |   0.086 |   0.113 |                |
| ende23 | S3_select            |       17 |  130.9 |  0.109 |   0.093 |   0.122 |                |
| ende23 | S3_select            |       23 |  141.8 |  0.095 |   0.082 |   0.107 |                |
| ende23 | S3_select            |       31 |  158.9 |  0.103 |   0.089 |   0.116 |                |
| ende23 | S3_select            |       41 |  178.8 |  0.097 |   0.086 |   0.11  | *              |
| ende23 | S3_select            |       55 |  207   |  0.074 |   0.063 |   0.084 |                |
| ende23 | S3_select            |       73 |  244.3 |  0.082 |   0.07  |   0.091 |                |
| ende23 | S3_select            |       98 |  292.8 |  0.08  |   0.069 |   0.092 |                |
| ende23 | S3_select            |      130 |  357   |  0.067 |   0.057 |   0.076 |                |
| ende23 | S3_select            |      174 |  444.6 |  0.052 |   0.044 |   0.062 |                |
| ende23 | S3_select            |      231 |  559.8 |  0.043 |   0.037 |   0.051 |                |
| ende23 | S3_select            |      308 |  710.7 |  0.03  |   0.024 |   0.037 |                |
| ende23 | S3_select            |      410 |  867   |  0     |   0     |   0     |                |
| ende23 | S4_select_or_abstain |       10 |  117.6 |  0.124 |   0.109 |   0.138 |                |
| ende23 | S4_select_or_abstain |       13 |  123.4 |  0.099 |   0.086 |   0.113 |                |
| ende23 | S4_select_or_abstain |       17 |  130.9 |  0.11  |   0.093 |   0.122 |                |
| ende23 | S4_select_or_abstain |       23 |  141.8 |  0.095 |   0.082 |   0.108 |                |
| ende23 | S4_select_or_abstain |       31 |  158.9 |  0.103 |   0.089 |   0.115 |                |
| ende23 | S4_select_or_abstain |       41 |  178.8 |  0.098 |   0.086 |   0.11  | *              |
| ende23 | S4_select_or_abstain |       55 |  207   |  0.074 |   0.062 |   0.084 |                |
| ende23 | S4_select_or_abstain |       73 |  244.3 |  0.082 |   0.07  |   0.091 |                |
| ende23 | S4_select_or_abstain |       98 |  292.8 |  0.079 |   0.068 |   0.091 |                |
| ende23 | S4_select_or_abstain |      130 |  357   |  0.067 |   0.057 |   0.076 |                |
| ende23 | S4_select_or_abstain |      174 |  444.6 |  0.052 |   0.044 |   0.062 |                |
| ende23 | S4_select_or_abstain |      231 |  559.8 |  0.043 |   0.037 |   0.051 |                |
| ende23 | S4_select_or_abstain |      308 |  710.7 |  0.03  |   0.024 |   0.036 |                |
| ende23 | S4_select_or_abstain |      410 |  867   |  0     |   0     |   0     |                |
| zhen23 | S1_design            |       10 |  110.8 |  0.179 |   0.158 |   0.2   |                |
| zhen23 | S1_design            |       14 |  117.9 |  0.175 |   0.157 |   0.199 |                |
| zhen23 | S1_design            |       20 |  130.6 |  0.135 |   0.117 |   0.153 |                |
| zhen23 | S1_design            |       29 |  147.9 |  0.119 |   0.103 |   0.135 |                |
| zhen23 | S1_design            |       42 |  173.7 |  0.121 |   0.104 |   0.137 |                |
| zhen23 | S1_design            |       61 |  213.2 |  0.085 |   0.071 |   0.101 | *              |
| zhen23 | S1_design            |       88 |  267.9 |  0.079 |   0.067 |   0.092 |                |
| zhen23 | S1_design            |      127 |  344.8 |  0.082 |   0.072 |   0.096 |                |
| zhen23 | S1_design            |      183 |  453.6 |  0.062 |   0.052 |   0.073 |                |
| zhen23 | S1_design            |      263 |  605.2 |  0.052 |   0.042 |   0.06  |                |
| zhen23 | S1_design            |      378 |  812.8 |  0.024 |   0.018 |   0.032 |                |
| zhen23 | S1_design            |      544 | 1078.2 |  0.017 |   0.012 |   0.022 |                |
| zhen23 | S1_design            |      783 | 1459.4 |  0.01  |   0.006 |   0.014 |                |
| zhen23 | S1_design            |     1127 | 1924.6 |  0     |   0     |   0     |                |
| zhen23 | S2_fixed             |       10 |  110.8 |  0.175 |   0.154 |   0.193 |                |
| zhen23 | S2_fixed             |       14 |  117.9 |  0.17  |   0.151 |   0.194 |                |
| zhen23 | S2_fixed             |       20 |  130.6 |  0.134 |   0.116 |   0.152 |                |
| zhen23 | S2_fixed             |       29 |  147.9 |  0.114 |   0.096 |   0.13  |                |
| zhen23 | S2_fixed             |       42 |  173.7 |  0.122 |   0.106 |   0.138 |                |
| zhen23 | S2_fixed             |       61 |  213.2 |  0.087 |   0.074 |   0.105 | *              |
| zhen23 | S2_fixed             |       88 |  267.9 |  0.084 |   0.072 |   0.097 |                |
| zhen23 | S2_fixed             |      127 |  344.8 |  0.08  |   0.07  |   0.092 |                |
| zhen23 | S2_fixed             |      183 |  453.6 |  0.058 |   0.049 |   0.069 |                |
| zhen23 | S2_fixed             |      263 |  605.2 |  0.05  |   0.04  |   0.058 |                |
| zhen23 | S2_fixed             |      378 |  812.8 |  0.027 |   0.02  |   0.034 |                |
| zhen23 | S2_fixed             |      544 | 1078.2 |  0.017 |   0.013 |   0.023 |                |
| zhen23 | S2_fixed             |      783 | 1459.4 |  0.011 |   0.006 |   0.015 |                |
| zhen23 | S2_fixed             |     1127 | 1924.6 |  0     |   0     |   0     |                |
| zhen23 | S3_select            |       10 |  110.8 |  0.121 |   0.107 |   0.135 |                |
| zhen23 | S3_select            |       14 |  117.9 |  0.126 |   0.112 |   0.143 |                |
| zhen23 | S3_select            |       20 |  130.6 |  0.114 |   0.1   |   0.132 |                |
| zhen23 | S3_select            |       29 |  147.9 |  0.096 |   0.085 |   0.111 |                |
| zhen23 | S3_select            |       42 |  173.7 |  0.105 |   0.093 |   0.118 |                |
| zhen23 | S3_select            |       61 |  213.2 |  0.079 |   0.067 |   0.092 | *              |
| zhen23 | S3_select            |       88 |  267.9 |  0.072 |   0.062 |   0.083 |                |
| zhen23 | S3_select            |      127 |  344.8 |  0.069 |   0.061 |   0.08  |                |
| zhen23 | S3_select            |      183 |  453.6 |  0.056 |   0.048 |   0.064 |                |
| zhen23 | S3_select            |      263 |  605.2 |  0.042 |   0.034 |   0.05  |                |
| zhen23 | S3_select            |      378 |  812.8 |  0.024 |   0.018 |   0.03  |                |
| zhen23 | S3_select            |      544 | 1078.2 |  0.014 |   0.01  |   0.018 |                |
| zhen23 | S3_select            |      783 | 1459.4 |  0.008 |   0.005 |   0.012 |                |
| zhen23 | S3_select            |     1127 | 1924.6 |  0     |   0     |   0     |                |
| zhen23 | S4_select_or_abstain |       10 |  110.8 |  0.12  |   0.107 |   0.134 |                |
| zhen23 | S4_select_or_abstain |       14 |  117.9 |  0.126 |   0.111 |   0.142 |                |
| zhen23 | S4_select_or_abstain |       20 |  130.6 |  0.114 |   0.1   |   0.132 |                |
| zhen23 | S4_select_or_abstain |       29 |  147.9 |  0.097 |   0.085 |   0.111 |                |
| zhen23 | S4_select_or_abstain |       42 |  173.7 |  0.106 |   0.094 |   0.119 |                |
| zhen23 | S4_select_or_abstain |       61 |  213.2 |  0.078 |   0.067 |   0.091 | *              |
| zhen23 | S4_select_or_abstain |       88 |  267.9 |  0.072 |   0.062 |   0.083 |                |
| zhen23 | S4_select_or_abstain |      127 |  344.8 |  0.069 |   0.06  |   0.08  |                |
| zhen23 | S4_select_or_abstain |      183 |  453.6 |  0.056 |   0.048 |   0.064 |                |
| zhen23 | S4_select_or_abstain |      263 |  605.2 |  0.042 |   0.034 |   0.05  |                |
| zhen23 | S4_select_or_abstain |      378 |  812.8 |  0.024 |   0.018 |   0.03  |                |
| zhen23 | S4_select_or_abstain |      544 | 1078.2 |  0.014 |   0.01  |   0.018 |                |
| zhen23 | S4_select_or_abstain |      783 | 1459.4 |  0.008 |   0.005 |   0.012 |                |
| zhen23 | S4_select_or_abstain |     1127 | 1924.6 |  0     |   0     |   0     |                |

### Each strategy against S1 on the same cell and budget (difference of wrong-certificate rates)

| lp     | strategy             |   cells_x_budgets |   mean_diff_vs_S1 |   share_above_S1 |   share_above_S1_by_2pts |   max_diff |
|:-------|:---------------------|------------------:|------------------:|-----------------:|-------------------------:|-----------:|
| ende23 | S2_fixed             |               210 |           -0.0081 |            0.2   |                    0.014 |      0.023 |
| ende23 | S3_select            |               210 |           -0.0155 |            0.162 |                    0.019 |      0.03  |
| ende23 | S4_select_or_abstain |               210 |           -0.0155 |            0.157 |                    0.014 |      0.027 |
| zhen23 | S2_fixed             |               210 |           -0.0009 |            0.295 |                    0.014 |      0.023 |
| zhen23 | S3_select            |               210 |           -0.0153 |            0.152 |                    0.024 |      0.037 |
| zhen23 | S4_select_or_abstain |               210 |           -0.0153 |            0.157 |                    0.024 |      0.037 |

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