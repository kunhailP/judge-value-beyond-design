# Robustness of the estimation tax (exploratory, post-lock)

HES of each evaluator over its own judge-free base design, by how the coefficient is set (mean over evaluators;
MT: 8 strongest metric variants + COMET-22, Qwen3-8B, Mistral-7B; Arena: Qwen3-8B, Mistral-7B, longer).

## J50

|                                  |   pilot |   refit |    xfit |   refit_ht |   xfit_ht |   oracle |
|:---------------------------------|--------:|--------:|--------:|-----------:|----------:|---------:|
| ('arena', 'arena_10', 'uniform') |   0.052 | nan     | nan     |      0.048 |     0.038 |    0.052 |
| ('arena', 'arena_11', 'uniform') |  -0.002 | nan     | nan     |      0.007 |    -0.001 |    0.005 |
| ('arena', 'arena_12', 'uniform') |   0.006 | nan     | nan     |      0.036 |     0.01  |    0.03  |
| ('arena', 'arena_13', 'uniform') |  -0.005 | nan     | nan     |      0.005 |    -0.009 |    0.003 |
| ('arena', 'arena_14', 'uniform') |  -0.002 | nan     | nan     |      0.018 |     0     |    0.008 |
| ('arena', 'arena_15', 'uniform') |   0.017 | nan     | nan     |      0.027 |     0.015 |    0.03  |
| ('mt', 'mt_ende', 'dedup')       |   0.008 |   0.072 |   0.017 |      0.124 |    -0.013 |  nan     |
| ('mt', 'mt_ende', 'weighted')    |   0.004 |   0.068 |   0.016 |      0.1   |    -0.013 |    0.067 |
| ('mt', 'mt_zhen', 'dedup')       |  -0.018 |   0.023 |   0.019 |      0.025 |     0.023 |  nan     |
| ('mt', 'mt_zhen', 'weighted')    |  -0.004 |   0.02  |   0.011 |      0.02  |     0.011 |    0.013 |

|                       |   tax_pilot |   tax_xfit |   tax_refit |
|:----------------------|------------:|-----------:|------------:|
| ('arena', 'arena_10') |      -0     |    nan     |     nan     |
| ('arena', 'arena_11') |       0.007 |    nan     |     nan     |
| ('arena', 'arena_12') |       0.023 |    nan     |     nan     |
| ('arena', 'arena_13') |       0.008 |    nan     |     nan     |
| ('arena', 'arena_14') |       0.01  |    nan     |     nan     |
| ('arena', 'arena_15') |       0.013 |    nan     |     nan     |
| ('mt', 'mt_ende')     |       0.063 |      0.051 |      -0.001 |
| ('mt', 'mt_zhen')     |       0.018 |      0.002 |      -0.007 |

## J80

|                                  |   pilot |   refit |    xfit |   refit_ht |   xfit_ht |   oracle |
|:---------------------------------|--------:|--------:|--------:|-----------:|----------:|---------:|
| ('arena', 'arena_10', 'uniform') |  -0.005 | nan     | nan     |      0.007 |     0.003 |    0.005 |
| ('arena', 'arena_11', 'uniform') |  -0.013 | nan     | nan     |     -0.006 |    -0.008 |   -0.001 |
| ('arena', 'arena_12', 'uniform') |  -0.001 | nan     | nan     |      0.005 |     0.005 |    0.005 |
| ('arena', 'arena_13', 'uniform') |  -0.027 | nan     | nan     |     -0.003 |    -0.009 |    0.004 |
| ('arena', 'arena_14', 'uniform') |   0.052 | nan     | nan     |      0.044 |     0.021 |    0.023 |
| ('arena', 'arena_15', 'uniform') |  -0.006 | nan     | nan     |     -0.03  |    -0.009 |   -0.041 |
| ('mt', 'mt_ende', 'dedup')       |   0.003 |   0.049 |   0.023 |      0.044 |     0.007 |  nan     |
| ('mt', 'mt_ende', 'weighted')    |   0.001 |   0.025 |   0.015 |      0.028 |     0.008 |    0.025 |
| ('mt', 'mt_zhen', 'dedup')       |   0.012 |   0.032 |   0.028 |      0.032 |     0.029 |  nan     |
| ('mt', 'mt_zhen', 'weighted')    |   0.005 |   0.022 |   0.023 |      0.021 |     0.02  |    0.019 |

|                       |   tax_pilot |   tax_xfit |   tax_refit |
|:----------------------|------------:|-----------:|------------:|
| ('arena', 'arena_10') |       0.01  |    nan     |     nan     |
| ('arena', 'arena_11') |       0.011 |    nan     |     nan     |
| ('arena', 'arena_12') |       0.006 |    nan     |     nan     |
| ('arena', 'arena_13') |       0.031 |    nan     |     nan     |
| ('arena', 'arena_14') |      -0.029 |    nan     |     nan     |
| ('arena', 'arena_15') |      -0.035 |    nan     |     nan     |
| ('mt', 'mt_ende')     |       0.025 |      0.01  |      -0     |
| ('mt', 'mt_zhen')     |       0.014 |     -0.004 |      -0.003 |

## Best evaluator on the best fixed judge-free base (matched base, J50, pilot / xfit coefficient)

|                    |   best_pilot |   best_refit |   mean_refit |   best_xfit |   mean_xfit |
|:-------------------|-------------:|-------------:|-------------:|------------:|------------:|
| ('arena_10', 0.05) |        0.105 |      nan     |      nan     |     nan     |     nan     |
| ('arena_10', 0.1)  |        0.032 |      nan     |      nan     |     nan     |     nan     |
| ('arena_11', 0.05) |        0.009 |      nan     |      nan     |     nan     |     nan     |
| ('arena_11', 0.1)  |       -0.003 |      nan     |      nan     |     nan     |     nan     |
| ('arena_12', 0.05) |        0.029 |      nan     |      nan     |     nan     |     nan     |
| ('arena_12', 0.1)  |        0.022 |      nan     |      nan     |     nan     |     nan     |
| ('arena_13', 0.05) |        0.001 |      nan     |      nan     |     nan     |     nan     |
| ('arena_13', 0.1)  |        0.019 |      nan     |      nan     |     nan     |     nan     |
| ('arena_14', 0.05) |       -0.011 |      nan     |      nan     |     nan     |     nan     |
| ('arena_14', 0.1)  |        0.032 |      nan     |      nan     |     nan     |     nan     |
| ('arena_15', 0.05) |        0.057 |      nan     |      nan     |     nan     |     nan     |
| ('arena_15', 0.1)  |        0.029 |      nan     |      nan     |     nan     |     nan     |
| ('mt_ende', 0.01)  |        0.071 |        0.106 |        0.069 |       0.083 |       0.035 |
| ('mt_ende', 0.02)  |        0.021 |        0.121 |        0.067 |       0.036 |      -0.003 |
| ('mt_zhen', 0.01)  |        0.073 |        0.154 |        0.048 |       0.121 |       0.051 |
| ('mt_zhen', 0.02)  |       -0.005 |        0.01  |       -0.003 |       0.003 |      -0.012 |