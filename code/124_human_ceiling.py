#!/usr/bin/env python3
"""Exploratory (post-review): a human noise ceiling for decision-level rho on WMT22 en->de.

The en->de 3-rater re-annotation (mqm_generalMT2022_ende.3ratingsPerSegment.tsv) gives three independent MQM ratings
per segment and system. For every pair of the top-6 systems (the 15 en->de two-system decisions) and every segment, two
distinct raters who rated both outputs give two paired differences D1, D2 (utility u = -min(MQM,25)/25, as everywhere).
corr(D1, D2) is the test-retest reliability of a single rating's paired difference; an evaluator that predicted the
true difference perfectly would reach rho = sqrt(reliability) against a single rating, which is what the audits label
with. Reported over all segments with D = 0 where the two outputs are identical (the paper's estimand) and over
segments with differing outputs only; rater pairs drawn at random (B = 200 repetitions, median and 2.5/97.5% range).
Writes results/HUMAN_CEILING.md.
"""
import csv, os, sys
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from paths import DATA
from mt_common import mqm_weight, utility, strip_marks, load_pool

DL = f"{DATA}/mt/dl/wmt-mqm-human-evaluation/generalMT2022"
R = os.path.join(HERE, "..", "results")
B = 200


def main():
    t = pd.read_csv(f"{DL}/ende/mqm_generalMT2022_ende.3ratingsPerSegment.tsv", sep="\t", quoting=csv.QUOTE_NONE,
                    keep_default_na=False, dtype=str)
    t["w"] = [mqm_weight(s, c) for s, c in zip(t.severity, t.category)]
    t["hyp"] = t.candidate.map(strip_marks)
    key = ["document_id", "doc_segment_id"]
    r = t.groupby(key + ["system_id", "rater_id"]).agg(w=("w", "sum"), hyp=("hyp", "first")).reset_index()
    r["u"] = utility(r.w)
    pool = load_pool("ende"); pool = pool[~pool.system.str.endswith("_bestmbr")]
    top6 = pool.groupby("system").u.mean().sort_values(ascending=False).index[:6].tolist()
    U = r.pivot_table(index=key + ["rater_id"], columns="system_id", values="u")
    H = r.pivot_table(index=key, columns="system_id", values="hyp", aggfunc="first")
    rng = np.random.default_rng(20261006)
    rows = []
    for i in range(6):
        for j in range(i + 1, 6):
            a, b = top6[i], top6[j]
            d = (U[a] - U[b]).dropna().rename("D").reset_index()
            ident = (H[a] == H[b]).rename("ident").reset_index()
            d = d.merge(ident, on=key)
            d.loc[d.ident, "D"] = 0.0
            g = [x.D.to_numpy() for _, x in d.groupby(key) if len(x) >= 2]
            idn = np.array([x.ident.iloc[0] for _, x in d.groupby(key) if len(x) >= 2])
            res = {"all": [], "differing": []}
            for _ in range(B):
                pick = np.array([rng.choice(x, 2, replace=False) for x in g])
                for name, m in (("all", np.ones(len(g), bool)), ("differing", ~idn)):
                    res[name].append(np.corrcoef(pick[m, 0], pick[m, 1])[0, 1])
            for name, v in res.items():
                v = np.array(v)
                rows.append(dict(pair=f"{a} vs {b}", subset=name, segments=int(len(g) if name == "all" else (~idn).sum()),
                                 reliability=np.median(v), lo=np.quantile(v, .025), hi=np.quantile(v, .975),
                                 rho_ceiling=np.sqrt(max(np.median(v), 0))))
    T = pd.DataFrame(rows)
    S = T.groupby("subset").agg(reliability_median=("reliability", "median"), reliability_min=("reliability", "min"),
                                reliability_max=("reliability", "max"), rho_ceiling_median=("rho_ceiling", "median"),
                                rho_ceiling_min=("rho_ceiling", "min"), rho_ceiling_max=("rho_ceiling", "max")).round(3)
    md = ["# Human noise ceiling for decision-level rho (WMT22 en->de, 3-rater re-annotation; exploratory)", "",
          f"Top-6 systems: {', '.join(top6)}; 15 pairs; two distinct raters per segment, B = {B} random rater pairs.", "",
          "## Over the 15 pairs", "", S.to_markdown(), "", "## Per pair", "", T.round(3).to_markdown(index=False), ""]
    open(f"{R}/HUMAN_CEILING.md", "w").write("\n".join(md)); print("\n".join(md))


if __name__ == "__main__":
    main()
