"""Build /root/naacl_data/mt/{lp}/pool.parquet from Google's WMT22 MQM data.

Run:  python3 -I /root/judge-audit-certification/06_naacl/code/mt_build_pool.py
Inputs (untrusted, read-only): /root/naacl_data/mt/dl/wmt-mqm-human-evaluation/generalMT2022/{lp}/
  mqm_generalMT2022_{lp}.tsv               error-level MQM annotations (scored here)
  mqm_generalMT2022_{lp}.avg_seg_scores.tsv clean hyp / source / reference(refA) text, global seg ids
  (ende only) mqm_generalMT2022_ende.3ratingsPerSegment.tsv  3-rater re-annotation -> mqm_3r, u_3r
"""
import csv
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

sys.path.insert(0, "/root/judge-audit-certification/06_naacl/code")
from mt_common import MT_ROOT, LPS, mqm_weight, utility, strip_marks, chrf  # noqa: E402

def norm(x):
    import re
    return re.sub(r"[\s,，]", "", x)


DL = f"{MT_ROOT}/dl/wmt-mqm-human-evaluation/generalMT2022"
REF_SYS = {"refA", "refB"}
MIN_COVER = 0.99


def read_avg(path):
    """Robust reader (one zh-en hyp contains a literal tab): 8 cols, hyp = middle."""
    with open(path, encoding="utf8") as f:
        head = f.readline().rstrip("\n").split("\t")
        rows = []
        for line in f:
            r = line.rstrip("\n").split("\t")
            if len(r) < 8:
                continue
            rows.append([r[0], "\t".join(r[1:-6])] + r[-6:])
    a = pd.DataFrame(rows, columns=head)
    a["seg_id"] = a.seg_id.astype(int)
    return a


def score_errors(m, sys_col, key_cols, rater_col, sev_col, cat_col):
    m = m.copy()
    m["w"] = [mqm_weight(s, c) for s, c in zip(m[sev_col], m[cat_col])]
    per_rater = m.groupby(key_cols + [sys_col, rater_col]).w.sum().reset_index()
    return per_rater.groupby(key_cols + [sys_col]).agg(mqm=("w", "mean"), n_raters=(rater_col, "nunique")).reset_index()


def _chrf_batch(pairs):
    return [chrf(h, r) for h, r in pairs]


