# Human noise ceiling for decision-level rho (WMT22 en->de, 3-rater re-annotation; exploratory)

Top-6 systems: Online-W, Online-B, JDExploreAcademy, Online-A, Online-G, Online-Y; 15 pairs; two distinct raters per segment, B = 200 random rater pairs.

## Over the 15 pairs

| subset    |   reliability_median |   reliability_min |   reliability_max |   rho_ceiling_median |   rho_ceiling_min |   rho_ceiling_max |
|:----------|---------------------:|------------------:|------------------:|---------------------:|------------------:|------------------:|
| all       |                0.352 |             0.306 |             0.409 |                0.593 |             0.553 |             0.639 |
| differing |                0.349 |             0.306 |             0.407 |                0.591 |             0.553 |             0.638 |

## Per pair

| pair                         | subset    |   segments |   reliability |    lo |    hi |   rho_ceiling |
|:-----------------------------|:----------|-----------:|--------------:|------:|------:|--------------:|
| Online-W vs Online-B         | all       |       1315 |         0.409 | 0.359 | 0.464 |         0.639 |
| Online-W vs Online-B         | differing |       1125 |         0.407 | 0.357 | 0.462 |         0.638 |
| Online-W vs JDExploreAcademy | all       |       1315 |         0.406 | 0.355 | 0.468 |         0.637 |
| Online-W vs JDExploreAcademy | differing |       1124 |         0.403 | 0.352 | 0.466 |         0.635 |
| Online-W vs Online-A         | all       |       1315 |         0.405 | 0.349 | 0.468 |         0.636 |
| Online-W vs Online-A         | differing |       1133 |         0.399 | 0.343 | 0.463 |         0.632 |
| Online-W vs Online-G         | all       |       1315 |         0.403 | 0.341 | 0.463 |         0.635 |
| Online-W vs Online-G         | differing |       1146 |         0.398 | 0.336 | 0.458 |         0.631 |
| Online-W vs Online-Y         | all       |       1315 |         0.39  | 0.347 | 0.441 |         0.624 |
| Online-W vs Online-Y         | differing |       1213 |         0.387 | 0.344 | 0.438 |         0.622 |
| Online-B vs JDExploreAcademy | all       |       1315 |         0.341 | 0.289 | 0.398 |         0.584 |
| Online-B vs JDExploreAcademy | differing |       1007 |         0.341 | 0.289 | 0.398 |         0.584 |
| Online-B vs Online-A         | all       |       1315 |         0.366 | 0.309 | 0.421 |         0.605 |
| Online-B vs Online-A         | differing |       1004 |         0.363 | 0.306 | 0.418 |         0.602 |
| Online-B vs Online-G         | all       |       1315 |         0.345 | 0.286 | 0.417 |         0.587 |
| Online-B vs Online-G         | differing |       1003 |         0.34  | 0.28  | 0.412 |         0.583 |
| Online-B vs Online-Y         | all       |       1315 |         0.322 | 0.255 | 0.386 |         0.568 |
| Online-B vs Online-Y         | differing |       1047 |         0.318 | 0.25  | 0.382 |         0.564 |
| JDExploreAcademy vs Online-A | all       |       1315 |         0.32  | 0.264 | 0.385 |         0.566 |
| JDExploreAcademy vs Online-A | differing |       1036 |         0.318 | 0.262 | 0.383 |         0.564 |
| JDExploreAcademy vs Online-G | all       |       1315 |         0.352 | 0.293 | 0.423 |         0.593 |
| JDExploreAcademy vs Online-G | differing |       1046 |         0.349 | 0.291 | 0.421 |         0.591 |
| JDExploreAcademy vs Online-Y | all       |       1315 |         0.358 | 0.302 | 0.41  |         0.598 |
| JDExploreAcademy vs Online-Y | differing |       1131 |         0.356 | 0.301 | 0.409 |         0.597 |
| Online-A vs Online-G         | all       |       1315 |         0.306 | 0.215 | 0.38  |         0.553 |
| Online-A vs Online-G         | differing |        963 |         0.306 | 0.214 | 0.38  |         0.553 |
| Online-A vs Online-Y         | all       |       1315 |         0.31  | 0.236 | 0.369 |         0.557 |
| Online-A vs Online-Y         | differing |       1055 |         0.31  | 0.235 | 0.369 |         0.557 |
| Online-G vs Online-Y         | all       |       1315 |         0.306 | 0.234 | 0.365 |         0.553 |
| Online-G vs Online-Y         | differing |       1050 |         0.306 | 0.234 | 0.366 |         0.553 |
