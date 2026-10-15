"""Lock v0.9 Arena pool: English single-turn pairs with >= 300 battles (ties kept) NOT used in v0.8, the 6 with the smallest
|win-rate gap| (a hard decision). Pair selection uses human votes only (it defines the decision); no judge output exists
for these battles when the lock is committed."""
import importlib.util, sys, numpy as np, pandas as pd
SRC, OUT, V08 = sys.argv[1], sys.argv[2], sys.argv[3]
spec = importlib.util.spec_from_file_location("ap", __file__.replace("arena_pool_v09.py", "arena_pool.py"))
src = open(spec.origin).read().split("dec = rows")[0]           # reuse the parsing part of arena_pool.py verbatim
ns = {"__name__": "x"}; sys.argv = [sys.argv[0], SRC, "/dev/null"]; exec(src, ns)
rows = ns["rows"]
used = set(pd.read_parquet(V08).battle_id) if V08 else set()
v08_pairs = set((pd.read_parquet(V08).model_x + " vs " + pd.read_parquet(V08).model_y).unique())
g = rows.groupby("pair").agg(n=("human", "size"), m=("human", "mean"))
g["gap"] = (2 * g.m - 1).abs()
cand = g[(g.n >= 300) & (~g.index.isin(v08_pairs))].sort_values("gap")
print(cand.round(3).to_string())
top = list(cand.index[:6])
pool = rows[rows.pair.isin(top)].copy()
assert not set(pool.battle_id) & used
pool["pair_id"] = pool.pair.map({p: 10 + i for i, p in enumerate(top)})
pool["len_x"] = pool.resp_x.str.len(); pool["len_y"] = pool.resp_y.str.len()
pool = pool[["battle_id","pair_id","model_x","model_y","prompt","resp_x","resp_y","human","len_x","len_y"]].sort_values(["pair_id","battle_id"]).reset_index(drop=True)
pool.to_parquet(OUT, index=False)
print(pool.groupby(["pair_id","model_x","model_y"]).agg(n=("human","size"), gap=("human", lambda h: abs(2*h.mean()-1))).round(3).to_string())
