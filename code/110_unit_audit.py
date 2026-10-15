#!/usr/bin/env python3
"""Fixed-budget certification audits for the MT (WMT22 MQM) and chat (LMArena) blocks.

Population: N units (MT: segments; Arena: battles of one model pair) and a menu of M systems with human utilities Y[N, M]
(MT: u = -min(MQM,25)/25, identical output strings of a segment share the mean of their ratings; Arena: u_x = vote,
u_y = 1 - vote, tie = 0.5). Estimand: the population mean utility of every system (finite population).

One draw = one audit: a random pilot of P units is fully labelled; the candidate is the menu system with the best pilot
mean; for every competitor j the paired difference D_j = Y_j - Y_c is estimated as
    [ sum_pilot D_j  +  sum_rest lam_j * Jd_j  +  sum_{s in S} (D_j(s) - lam_j * Jd_j(s)) / pi_s ] / N
with S a Poisson sample of the non-pilot units (inclusion probabilities pi), Jd_j = judge score difference, lam_j >= 0 the
PPI++ coefficient fitted on the pilot and frozen (lam = 0: humans only). Variance: sum_S (1 - pi) R^2 / pi^2 / N^2.
Certificate: every one-sided normal upper bound (level alpha/(M-1)) is <= eps. A wrong certificate: true regret > eps.
Cost: unique human ratings, pilot included (pilot: every distinct menu output of its units).

Designs (sampling x estimator):
  uniform       pi uniform over the non-pilot units, every menu output rated (cost M per unit, naive)
  dedup         pi uniform over units where some competitor's output differs from the candidate's; identical
                strings rated once; D_j = 0 known exactly when output_j == output_c                 (MT only)
  weighted      pi ∝ g(s) = sqrt(sum_j sigma^2(bin of dissimilarity(c, j))), sigma^2 fitted on the pilot
                (bin 0 = identical output, weight 0; positive dissimilarities in three bins by default: below the
                pilot-free population median, third quartile, fourth quartile; --bins 4: quartiles); dedup costs (MT only)
  uniform_cvl:f uniform sampling and cost + judge f control variate (pilot lam)
  weighted_cvl:f weighted sampling + judge f control variate                                         (MT only)
  active_cvl:f  pi ∝ sqrt(sum_j sigma_R^2(bin)), residual variance by (dissimilarity bin x |Jd| half) on the pilot (MT)
                or by |Jd| quintile (Arena); dedup costs in MT, unit cost in Arena
Pilot-only predictions per draw and design: predicted post-pilot labels L = max_j z^2 (sum_rest g c) N_rest m_j / (N^2 s_j^2),
m_j = pilot mean of R_j^2 / g over units with g > 0, s_j = eps - pilot mean of D_j; plus pilot judge accuracy and pilot rho.

Known-zero differences. Units whose every competitor output equals the candidate's have D = 0 and pi = 0 under dedup /
weighted / active sampling; the estimator still adds lam * Jd over them (sum_rest) and no residual ever corrects it, so
it is unbiased only if the evaluator gives identical outputs identical scores (Jd = 0 there). Every real evaluator here
does (chrF, COMET, the WMT22 metrics and the GEMBA judges score the string); the semi-synthetic judges do so since
2026-10-10 (--syn_noise string); --syn_noise output reproduces the earlier runs, whose bias is (1/N) sum_{pi=0} lam Jd.
"""
import argparse, json, os, sys
from multiprocessing import Pool
import numpy as np, pandas as pd
from scipy.stats import norm, t as tdist

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from paths import DATA
ALPHA = 0.10
MBR = ("bleu_bestmbr", "bleurt_bestmbr", "comet_bestmbr", "chrf_bestmbr")


