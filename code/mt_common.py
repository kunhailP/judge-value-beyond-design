"""Shared helpers for the MT (WMT22 MQM) block.

Data provenance: github.com/google/wmt-mqm-human-evaluation @ 29acd6999aaea3586378c9dcb58d8cc4820cede3
(cloned to /root/naacl_data/mt/dl/wmt-mqm-human-evaluation).
"""
import re

import numpy as np
from sacrebleu.metrics import CHRF

MT_ROOT = "/root/naacl_data/mt"
LPS = ("ende", "zhen")
CAP = 25.0

_chrf = CHRF()  # sacrebleu defaults: char order 6, word order 0, beta 2 (chrF2)


def mqm_weight(severity: str, category: str) -> float:
    """Google MQM weights (Freitag et al. 2021; repo README / Marot defaults).

    Non-translation 25 (any severity); Minor Fluency/Punctuation 0.1; Major 5; Minor 1;
    Neutral / No-error 0. HOTW-test rows must be dropped before calling this.
    """
    sev = severity.strip().lower()
    cat = category.strip().lower().replace("_", "-")
    if cat.startswith("non-translation"):
        return 25.0
    if sev == "major":
        return 5.0
    if sev == "minor":
        return 0.1 if cat == "fluency/punctuation" else 1.0
    return 0.0  # no-error, neutral


def utility(mqm):
    """u = -min(MQM, 25)/25, in [-1, 0]."""
    return -np.minimum(np.asarray(mqm, dtype=float), CAP) / CAP


_V = re.compile(r"</?v>")


def strip_marks(s: str) -> str:
    return _V.sub("", s).strip()


def chrf(hyp: str, ref: str) -> float:
    """Sentence chrF2 (0-100) with sacrebleu defaults."""
    return _chrf.sentence_score(hyp, [ref]).score


def dissimilarity(hyp_a: str, hyp_b: str) -> float:
    """Label-free pairwise output dissimilarity in [0, 1]: 1 - chrF(hyp_a, hyp_b)/100.

    chrF is asymmetric (beta=2 weights recall), so symmetrise by averaging both directions.
    Identical strings -> 0 exactly.
    """
    if hyp_a == hyp_b:
        return 0.0
    return 1.0 - 0.5 * (chrf(hyp_a, hyp_b) + chrf(hyp_b, hyp_a)) / 100.0


def load_pool(lp: str):
    import pandas as pd
    return pd.read_parquet(f"{MT_ROOT}/{lp}/pool.parquet")
