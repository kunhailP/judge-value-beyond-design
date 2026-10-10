# S2 (fixed mtme_COMET-refA) vs S3 (pilot selection by rho), cvq; results/mt/mt_*23_m2_p50_boundary_pair23b??

G = 1 - J50(S3)/J50(S2) per cell, paired over audits (300 per cell, 200 bootstrap draws); positive = selection cheaper. Margin of practical equivalence: 2% (lock v1.2 addendum).

## Pooled (mean over cells; cluster bootstrap over decisions)

| cells   | lp     |   n |   G_mean |   G_lo |   G_hi |   share_G_pos |   D2_mean |   D2_lo |   D2_hi |   D3_mean |   D3_lo |   D3_hi | verdict   |
|:--------|:-------|----:|---------:|-------:|-------:|--------------:|----------:|--------:|--------:|----------:|--------:|--------:|:----------|
| all 60  | pooled |  30 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |
| all 60  | ende23 |  15 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |
| all 60  | zhen23 |  15 |      nan |    nan |    nan |             0 |       nan |     nan |     nan |       nan |     nan |     nan | undecided |

## Per-cell interval widths (informative cells, medians)

G: nan; D2 (S2 vs S1): nan; D3 (S3 vs S1): nan
cells with G interval above 0: 0/0; below 0: 0/0; D2 above 0: 0; D3 above 0: 0

## Coverage of the chosen arm's upper bound (nominal 0.90) and wrong certificates, informative cells

| strategy   | ('cover_all', 'mean')   | ('cover_all', 'min')   | ('cover_all', 'max')   | ('cover_min_budget', 'mean')   | ('cover_min_budget', 'min')   | ('cover_min_budget', 'max')   | ('cover_at_J50', 'mean')   | ('cover_at_J50', 'min')   | ('cover_at_J50', 'max')   | ('wrong_at_J50', 'mean')   | ('wrong_at_J50', 'min')   | ('wrong_at_J50', 'max')   | ('wrong_max', 'mean')   | ('wrong_max', 'min')   | ('wrong_max', 'max')   | ('wrong_mean', 'mean')   | ('wrong_mean', 'min')   | ('wrong_mean', 'max')   |
|------------|-------------------------|------------------------|------------------------|--------------------------------|-------------------------------|-------------------------------|----------------------------|---------------------------|---------------------------|----------------------------|---------------------------|---------------------------|-------------------------|------------------------|------------------------|--------------------------|-------------------------|-------------------------|

## Wrong-certificate rate by post-pilot budget, mean over all 30 cells (boundary runs: type-I error, nominal 0.10)

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