# ----------------------------------------------------------------------------------------------- data adapters
def _synthetic(Y, rho, seed, S=None):
    """Judge = human utility + Gaussian noise, with the noise scale set so that the correlation of the paired differences
    (averaged over menu pairs, all units) is approximately rho. Exploratory calibration device only.
    S (string ids per unit and menu slot): identical output strings of a unit share ONE noise draw, so a known-zero
    difference (D_i = 0, never sampled by the dedup / weighted / active designs) has judge difference 0 as well; the
    noise scale is then set on the non-identical pairs (share q) to keep the all-unit rho at the target. S=None: an
    independent draw per output (runs before 2026-10-10), which leaves the uncorrected term (1/N) sum_{pi_i=0} lam Dhat_i
    in the estimate (see the note in the module docstring)."""
    import zlib
    rng = np.random.default_rng(zlib.crc32(f"{rho:.3f}".encode()))
    M = Y.shape[1]
    pairs = [(a, b) for a in range(M) for b in range(a + 1, M)]
    vD = np.mean([np.var(Y[:, a] - Y[:, b]) for a, b in pairs])
    q = np.mean([np.mean(S[:, a] != S[:, b]) for a, b in pairs]) if S is not None else 1.0
    sig = np.sqrt(vD * (1 / rho ** 2 - 1) / (2 * q)) if rho < 1 else 0.0
    E = sig * rng.standard_normal(Y.shape)
    if S is not None:
        E = np.take_along_axis(E, S, axis=1)        # slot j of unit i takes the noise of its string id S[i, j]
    return Y + E
def load_mt(lp, menu_k=4, menu=None, judges=("chrf",), judge_dir=None, ident="mean", ident_seed=0, syn_noise="string"):
    from mt_common import load_pool, dissimilarity
    judge_dir = judge_dir or f"{DATA}/mt"
    d = load_pool(lp)
    d = d[~d.system.isin(MBR)].copy()
    # identical output strings of a segment share one label: the mean of their ratings (default) or, as a sensitivity
    # check (ident="pick"), one of their ratings drawn at random, so that a shared label is a single human rating
    if ident == "pick":
        rng = np.random.default_rng(ident_seed)
        d["_r"] = rng.random(len(d))
        d["u"] = d.loc[d.groupby(["seg_id", "hyp"])._r.transform("idxmin"), "u"].to_numpy()
        d = d.drop(columns="_r")
    else:
        d["u"] = d.groupby(["seg_id", "hyp"]).u.transform("mean")
    if menu is None:
        menu = d.groupby("system").u.mean().sort_values(ascending=False).index[:menu_k].tolist()
    d = d[d.system.isin(menu)]
    segs = np.sort(d.seg_id.unique())
    piv = lambda col: d.pivot(index="seg_id", columns="system", values=col).loc[segs, menu]
    Y = piv("u").to_numpy(float)
    H = piv("hyp").to_numpy(object)
    S = np.zeros_like(Y, dtype=int)
    for i in range(len(segs)):
        _, inv = np.unique(H[i], return_inverse=True); S[i] = inv
    M = len(menu)
    X = np.zeros((len(segs), M, M))
    for a in range(M):
        for b in range(a + 1, M):
            X[:, a, b] = X[:, b, a] = [dissimilarity(H[i, a], H[i, b]) for i in range(len(segs))]
    J = {}
    for f in judges:
        if f == "chrf":
            J[f] = piv("chrf").to_numpy(float)
        elif f.startswith("syn"):                       # exploratory: utility + Gaussian noise, paired-difference rho ~ target
            J[f] = _synthetic(Y, float(f[3:]), seed=hash(f) % 2**31, S=S if syn_noise == "string" else None)
        else:
            base, inv = (f[4:], True) if f.startswith("inv_") else (f, False)
            jd = pd.read_parquet(os.path.join(judge_dir, lp, f"judge_{base}.parquet"))
            jd = jd[jd.system.isin(menu)].pivot(index="seg_id", columns="system", values="score").loc[segs, menu].to_numpy(float)
            J[f] = -jd if inv else jd
    return dict(name=f"mt_{lp}", menu=menu, Y=Y, S=S, X=X, J=J, structural=True)


