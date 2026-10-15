# Known-zero differences and the coverage of the refitted bound: one WMT23 cell re-run with the fixed code

Cell: WMT23 en-de, GPT4-5shot vs ONLINE-W (pair 01), pilot 50, eps 0.01 / 0.02, 300 simulated audits, same seed, 42 metric variants + chrF
(`results/mt/mt_ende23_m2_p50_pair2301_*` before, `*_pair23z01_*` after).
The 300-audit WMT23 runs (`pair23`) and the original WMT22 runs (`pairmtme`) predate the fix of 2026-10-10 in `code/110_unit_audit.py`
(`--zero_known`, default on) that sets the evaluator's difference to 0 on items whose outputs are identical, as the estimator assumes;
real evaluators score identical strings slightly differently. The 2,000-audit WMT23 runs (`pair23n`), the boundary runs (`pair23b`)
and the WMT22 re-run (`pairmtmez`) use the fixed code.

| run | eps | strategy | coverage, all budgets | coverage, smallest budget | coverage at J50 | wrong at J50 | J50(S1) | J50(S2) | J50(S3) |
|---|---|---|---|---|---|---|---|---|---|
| before the fix | 0.01 | S1_design | 0.902 | 0.860 | 0.923 | 0.000 | 530.3 | 513.0 | 502.6 |
| before the fix | 0.01 | S2_fixed | 0.862 | 0.430 | 0.917 | 0.000 | 530.3 | 513.0 | 502.6 |
| before the fix | 0.01 | S3_select | 0.873 | 0.643 | 0.920 | 0.000 | 530.3 | 513.0 | 502.6 |
| before the fix | 0.01 | S4_select_or_abstain | 0.874 | 0.650 | 0.920 | 0.000 | 530.3 | 513.0 | 502.6 |
| before the fix | 0.02 | S1_design | 0.902 | 0.860 | 0.897 | 0.000 | 305.2 | 293.0 | 307.1 |
| before the fix | 0.02 | S2_fixed | 0.862 | 0.430 | 0.887 | 0.000 | 305.2 | 293.0 | 307.1 |
| before the fix | 0.02 | S3_select | 0.873 | 0.643 | 0.877 | 0.000 | 305.2 | 293.0 | 307.1 |
| before the fix | 0.02 | S4_select_or_abstain | 0.874 | 0.650 | 0.877 | 0.000 | 305.2 | 293.0 | 307.1 |
| after the fix | 0.01 | S1_design | 0.902 | 0.860 | 0.923 | 0.000 | 530.3 | 513.0 | 501.4 |
| after the fix | 0.01 | S2_fixed | 0.903 | 0.863 | 0.917 | 0.000 | 530.3 | 513.0 | 501.4 |
| after the fix | 0.01 | S3_select | 0.899 | 0.847 | 0.920 | 0.000 | 530.3 | 513.0 | 501.4 |
| after the fix | 0.01 | S4_select_or_abstain | 0.899 | 0.847 | 0.920 | 0.000 | 530.3 | 513.0 | 501.4 |
| after the fix | 0.02 | S1_design | 0.902 | 0.860 | 0.897 | 0.000 | 305.2 | 293.0 | 306.9 |
| after the fix | 0.02 | S2_fixed | 0.903 | 0.863 | 0.887 | 0.000 | 305.2 | 293.0 | 306.9 |
| after the fix | 0.02 | S3_select | 0.899 | 0.847 | 0.877 | 0.000 | 305.2 | 293.0 | 306.9 |
| after the fix | 0.02 | S4_select_or_abstain | 0.899 | 0.847 | 0.877 | 0.000 | 305.2 | 293.0 | 306.9 |

Reading: J50 is unchanged to the first decimal (S1 and S2 identical, S3 within one label), so the fix does not change the savings;
it removes the under-coverage of the refitted bound at the smallest budgets (S2 0.43 -> 0.86 at nominal 0.90), which was the bias term
lambda x (sum of D-hat over unsampled known-zero items), not a property of refitting.
