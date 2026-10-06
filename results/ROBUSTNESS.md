# Robustness of the estimation tax (exploratory, post-lock)

HES of each evaluator over its own judge-free base design, by how the coefficient is set (mean over evaluators;
MT: 8 strongest metric variants + COMET-22, Qwen3-8B, Mistral-7B; Arena: Qwen3-8B, Mistral-7B, longer).

## J50

|                                  |   pilot |   refit |   xfit |   oracle |
|:---------------------------------|--------:|--------:|-------:|---------:|
| ('arena', 'arena_10', 'uniform') |   0.052 |   0.048 |  0.038 |    0.052 |
| ('arena', 'arena_11', 'uniform') |  -0.002 |   0.007 | -0.001 |    0.005 |
| ('arena', 'arena_12', 'uniform') |   0.006 |   0.036 |  0.01  |    0.03  |
| ('arena', 'arena_13', 'uniform') |  -0.005 |   0.005 | -0.009 |    0.003 |
| ('arena', 'arena_14', 'uniform') |  -0.002 |   0.018 |  0     |    0.008 |
| ('arena', 'arena_15', 'uniform') |   0.017 |   0.027 |  0.015 |    0.03  |
| ('mt', 'mt_ende', 'dedup')       |   0.008 |   0.124 | -0.013 |  nan     |
| ('mt', 'mt_ende', 'weighted')    |   0.004 |   0.1   | -0.013 |    0.067 |
| ('mt', 'mt_zhen', 'dedup')       |  -0.018 |   0.025 |  0.023 |  nan     |
| ('mt', 'mt_zhen', 'weighted')    |  -0.004 |   0.02  |  0.011 |    0.013 |

|                       |   tax_pilot |   tax_xfit |   tax_refit |
|:----------------------|------------:|-----------:|------------:|
| ('arena', 'arena_10') |      -0     |      0.014 |       0.004 |
| ('arena', 'arena_11') |       0.007 |      0.006 |      -0.002 |
| ('arena', 'arena_12') |       0.023 |      0.019 |      -0.006 |
| ('arena', 'arena_13') |       0.008 |      0.013 |      -0.001 |
| ('arena', 'arena_14') |       0.01  |      0.008 |      -0.011 |
| ('arena', 'arena_15') |       0.013 |      0.016 |       0.003 |
| ('mt', 'mt_ende')     |       0.063 |      0.08  |      -0.033 |
| ('mt', 'mt_zhen')     |       0.018 |      0.003 |      -0.006 |

## J80

|                                  |   pilot |   refit |   xfit |   oracle |
|:---------------------------------|--------:|--------:|-------:|---------:|
| ('arena', 'arena_10', 'uniform') |  -0.005 |   0.007 |  0.003 |    0.005 |
| ('arena', 'arena_11', 'uniform') |  -0.013 |  -0.006 | -0.008 |   -0.001 |
| ('arena', 'arena_12', 'uniform') |  -0.001 |   0.005 |  0.005 |    0.005 |
| ('arena', 'arena_13', 'uniform') |  -0.027 |  -0.003 | -0.009 |    0.004 |
| ('arena', 'arena_14', 'uniform') |   0.052 |   0.044 |  0.021 |    0.023 |
| ('arena', 'arena_15', 'uniform') |  -0.006 |  -0.03  | -0.009 |   -0.041 |
| ('mt', 'mt_ende', 'dedup')       |   0.003 |   0.044 |  0.007 |  nan     |
| ('mt', 'mt_ende', 'weighted')    |   0.001 |   0.028 |  0.008 |    0.025 |
| ('mt', 'mt_zhen', 'dedup')       |   0.012 |   0.032 |  0.029 |  nan     |
| ('mt', 'mt_zhen', 'weighted')    |   0.005 |   0.021 |  0.02  |    0.019 |

|                       |   tax_pilot |   tax_xfit |   tax_refit |
|:----------------------|------------:|-----------:|------------:|
| ('arena', 'arena_10') |       0.01  |      0.003 |      -0.001 |
| ('arena', 'arena_11') |       0.011 |      0.007 |       0.005 |
| ('arena', 'arena_12') |       0.006 |      0     |       0     |
| ('arena', 'arena_13') |       0.031 |      0.013 |       0.007 |
| ('arena', 'arena_14') |      -0.029 |      0.002 |      -0.021 |
| ('arena', 'arena_15') |      -0.035 |     -0.031 |      -0.01  |
| ('mt', 'mt_ende')     |       0.025 |      0.017 |      -0.003 |
| ('mt', 'mt_zhen')     |       0.014 |     -0     |      -0.002 |

## Best evaluator on the best fixed judge-free base (matched base, J50, pilot / xfit coefficient)

|                    |   best_pilot |   best_xfit |   best_refit |
|:-------------------|-------------:|------------:|-------------:|
| ('arena_10', 0.05) |        0.105 |       0.076 |        0.083 |
| ('arena_10', 0.1)  |        0.032 |       0.052 |        0.047 |
| ('arena_11', 0.05) |        0.009 |       0.01  |        0.021 |
| ('arena_11', 0.1)  |       -0.003 |      -0.003 |        0.011 |
| ('arena_12', 0.05) |        0.029 |       0.024 |        0.035 |
| ('arena_12', 0.1)  |        0.022 |       0.026 |        0.079 |
| ('arena_13', 0.05) |        0.001 |       0.001 |        0.015 |
| ('arena_13', 0.1)  |        0.019 |       0.013 |        0.027 |
| ('arena_14', 0.05) |       -0.011 |      -0.003 |        0.009 |
| ('arena_14', 0.1)  |        0.032 |       0.019 |        0.036 |
| ('arena_15', 0.05) |        0.057 |       0.046 |        0.058 |
| ('arena_15', 0.1)  |        0.029 |       0.011 |        0.044 |
| ('mt_ende', 0.01)  |        0.071 |       0.044 |        0.116 |
| ('mt_ende', 0.02)  |        0.021 |      -0.013 |        0.156 |
| ('mt_zhen', 0.01)  |        0.073 |       0.154 |        0.154 |
| ('mt_zhen', 0.02)  |       -0.005 |       0.007 |        0.015 |