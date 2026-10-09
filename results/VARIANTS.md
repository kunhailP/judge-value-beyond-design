# The 30-decision summary under variations of the audit (exploratory, pre-submission)

Percent. Informative cells: post-pilot share of uniform-sampling cost >= 0.3. mean_eval: median over cells of the mean evaluator HES over the matched best fixed judge-free base; design_wins: share of cells where the design's saving over uniform exceeds that mean; excl5/excl10: share of (cell, evaluator) pairs whose one-sided 95% bootstrap upper bound of HES is below 5% / 10%; cell_ub_lt5: share of cells where the upper bound of the MEAN evaluator is below 5%; halfwidth: median half-width of the 95% interval of a single evaluator's HES.

## Headline

| variant                         |   cells |   en_de |   zh_en |   evaluators |   pilot_share_median |   design_median |   mean_eval_pilot |   mean_eval_refit |   mean_eval_xfit |   design_wins_pilot |   design_wins_refit |   design_wins_xfit |   best_refit |
|:--------------------------------|--------:|--------:|--------:|-------------:|---------------------:|----------------:|------------------:|------------------:|-----------------:|--------------------:|--------------------:|-------------------:|-------------:|
| paper (P=50, 300 draws, 3 bins) |      33 |       4 |      29 |           34 |                 35.1 |             5.5 |              -0.1 |               1.6 |              0.4 |                93.9 |                81.8 |               90.9 |          6.8 |
| pilot 25                        |      49 |      19 |      30 |           31 |                 26.9 |             4.3 |              -2.7 |               0.7 |              0   |                98   |                85.7 |               91.8 |          5.4 |
| pilot 10                        |      60 |      30 |      30 |           31 |                 12.9 |             4.4 |              -7.7 |               0.3 |             -0   |               100   |                90   |               98.3 |          6.2 |
| four bins                       |      33 |       4 |      29 |           31 |                 35.1 |             5.5 |              -0.5 |               1.3 |              0.2 |                93.9 |                87.9 |               93.9 |          5.9 |
| 2,000 draws                     |      36 |       6 |      30 |           31 |                 37.2 |             4.6 |               0.2 |               2.3 |              0.9 |               100   |                88.9 |              100   |          6   |

## Ten evaluators with the highest system-level Pearson

| variant                         |   mean_eval_pilot_top10 |   mean_eval_refit_top10 |   mean_eval_xfit_top10 |   design_wins_pilot_top10 |   design_wins_refit_top10 |   design_wins_xfit_top10 |
|:--------------------------------|------------------------:|------------------------:|-----------------------:|--------------------------:|--------------------------:|-------------------------:|
| paper (P=50, 300 draws, 3 bins) |                     0.6 |                     2.8 |                    1.8 |                      90.9 |                      75.8 |                     78.8 |
| pilot 25                        |                    -2.4 |                     2.2 |                    0   |                      95.9 |                      75.5 |                     85.7 |
| pilot 10                        |                    -6.8 |                     0.5 |                    0   |                     100   |                      80   |                     90   |
| four bins                       |                     0.6 |                     2.6 |                    1.5 |                      93.9 |                      81.8 |                     84.8 |
| 2,000 draws                     |                     1.4 |                     3.9 |                    2.2 |                      88.9 |                      61.1 |                     77.8 |

## What the intervals rule out

| variant                         |   halfwidth_refit |   excl5_pilot |   excl10_pilot |   excl5_refit |   excl10_refit |   excl5_xfit |   excl10_xfit |   excl5_refit_top10 |   excl10_refit_top10 |   cell_ub_lt5_refit |   cell_ub_lt10_refit |
|:--------------------------------|------------------:|--------------:|---------------:|--------------:|---------------:|-------------:|--------------:|--------------------:|---------------------:|--------------------:|---------------------:|
| paper (P=50, 300 draws, 3 bins) |               6.6 |          54.2 |           86.5 |          37.4 |           70   |         49.3 |          81.9 |                15.8 |                 50   |                48.5 |                 87.9 |
| pilot 25                        |               8   |          74.5 |           89.5 |          45.1 |           66.6 |         62.1 |          82   |                28.4 |                 52.2 |                46.9 |                 77.6 |
| pilot 10                        |               8.6 |          91   |           97.6 |          43.7 |           63.1 |         63   |          83.6 |                34   |                 49.8 |                41.7 |                 70   |
| four bins                       |               6.6 |          54.3 |           85.6 |          38.3 |           71.4 |         49.3 |          81   |                15.5 |                 49.4 |                48.5 |                 87.9 |
| 2,000 draws                     |               2.3 |          89.2 |           99   |          63.7 |           93.8 |         82.2 |          98.4 |                29.4 |                 87.5 |                88.9 |                 97.2 |