def build(lp):
    a = read_avg(f"{DL}/{lp}/mqm_generalMT2022_{lp}.avg_seg_scores.tsv")
    a["dkey"] = a.domain + "_" + a.doc

    m = pd.read_csv(f"{DL}/{lp}/mqm_generalMT2022_{lp}.tsv", sep="\t", quoting=csv.QUOTE_NONE,
                    keep_default_na=False, dtype=str)
    n0 = len(m)
    m = m[m.severity != "HOTW-test"]  # attention-check rows (zh-en only)
    print(f"[{lp}] mqm rows {n0}, dropped HOTW-test {n0 - len(m)}")
    m["system"] = m.system.str.replace(r"\.en$", "", regex=True)
    m["dkey"] = m.doc.str.split(":").str[0]
    m["tgt"] = m.target.map(strip_marks)
    # local segment key in mqm file: (dkey, seg_id_local)
    m["lkey"] = m.dkey + "#" + m.seg_id
    s = score_errors(m, "system", ["lkey"], "rater", "severity", "category")
    meta = m.drop_duplicates(["lkey", "system"])[["lkey", "system", "dkey", "source", "tgt"]]
    s = s.merge(meta, on=["lkey", "system"])

    # map local key -> global seg_id of avg file. Source text in the MQM tsv is re-tokenised (e.g. "100,000" ->
    # "100000"), so match by position: within each document, the MQM rows ordered by doc_id (position among rated
    # segments) align 1:1 with the avg file's rated seg_ids in ascending order. Verified below via exact score match.
    rated = a[a.score != "None"].drop_duplicates("seg_id").sort_values("seg_id")
    loc = m.drop_duplicates("lkey").assign(p=lambda d: d.doc_id.astype(int)).sort_values(["dkey", "p"])
    cand = {}
    for dk, g in loc.groupby("dkey"):
        r = rated[rated.dkey == dk]
        assert len(r) == len(g), (lp, dk)
        cand.update(dict(zip(g.lkey, r.seg_id)))
    cand = pd.Series(cand)
    print(f"[{lp}] local segs {s.lkey.nunique()}, mapped {len(cand)}")
    s["seg_id"] = s.lkey.map(cand)
    s = s.dropna(subset=["seg_id"])
    s["seg_id"] = s.seg_id.astype(int)

    # sanity: compare with Google's avg_seg_scores score (= -MQM)
    chk = s.merge(a.rename(columns={"sys": "system"})[["system", "seg_id", "score", "hyp"]], on=["system", "seg_id"], how="left")
    ok = chk.score.notna() & (chk.score != "None")
    diff = np.abs(chk.loc[ok, "mqm"] - (-chk.loc[ok, "score"].astype(float)))
    print(f"[{lp}] check vs avg_seg_scores: n={ok.sum()} exact(<1e-6)={np.mean(diff < 1e-6):.4f} max|diff|={diff.max():.3f}")
    hyp_mismatch = (chk.loc[ok, "hyp"].str.strip() != chk.loc[ok, "tgt"]).mean()
    print(f"[{lp}] hyp text mismatch avg vs stripped mqm target: {hyp_mismatch:.4f}")

    # system coverage
    nseg = s.seg_id.nunique()
    cov = s.groupby("system").seg_id.nunique() / nseg
    print(f"[{lp}] rated segments {nseg}; coverage:\n{cov.sort_values().round(4).to_string()}")
    keep = [x for x in cov.index if cov[x] >= MIN_COVER and x not in REF_SYS]
    s = s[s.system.isin(keep)]
    full = s.groupby("seg_id").system.nunique()
    segs = full[full == len(keep)].index
    s = s[s.seg_id.isin(segs)]

    # text from avg file (clean hyp; reference = 'ref' column = refA; ref_b = refB output)
    at = a.rename(columns={"sys": "system"})
    seg_meta = at.drop_duplicates("seg_id").set_index("seg_id")[["source", "ref", "domain", "doc"]]
    refb = at[at.system == "refB"].set_index("seg_id").hyp
    hyp = at.set_index(["system", "seg_id"]).hyp
    pool = pd.DataFrame({
        "seg_id": s.seg_id.values,
        "doc_id": seg_meta.loc[s.seg_id, "doc"].values,
        "domain": seg_meta.loc[s.seg_id, "domain"].values,
        "system": s.system.values,
        "source": seg_meta.loc[s.seg_id, "source"].values,
        "reference": seg_meta.loc[s.seg_id, "ref"].values,
        "ref_b": refb.reindex(s.seg_id).values,
        "hyp": [hyp.get((x, i), np.nan) for x, i in zip(s.system, s.seg_id)],
        "mqm": s.mqm.values,
        "n_raters": s.n_raters.values,
    })
    assert pool.hyp.notna().all() and pool.reference.notna().all()
    # check reference == refA output in mqm file
    ra = m[m.system == "refA"].drop_duplicates("lkey").assign(seg_id=lambda d: d.lkey.map(cand)).dropna(subset=["seg_id"])
    ra = ra.set_index(ra.seg_id.astype(int)).tgt
    ra = ra[~ra.index.duplicated()]
    common = ra.index.intersection(seg_meta.index)
    eq = np.mean([norm(x) == norm(y) for x, y in zip(seg_meta.loc[common, "ref"], ra.loc[common])])
    print(f"[{lp}] reference(avg 'ref') == refA(mqm target), whitespace/comma-normalised: {eq:.4f} of {len(common)}")
    pool["u"] = utility(pool.mqm)

    if lp == "ende":
        t = pd.read_csv(f"{DL}/ende/mqm_generalMT2022_ende.3ratingsPerSegment.tsv", sep="\t", quoting=csv.QUOTE_NONE,
                        keep_default_na=False, dtype=str)
        t["dkey"] = t.document_id
        t3 = score_errors(t, "system_id", ["document_id", "doc_segment_id"], "rater_id", "severity", "category")
        tm = t.drop_duplicates(["document_id", "doc_segment_id", "system_id"])[
            ["document_id", "doc_segment_id", "system_id", "candidate"]]
        t3 = t3.merge(tm, on=["document_id", "doc_segment_id", "system_id"])
        # positional doc alignment (same as above): doc_segment_id order == rated seg_id order within the doc
        tl = t3.drop_duplicates(["document_id", "doc_segment_id"]).assign(p=lambda d: d.doc_segment_id.astype(int))
        pos = {}
        for dk, g in tl.sort_values(["document_id", "p"]).groupby("document_id"):
            r = rated[rated.doc == dk]
            assert len(r) == len(g), dk
            pos.update({(dk, ds): sid for ds, sid in zip(g.doc_segment_id, r.seg_id)})
        t3["seg_id"] = [pos[(d, k)] for d, k in zip(t3.document_id, t3.doc_segment_id)]
        hchk = t3.merge(at[["system", "seg_id", "hyp"]], left_on=["system_id", "seg_id"], right_on=["system", "seg_id"])
        print(f"[ende] 3r candidate == avg hyp (normalised): "
              f"{np.mean([norm(strip_marks(x)) == norm(y) for x, y in zip(hchk.candidate, hchk.hyp)]):.4f}")
        t3 = t3.set_index(["system_id", "seg_id"])
        idx = list(zip(pool.system, pool.seg_id))
        pool["mqm_3r"] = t3.mqm.reindex(idx).values
        pool["u_3r"] = utility(pool.mqm_3r)
        ok = pool.mqm_3r.notna()
        print(f"[ende] 3-rater re-annotation joined for {ok.mean():.4f} of pool rows; "
              f"corr(mqm, mqm_3r)={np.corrcoef(pool.mqm[ok], pool.mqm_3r[ok])[0, 1]:.3f}")

    pairs = list(zip(pool.hyp, pool.reference))
    chunks = [pairs[i:i + 500] for i in range(0, len(pairs), 500)]
    with ProcessPoolExecutor(64) as ex:
        pool["chrf"] = [v for c in ex.map(_chrf_batch, chunks) for v in c]

    pool = pool.sort_values(["seg_id", "system"]).reset_index(drop=True)
    import os
    os.makedirs(f"{MT_ROOT}/{lp}", exist_ok=True)
    pool.to_parquet(f"{MT_ROOT}/{lp}/pool.parquet", index=False)
    print(f"[{lp}] wrote pool: {pool.seg_id.nunique()} segs x {pool.system.nunique()} systems = {len(pool)} rows")
    return pool


if __name__ == "__main__":
    for lp in LPS:
        build(lp)
