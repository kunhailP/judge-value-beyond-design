# Sensitivity of the 30-decision summary (exploratory)

## Identical strings share the mean of their ratings (paper)

Percent; per cell the mean evaluator HES is the mean over the evaluator set, then the median over cells; design_wins = share of cells where the design's saving exceeds that mean.

| evaluators         |   t |   cells |   en_de |   zh_en |   design_median |   mean_eval_pilot |   design_wins_pilot |   mean_eval_refit |   design_wins_refit |   mean_eval_xfit |   design_wins_xfit |
|:-------------------|----:|--------:|--------:|--------:|----------------:|------------------:|--------------------:|------------------:|--------------------:|-----------------:|-------------------:|
| all 34             | 0   |      60 |      30 |      30 |             0.7 |               0   |                  97 |               0   |                  90 |              0   |                 95 |
| all 34             | 0.2 |      34 |       4 |      30 |             5.4 |              -0.1 |                  94 |               1.5 |                  82 |              0.4 |                 91 |
| all 34             | 0.3 |      33 |       4 |      29 |             5.5 |              -0.1 |                  94 |               1.6 |                  82 |              0.4 |                 91 |
| all 34             | 0.4 |      33 |       4 |      29 |             5.5 |              -0.1 |                  94 |               1.6 |                  82 |              0.4 |                 91 |
| all 34             | 0.5 |      30 |       3 |      27 |             5.8 |              -0.1 |                  93 |               1.5 |                  83 |              0.4 |                 90 |
| all 34             | 0.6 |      23 |       1 |      22 |             5.2 |               0.1 |                  91 |               1.7 |                  78 |              0.5 |                 87 |
| top-10 by system r | 0   |      60 |      30 |      30 |             0.7 |               0   |                  95 |               0   |                  87 |              0   |                 88 |
| top-10 by system r | 0.2 |      34 |       4 |      30 |             5.4 |               0.6 |                  91 |               2.7 |                  76 |              1.7 |                 79 |
| top-10 by system r | 0.3 |      33 |       4 |      29 |             5.5 |               0.6 |                  91 |               2.8 |                  76 |              1.8 |                 79 |
| top-10 by system r | 0.4 |      33 |       4 |      29 |             5.5 |               0.6 |                  91 |               2.8 |                  76 |              1.8 |                 79 |
| top-10 by system r | 0.5 |      30 |       3 |      27 |             5.8 |               0.7 |                  90 |               2.7 |                  80 |              1.7 |                 80 |
| top-10 by system r | 0.6 |      23 |       1 |      22 |             5.2 |               1.5 |                  87 |               3.5 |                  74 |              2.3 |                 74 |

## Identical strings share one random rating (IDENT=pick)

Percent; per cell the mean evaluator HES is the mean over the evaluator set, then the median over cells; design_wins = share of cells where the design's saving exceeds that mean.

| evaluators         |   t |   cells |   en_de |   zh_en |   design_median |   mean_eval_pilot |   design_wins_pilot |   mean_eval_refit |   design_wins_refit |   mean_eval_xfit |   design_wins_xfit |
|:-------------------|----:|--------:|--------:|--------:|----------------:|------------------:|--------------------:|------------------:|--------------------:|-----------------:|-------------------:|
| all 34             | 0   |      60 |      30 |      30 |             0.9 |               0   |                  95 |               0.1 |                  90 |              0   |                 95 |
| all 34             | 0.2 |      34 |       4 |      30 |             5   |              -0.6 |                  91 |               1.3 |                  85 |              0.1 |                 91 |
| all 34             | 0.3 |      33 |       4 |      29 |             5.2 |              -0.6 |                  91 |               1.4 |                  85 |              0.1 |                 91 |
| all 34             | 0.4 |      33 |       4 |      29 |             5.2 |              -0.6 |                  91 |               1.4 |                  85 |              0.1 |                 91 |
| all 34             | 0.5 |      30 |       4 |      26 |             5.4 |              -0.6 |                  90 |               1.4 |                  87 |              0.4 |                 90 |
| all 34             | 0.6 |      23 |       2 |      21 |             4.8 |              -0.6 |                  91 |               1.3 |                  91 |              0.4 |                 91 |
| top-10 by system r | 0   |      60 |      30 |      30 |             0.9 |               0   |                  95 |               0.2 |                  83 |              0   |                 92 |
| top-10 by system r | 0.2 |      34 |       4 |      30 |             5   |               0.2 |                  91 |               2.7 |                  74 |              0.8 |                 88 |
| top-10 by system r | 0.3 |      33 |       4 |      29 |             5.2 |               0.3 |                  91 |               2.8 |                  73 |              0.9 |                 88 |
| top-10 by system r | 0.4 |      33 |       4 |      29 |             5.2 |               0.3 |                  91 |               2.8 |                  73 |              0.9 |                 88 |
| top-10 by system r | 0.5 |      30 |       4 |      26 |             5.4 |               0.4 |                  90 |               2.7 |                  77 |              1   |                 90 |
| top-10 by system r | 0.6 |      23 |       2 |      21 |             4.8 |               0.4 |                  91 |               2.4 |                  78 |              1   |                 91 |

## Locked cells: design saving over uniform (J50), mean vs one random rating per identical-string group

(100 x fraction; pick: three seeds of the random rating, mean/min/max)

|                        |   ('dedup', 'mean') |   ('dedup', 'min') |   ('dedup', 'max') |   ('weighted', 'mean') |   ('weighted', 'min') |   ('weighted', 'max') |   ('best_fixed', 'mean') |   ('best_fixed', 'min') |   ('best_fixed', 'max') |
|:-----------------------|--------------------:|-------------------:|-------------------:|-----------------------:|----------------------:|----------------------:|-------------------------:|------------------------:|------------------------:|
| ('ende', 0.01, 'mean') |                13.4 |               13.4 |               13.4 |                   15.9 |                  15.9 |                  15.9 |                     15.9 |                    15.9 |                    15.9 |
| ('ende', 0.01, 'pick') |                16.6 |               15.5 |               17.7 |                   16.8 |                  14.9 |                  18.4 |                     17   |                    15.5 |                    18.4 |
| ('ende', 0.02, 'mean') |                 5.6 |                5.6 |                5.6 |                    9   |                   9   |                   9   |                      9   |                     9   |                     9   |
| ('ende', 0.02, 'pick') |                 6.5 |                5.9 |                7   |                    8.5 |                   7.9 |                   8.8 |                      8.5 |                     7.9 |                     8.8 |
| ('zhen', 0.01, 'mean') |                 8.4 |                8.4 |                8.4 |                    7.5 |                   7.5 |                   7.5 |                      8.4 |                     8.4 |                     8.4 |
| ('zhen', 0.01, 'pick') |                 8.4 |                7.2 |               10   |                    7.8 |                   6   |                   9.6 |                      9.2 |                     7.9 |                    10   |
| ('zhen', 0.02, 'mean') |                 8.5 |                8.5 |                8.5 |                    6.1 |                   6.1 |                   6.1 |                      8.5 |                     8.5 |                     8.5 |
| ('zhen', 0.02, 'pick') |                11   |                7.5 |               13.9 |                   12   |                  11   |                  13.8 |                     12.2 |                    11   |                    13.9 |
