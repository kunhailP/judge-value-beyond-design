# Same-condition decomposition (informative cells; medians of shares of uniform-sampling labels)

s_D = design saving (A→C); s_B = evaluator on uniform (A→B); h = HES over dedup (C→D); s_total = 1 − D/A = s_D + (1 − s_D)h; comp_mean = mean over cells of the evaluator's component (1 − s_D)h, so s_D_mean + comp_mean = s_total_mean exactly (the figure stacks these means; medians do not add); design_gt_judge = share of cells in which the design saves more labels than the evaluator adds on dedup.

| mode   |   year | evaluator     |   cells |   s_D |   s_B |     h |   s_total |   s_D_mean |   h_mean |   comp_mean |   s_total_mean |   design_gt_judge |
|:-------|-------:|:--------------|--------:|------:|------:|------:|----------:|-----------:|---------:|------------:|---------------:|------------------:|
| cvl    |     22 | COMET-22      |      33 | 0.052 | 0.021 | 0.014 |     0.064 |      0.072 |    0.022 |       0.021 |          0.093 |             0.758 |
| cvl    |     22 | best post hoc |      33 | 0.052 | 0.033 | 0.054 |     0.11  |      0.072 |    0.062 |       0.057 |          0.129 |             0.455 |
| cvl    |     22 | mean          |      33 | 0.052 | 0.009 | 0.002 |     0.05  |      0.072 |   -0.001 |      -0.001 |          0.072 |             0.909 |
| cvl    |     22 | strongest     |      33 | 0.052 | 0.021 | 0.012 |     0.075 |      0.072 |    0.018 |       0.017 |          0.089 |             0.788 |
| cvl    |     23 | COMET-22      |      26 | 0.038 | 0.012 | 0.008 |     0.055 |      0.077 |    0.004 |       0.005 |          0.083 |             0.808 |
| cvl    |     23 | best post hoc |      26 | 0.038 | 0.039 | 0.034 |     0.088 |      0.077 |    0.035 |       0.034 |          0.112 |             0.577 |
| cvl    |     23 | mean          |      26 | 0.038 | 0.005 | 0.003 |     0.047 |      0.077 |    0     |       0.002 |          0.079 |             0.923 |
| cvl    |     23 | strongest     |      26 | 0.038 | 0.026 | 0.023 |     0.07  |      0.077 |    0.023 |       0.023 |          0.101 |             0.654 |
| cvq    |     22 | COMET-22      |      33 | 0.052 | 0.046 | 0.029 |     0.09  |      0.072 |    0.044 |       0.04  |          0.113 |             0.606 |
| cvq    |     22 | best post hoc |      33 | 0.052 | 0.049 | 0.068 |     0.122 |      0.072 |    0.077 |       0.072 |          0.144 |             0.394 |
| cvq    |     22 | mean          |      33 | 0.052 | 0.021 | 0.018 |     0.071 |      0.072 |    0.02  |       0.018 |          0.091 |             0.788 |
| cvq    |     22 | strongest     |      33 | 0.052 | 0.05  | 0.037 |     0.096 |      0.072 |    0.051 |       0.047 |          0.12  |             0.667 |
| cvq    |     23 | COMET-22      |      26 | 0.038 | 0.033 | 0.031 |     0.073 |      0.077 |    0.034 |       0.032 |          0.109 |             0.615 |
| cvq    |     23 | best post hoc |      26 | 0.038 | 0.069 | 0.062 |     0.112 |      0.077 |    0.07  |       0.066 |          0.143 |             0.308 |
| cvq    |     23 | mean          |      26 | 0.038 | 0.029 | 0.025 |     0.073 |      0.077 |    0.028 |       0.026 |          0.103 |             0.692 |
| cvq    |     23 | strongest     |      26 | 0.038 | 0.055 | 0.047 |     0.093 |      0.077 |    0.054 |       0.05  |          0.128 |             0.423 |