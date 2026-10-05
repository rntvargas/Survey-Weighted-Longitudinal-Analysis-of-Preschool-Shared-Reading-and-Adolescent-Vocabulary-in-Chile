"""Leave-one-region-out (LORO) ridge validation for the supplementary cohort.

Run from the repository root after rebuilding data/cohorte_2012_2024.csv (child-level file, NOT included here; see data/README.md).
Writes results/loro_summary.csv and results/loro_by_region.csv."""
import os
import numpy as np, pandas as pd
from sklearn.linear_model import RidgeCV
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

c = pd.read_csv("data/cohorte_2012_2024.csv")
basic = ["edad_2012_meses", "tvip_2012", "sexo_2012"]
full = basic + ["educ_madre_codigo_2012", "integrantes_hogar_2012", "madre_conviviente_registrada",
                "hm2_1", "hm2_2", "hm2_4", "hm2_5", "hm2_10", "hm2_11", "hm2_15"]

def fit_predict(tr, te, cols):
    m = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(), RidgeCV(alphas=np.logspace(-2, 3, 30)))
    m.fit(tr[cols], tr.tvip_2024)
    return m.predict(te[cols])

P = {k: np.zeros(len(c)) for k in ["mean", "basic", "full"]}
for r in sorted(c.region_2012.unique()):
    te = (c.region_2012 == r).values
    tr, tt = c[~te], c[te]
    P["mean"][te] = tr.tvip_2024.mean()
    P["basic"][te] = fit_predict(tr, tt, basic)
    P["full"][te] = fit_predict(tr, tt, full)

y = c.tvip_2024.values
reg = c.region_2012.values
regs = np.unique(reg)

def metrics(i, p):
    e = y[i] - p[i]
    return np.abs(e).mean(), np.sqrt((e ** 2).mean()), 1 - (e ** 2).sum() / ((y[i] - y[i].mean()) ** 2).sum()  # R2 computed once on pooled predictions

allidx = np.arange(len(y))
rm = {k: np.array([metrics(np.where(reg == r)[0], P[k])[1] for r in regs]) for k in P}
rng = np.random.default_rng(42)
idx = {r: np.where(reg == r)[0] for r in regs}
boot, macro = [], []
for _ in range(2000):  # percentile bootstrap resampling regions
    s = rng.integers(0, len(regs), len(regs))
    i = np.concatenate([idx[regs[j]] for j in s])
    boot.append([metrics(i, P[k]) for k in P])
    macro.append([rm[k][s].mean() for k in P])
boot, macro = np.array(boot), np.array(macro)
lo, hi = np.percentile(boot, 2.5, axis=0), np.percentile(boot, 97.5, axis=0)
mlo, mhi = np.percentile(macro, 2.5, axis=0), np.percentile(macro, 97.5, axis=0)

rows = []
for q, k in enumerate(P):
    mae, rmse, r2 = metrics(allidx, P[k])
    rows.append(dict(model=k, MAE=mae, RMSE=rmse, RMSE_lo=lo[q][1], RMSE_hi=hi[q][1], macro_RMSE=rm[k].mean(),
                     macro_lo=mlo[q], macro_hi=mhi[q], R2=r2, R2_lo=lo[q][2], R2_hi=hi[q][2]))
summary = pd.DataFrame(rows).round(3)
by_region = pd.DataFrame({"region": regs.astype(int), "n": [len(idx[r]) for r in regs],
                          **{f"RMSE_{k}": rm[k].round(3) for k in P}})
os.makedirs("results", exist_ok=True)
summary.to_csv("results/loro_summary.csv", index=False)
by_region.to_csv("results/loro_by_region.csv", index=False)
print(summary.to_string(index=False))
print(by_region.to_string(index=False))