def load_arena(pair_id, judges=("qwen3_8b",), root=None):
    root = root or f"{DATA}/arena"
    v09 = int(pair_id) >= 10                      # lock v0.9 pairs live in their own pool / judge files
    sfx = "_v09" if v09 else ""
    p = pd.read_parquet(os.path.join(root, f"pool{sfx}.parquet"))
    p = p[p.pair_id == int(pair_id)].sort_values("battle_id")
    y = p.human.to_numpy(float)
    Y = np.stack([y, 1 - y], 1)
    N = len(p)
    J = {}
    for f in judges:
        if f.startswith("syn"):
            J[f] = _synthetic(Y, float(f[3:]), seed=hash(f) % 2**31); continue
        if f == "longer":
            s = (p.len_x.to_numpy(float) > p.len_y.to_numpy(float)) + 0.5 * (p.len_x.to_numpy() == p.len_y.to_numpy())
        else:
            base, inv = (f[4:], True) if f.startswith("inv_") else (f, False)
            base, col = (base.split("@")[0], {"o1": "p_x_order1", "o2": "p_x_order2"}[base.split("@")[1]]) if "@" in base else (base, "p_x")
            jd = pd.read_parquet(os.path.join(root, f"judge_{base}{sfx}.parquet")).set_index("battle_id").loc[p.battle_id]
            s = jd[col].to_numpy(float)                 # @o1 / @o2: a single presentation order (exploratory)
            s = np.where(np.isnan(s), 0.5, s)
            s = 1 - s if inv else s
        J[f] = np.stack([s, 1 - s], 1)
    return dict(name=f"arena_{pair_id}", menu=[p.model_x.iloc[0], p.model_y.iloc[0]], Y=Y, S=np.tile([0, 1], (N, 1)),
                X=None, J=J, structural=False)


# ----------------------------------------------------------------------------------------------- design helpers
def poisson_pi(g, n):
    g = np.asarray(g, float); pi = np.zeros_like(g)
    if g.sum() <= 0 or n <= 0:
        return pi
    free = g > 0
    for _ in range(50):
        rem = n - (pi[~free & (g > 0)].sum())
        pi[free] = rem * g[free] / g[free].sum()
        over = free & (pi >= 1)
        if not over.any():
            break
        pi[over] = 1.0; free &= ~over
        if not free.any():
            break
    return np.clip(pi, 0, 1)


def bin_index(x, edges):
    b = np.searchsorted(edges, x, side="right")         # 1..len(edges)
    return np.where(x <= 0, 0, b)


def fit_bin_var(vals, bins, nb):
    """mean of vals by bin (vals = squared residuals on pilot), fallback to the overall mean of non-zero bins."""
    out = np.zeros(nb)
    ok = bins > 0
    overall = vals[ok].mean() if ok.any() else 0.0
    for k in range(1, nb):
        m = bins == k
        out[k] = vals[m].mean() if m.sum() >= 3 else overall
    return np.maximum(out, 1e-8)


def wlam(Dv, Jv, wv):
    """weighted least-squares coefficient per comparison (columns), clipped at 0."""
    sw = wv.sum(); md = (wv[:, None] * Dv).sum(0) / sw; mj = (wv[:, None] * Jv).sum(0) / sw
    cov = (wv[:, None] * (Dv - md) * (Jv - mj)).sum(0); var = (wv[:, None] * (Jv - mj) ** 2).sum(0)
    return np.where(var > 0, np.maximum(cov / np.where(var > 0, var, 1), 0.0), 0.0)


