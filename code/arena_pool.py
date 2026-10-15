"""Build LMArena pool: English (ascii>95%) single-turn battles of the 6 pairs with most decisive battles; ties kept."""
import pandas as pd, numpy as np, json, sys
SRC, OUT = sys.argv[1], sys.argv[2]
df = pd.read_csv(SRC)
def jl(s):
    try:
        v = json.loads(s)
        return v if isinstance(v, list) else [v]
    except Exception:
        return [s]
P, RA, RB = df.prompt.map(jl), df.response_a.map(jl), df.response_b.map(jl)
def ascii_en(s):
    s = s[:2000]
    return len(s) > 0 and sum(ch.isascii() for ch in s) / len(s) > 0.95
en = P.map(lambda p: ascii_en(' '.join(x or '' for x in p)))
single = (P.map(len) == 1) & (RA.map(len) == 1) & (RB.map(len) == 1)
ok = en & single & RA.map(lambda r: isinstance(r[0], str) and len(r[0]) > 0) & RB.map(lambda r: isinstance(r[0], str) and len(r[0]) > 0)
d = df[ok].copy(); P, RA, RB = P[ok], RA[ok], RB[ok]
print("total", len(df), "EN single-turn non-empty", len(d))
win = np.where(d.winner_model_a == 1, 'a', np.where(d.winner_model_b == 1, 'b', 'tie'))
swap = d.model_a.values > d.model_b.values  # x = alphabetically first
rows = pd.DataFrame(dict(
    battle_id=d.id.astype(str).values,
    model_x=np.where(swap, d.model_b, d.model_a), model_y=np.where(swap, d.model_a, d.model_b),
    prompt=[p[0] for p in P],
    resp_x=[(b if s else a)[0] for a, b, s in zip(RA, RB, swap)],
    resp_y=[(a if s else b)[0] for a, b, s in zip(RA, RB, swap)],
    human=np.where(win == 'tie', 0.5, np.where((win == 'a') ^ swap, 1.0, 0.0))))
rows['pair'] = rows.model_x + ' vs ' + rows.model_y
dec = rows[rows.human != 0.5].groupby('pair').size().sort_values(ascending=False)
top = list(dec.index[:6])
pool = rows[rows.pair.isin(top)].copy()
pool['pair_id'] = pool.pair.map({p: i for i, p in enumerate(top)})
pool['len_x'] = pool.resp_x.str.len(); pool['len_y'] = pool.resp_y.str.len()
pool = pool[['battle_id','pair_id','model_x','model_y','prompt','resp_x','resp_y','human','len_x','len_y']].sort_values(['pair_id','battle_id']).reset_index(drop=True)
assert pool.battle_id.is_unique and not pool.isnull().any().any()
pool.to_parquet(OUT, index=False)
print("7th+ pairs decisive:", dec.iloc[6:9].to_dict())
g = pool.groupby(['pair_id','model_x','model_y']).agg(n=('human','size'), decisive=('human', lambda h: (h != 0.5).sum()), ties=('human', lambda h: (h == 0.5).sum()))
print(g.to_string()); print("pool rows", len(pool))