# ----------------------------------------------------------------------------------------------- one draw
def run_draw(args):
    data, cfg, i = args
    Y, S, X, J = data["Y"], data["S"], data["X"], data["J"]
    N, M = Y.shape
    rng = np.random.default_rng(cfg["seed"] * 100003 + i)
    perm = rng.permutation(N); P = cfg["pilot"]
    pil, rest = perm[:P], perm[P:]
    mu = Y.mean(0)
    if cfg.get("boundary"):
        order = np.argsort(-mu); c = int(order[1]); eps_list = [cfg.get("boundary_frac", 0.9) * (mu[order[0]] - mu[c])]
    else:
        c = int(np.argmax(Y[pil].mean(0))); eps_list = cfg["eps"]
    comp = [j for j in range(M) if j != c]
    regret = mu.max() - mu[c]
    D = np.stack([Y[:, j] - Y[:, c] for j in comp], 1)                     # [N, M-1]
    same = np.stack([S[:, j] == S[:, c] for j in comp], 1)                 # D == 0 known
    # costs
    pilot_cost = int(sum(len(np.unique(S[s])) for s in pil)) if data["structural"] else P   # Arena: one vote per battle
    c_naive = np.full(N, M, float)
    c_dedup = np.zeros(N)
    for s in range(N):
        diff = S[s][np.array(comp)][~same[s]]
        c_dedup[s] = 0 if len(diff) == 0 else 1 + len(np.unique(diff))
    if not data["structural"]:
        c_naive = np.ones(N); c_dedup = np.ones(N)
    relevant = c_dedup > 0
    # judge differences and pilot lambdas
    JD, lam, acc, rho = {}, {}, {}, {}
    for f, sc in J.items():
        jd = np.stack([sc[:, j] - sc[:, c] for j in comp], 1)
        if cfg.get("zero_known", True):
            jd = np.where(same, 0.0, jd)        # known-zero differences: the evaluator's difference is set to 0 as well (eq. est)
        JD[f] = jd
        lam[f] = np.zeros(len(comp))
        r_ = []
        for k in range(len(comp)):
            a, b = D[pil, k], jd[pil, k]
            v = b.var(ddof=1)
            lam[f][k] = max(0.0, np.cov(a, b)[0, 1] / v) if v > 0 else 0.0
            r_.append(np.corrcoef(a, b)[0, 1] if a.std() > 0 and b.std() > 0 else 0.0)
        rho[f] = float(np.nanmean(r_))
        m = D[pil] != 0                                                      # pilot pairwise accuracy (non-tied)
        acc[f] = float((np.sign(D[pil][m]) == np.sign(jd[pil][m])).mean()) if m.any() else np.nan
    # sampling weights
    designs = {}
    designs["uniform"] = dict(g=np.ones(N), cost=c_naive, lam=None)
    if data["structural"]:
        designs["dedup"] = dict(g=relevant.astype(float), cost=c_dedup, lam=None)
        xs = np.stack([X[:, c, j] for j in comp], 1)
        edges = np.quantile(xs[xs > 0], [0.25, 0.5, 0.75]) if (xs > 0).any() else np.array([1.0])
        if cfg.get("bins", 3) == 4:
            # four quartile bins of the positive dissimilarities (1..4); weight 0 only for identical strings
            xb = np.where(same, 0, np.searchsorted(edges, xs, side="right") + 1); nb = len(edges) + 2
        else:
            # locked runs (default): bin_index gives 0 for x below the first quartile and np.maximum(., 1) folds it into
            # bin 1, so the positive dissimilarities fall into THREE bins (below the median; third quartile; fourth
            # quartile), not four. Kept as the default because every locked and exploratory run used it; --bins 4 is the
            # four-quartile variant (sensitivity check).
            xb = np.where(same, 0, np.maximum(bin_index(xs, edges), 1)); nb = len(edges) + 1   # weight 0 only for identical strings
        sig = fit_bin_var((D[pil] ** 2).ravel(), xb[pil].ravel(), nb)
        g_w = np.sqrt((sig[xb] * (xb > 0)).sum(1))
        designs["weighted"] = dict(g=g_w, cost=c_dedup, lam=None)
    for f in J:
        designs[f"uniform_cvl:{f}"] = dict(g=np.ones(N), cost=c_naive, lam=f)
        R2 = (D - lam[f] * JD[f]) ** 2
        if data["structural"]:
            designs[f"weighted_cvl:{f}"] = dict(g=g_w, cost=c_dedup, lam=f)
            aj = np.abs(JD[f]); med = np.median(aj[pil][xb[pil] > 0]) if (xb[pil] > 0).any() else 0
            rb = np.where(xb > 0, xb + nb * (aj > med), 0); nrb = 2 * nb
            sigr = fit_bin_var(R2[pil].ravel(), rb[pil].ravel(), nrb)
            g_a = np.sqrt((sigr[rb] * (rb > 0)).sum(1))
            designs[f"active_cvl:{f}"] = dict(g=g_a, cost=c_dedup, lam=f)
        else:
            aj = np.abs(JD[f][:, 0]); edges_a = np.quantile(aj[pil], [0.2, 0.4, 0.6, 0.8])
            ab = np.searchsorted(edges_a, aj, side="right") + 1
            sigr = fit_bin_var(R2[pil, 0], ab[pil], 6)
            designs[f"active_cvl:{f}"] = dict(g=np.sqrt(sigr[ab]), cost=c_naive, lam=f)
    if cfg.get("oracle"):                                   # diagnostic: lambda from the whole population (not available to an auditor)
        for f in J:
            lo_ = np.array([max(0.0, np.cov(D[:, k], JD[f][:, k])[0, 1] / JD[f][:, k].var(ddof=1)) if JD[f][:, k].var() > 0 else 0.0
                            for k in range(len(comp))])
            lam[f"__o:{f}"] = lo_; JD[f"__o:{f}"] = JD[f]
            designs[f"uniform_cvo:{f}"] = dict(g=np.ones(N), cost=c_naive, lam=f"__o:{f}")
            if data["structural"]:
                designs[f"weighted_cvo:{f}"] = dict(g=g_w, cost=c_dedup, lam=f"__o:{f}")
    if cfg.get("extra"):                                    # post-lock robustness arms (exploratory)
        for f in J:
            if data["structural"]:
                designs[f"dedup_cvl:{f}"] = dict(g=relevant.astype(float), cost=c_dedup, lam=f)
            bases = [("uniform", np.ones(N), c_naive)] + ([("weighted", g_w, c_dedup), ("dedup", relevant.astype(float), c_dedup)] if data["structural"] else [])
            for bname, bg, bc in bases:
                designs[f"{bname}_cvr:{f}"] = dict(g=bg, cost=bc, lam=f, mode="refit")    # lambda refit on pilot + all post-pilot labels (same labels)
                designs[f"{bname}_cvx:{f}"] = dict(g=bg, cost=bc, lam=f, mode="xfit")     # lambda cross-fitted over two folds of the post-pilot sample
                designs[f"{bname}_cvu:{f}"] = dict(g=bg, cost=bc, lam=f, mode="xfit", unweighted=True)    # cross-fitted, unweighted least squares
                designs[f"{bname}_cvq:{f}"] = dict(g=bg, cost=bc, lam=f, mode="refit", unweighted=True)   # refit on all labels, unweighted
    z = norm.ppf(1 - ALPHA / len(comp))
    Dbar = D.mean(0)
    known = D[pil].sum(0)
    rows, pred = [], []
    rest_mask = np.zeros(N, bool); rest_mask[rest] = True
    for name, dz in designs.items():
        lm = lam[dz["lam"]] if dz["lam"] else np.zeros(len(comp))
        jd = JD[dz["lam"]] if dz["lam"] else np.zeros_like(D)
        R = D - lm * jd
        g = dz["g"].copy(); g[~rest_mask] = 0
        # pilot-only prediction of post-pilot labels (one per eps)
        gp = dz["g"][pil]; ok = gp > 0
        m_j = ((R[pil][ok] ** 2) / gp[ok, None]).sum(0) / P if ok.any() else np.zeros(len(comp))
        Gc = (g * dz["cost"]).sum()
        for eps in eps_list:
            s_j = eps - D[pil].mean(0)
            L = np.where(s_j > 0, z ** 2 * Gc * len(rest) * m_j / (N ** 2 * np.maximum(s_j, 1e-12) ** 2), np.inf).max()
            pred.append((i, name, eps, float(L), pilot_cost))
        base_rest = (lm * jd)[rest].sum(0)
        for n in cfg["budgets"]:
            pi = poisson_pi(g, n)
            U = np.random.default_rng((cfg["seed"] * 100003 + i) * 1009 + n).random(N)   # common random numbers across designs
            samp = (U < pi) & (pi > 0)
            cost = pilot_cost + dz["cost"][samp].sum()
            w = 1.0 / pi[samp]
            mode = dz.get("mode", "fixed")
            if mode == "fixed":
                est = (known + base_rest + (R[samp] * w[:, None]).sum(0)) / N
                var = ((1 - pi[samp])[:, None] * R[samp] ** 2 * w[:, None] ** 2).sum(0) / N ** 2
            elif mode == "refit":
                idx = np.concatenate([pil, np.where(samp)[0]]); wv = np.concatenate([np.ones(len(pil)), w])
                if dz.get("unweighted"):
                    wv = np.ones_like(wv)
                lr = wlam(D[idx], jd[idx], wv); Rr = D - lr * jd
                est = (known + (lr * jd)[rest].sum(0) + (Rr[samp] * w[:, None]).sum(0)) / N
                var = ((1 - pi[samp])[:, None] * Rr[samp] ** 2 * w[:, None] ** 2).sum(0) / N ** 2
            else:   # xfit: every unit gets a fold; its residual uses lambda fitted on pilot + the sampled units of the other fold
                fold = np.random.default_rng((cfg["seed"] * 100003 + i) * 7919 + n).random(N) < 0.5
                lam_f = {}
                for fo in (True, False):
                    So = samp & (fold != fo)
                    idx = np.concatenate([pil, np.where(So)[0]]); wv = np.concatenate([np.ones(len(pil)), 1.0 / pi[So]])
                    if dz.get("unweighted"):
                        wv = np.ones_like(wv)
                    lam_f[fo] = wlam(D[idx], jd[idx], wv)
                lu = np.where(fold[:, None], lam_f[True], lam_f[False])            # [N, K] unit-specific coefficient
                Rx = D - lu * jd
                est = (known + (lu * jd)[rest].sum(0) + (Rx[samp] * w[:, None]).sum(0)) / N
                var = ((1 - pi[samp])[:, None] * Rx[samp] ** 2 * w[:, None] ** 2).sum(0) / N ** 2
            zq = z if cfg.get("bound", "normal") == "normal" else tdist.ppf(1 - ALPHA / len(comp), max(int(samp.sum()) - 1, 1))
            ucb = est + zq * np.sqrt(var)
            cover = int((ucb >= Dbar - 1e-9).all())      # simultaneous one-sided coverage of the true mean differences (nominal 1 - alpha; tolerance for census rounding)
            for eps in eps_list:
                act = bool((ucb <= eps).all())
                rows.append((i, name, n, eps, float(cost), int(act), int(act and regret > eps), float(regret), cover))
    meta = dict(draw=i, cand=c, regret=float(regret), pilot_cost=pilot_cost,
                **{f"lam:{f}": float(lam[f].mean()) for f in J}, **{f"lamo:{f}": float(lam[f"__o:{f}"].mean()) for f in J if f"__o:{f}" in lam}, **{f"acc:{f}": acc[f] for f in J}, **{f"rho:{f}": rho[f] for f in J})
    return rows, pred, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("domain", choices=["mt", "arena"])
    ap.add_argument("unit", help="mt: ende|zhen ; arena: pair_id")
    ap.add_argument("--menu", nargs="*", default=None, help="mt: explicit menu (default top-4 by mean u, MBR systems excluded)")
    ap.add_argument("--menu_k", type=int, default=4)
    ap.add_argument("--judges", nargs="*", default=["chrf"])
    ap.add_argument("--pilot", type=int, default=100)
    ap.add_argument("--eps", nargs="*", type=float, default=[0.005, 0.01, 0.02])
    ap.add_argument("--budgets", nargs="*", type=int, default=None)
    ap.add_argument("--draws", type=int, default=300)
    ap.add_argument("--seed", type=int, default=20261007)
    ap.add_argument("--boundary", action="store_true")
    ap.add_argument("--boundary_frac", type=float, default=0.9, help="boundary stress: eps as a fraction of the true gap")
    ap.add_argument("--bound", choices=["normal", "t"], default="normal", help="robustness: Student-t quantile with (sampled units - 1) df")
    ap.add_argument("--extra", action="store_true", help="exploratory: dedup+evaluator, refit-lambda (*_cvr) and cross-fitted-lambda (*_cvx) arms")
    ap.add_argument("--oracle", action="store_true", help="exploratory: add population-lambda arms *_cvo")
    ap.add_argument("--ident", choices=["mean", "pick"], default="mean", help="mt sensitivity: identical strings share the mean rating or one random rating")
    ap.add_argument("--ident_seed", type=int, default=0)
    ap.add_argument("--zero_known", type=int, choices=[0, 1], default=1, help="set the evaluator difference to 0 where the outputs coincide (D = 0 known); 0 reproduces the locked records, which differ by at most 7e-6 in the mean difference")
    ap.add_argument("--syn_noise", choices=["string", "output"], default="string", help="semi-synthetic judges (syn<rho>): one noise draw per distinct output string (identical outputs share a score; default since 2026-10-10) or per output (the earlier runs; biased on known-zero differences under dedup/weighted/active sampling)")
    ap.add_argument("--bins", type=int, choices=[3, 4], default=3, help="weighted design: positive dissimilarity bins; 3 = the locked runs (below the median, third and fourth quartile), 4 = quartiles (sensitivity)")
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default=os.path.join(HERE, "..", "results"))
    ap.add_argument("--procs", type=int, default=64)
    a = ap.parse_args()
    data = load_mt(a.unit, a.menu_k, a.menu, a.judges, ident=a.ident, ident_seed=a.ident_seed, syn_noise=a.syn_noise) if a.domain == "mt" else load_arena(a.unit, a.judges)
    N = data["Y"].shape[0]
    budgets = a.budgets or sorted({int(x) for x in np.geomspace(10, N - a.pilot, 14)})
    cfg = dict(pilot=a.pilot, eps=a.eps, budgets=budgets, seed=a.seed, boundary=a.boundary, boundary_frac=a.boundary_frac, oracle=a.oracle, bound=a.bound, extra=a.extra, bins=a.bins, syn_noise=a.syn_noise, zero_known=bool(a.zero_known))
    with Pool(a.procs) as pool:
        res = pool.map(run_draw, [(data, cfg, i) for i in range(a.draws)])
    # tuples rather than dicts: the same columns, several times faster to assemble for millions of rows
    rows = pd.DataFrame([r for x in res for r in x[0]], columns=["draw", "design", "budget", "eps", "cost", "act", "wrong", "regret", "cover"])
    pred = pd.DataFrame([r for x in res for r in x[1]], columns=["draw", "design", "eps", "L_pred", "pilot_cost"])
    meta = pd.DataFrame([x[2] for x in res])
    od = os.path.join(a.out, a.domain); os.makedirs(od, exist_ok=True)
    stem = f"{data['name']}_m{len(data['menu'])}_p{a.pilot}{'_boundary' if a.boundary else ''}{a.tag}"
    rows.to_parquet(os.path.join(od, f"{stem}_draws.parquet")); pred.to_parquet(os.path.join(od, f"{stem}_pred.parquet"))
    meta.to_parquet(os.path.join(od, f"{stem}_meta.parquet"))
    json.dump(dict(menu=data["menu"], N=N, mu=data["Y"].mean(0).tolist(), cfg=cfg, judges=a.judges),
              open(os.path.join(od, f"{stem}_info.json"), "w"), indent=1)
    s = rows.groupby(["eps", "design", "budget"]).agg(act=("act", "mean"), wrong=("wrong", "mean"), cost=("cost", "mean")).reset_index()
    print(stem, "menu", data["menu"], "mu", np.round(data["Y"].mean(0), 4), "N", N)
    print(s.groupby(["eps", "design"]).agg(max_act=("act", "max"), max_wrong=("wrong", "max")).round(3).unstack(0).to_string())


if __name__ == "__main__":
    main()
