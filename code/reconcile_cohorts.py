"""Folio-level reconciliation between the primary analytic sample and the supplementary cohort.

Usage (from the repository root):
    python code/reconcile_cohorts.py primary_folios.csv
primary_folios.csv: column 'folio'; optional 0/1 columns 'in_6295' and 'in_5016'."""
import sys
import pandas as pd

c = pd.read_csv("data/cohorte_2012_2024.csv")
p = pd.read_csv(sys.argv[1])
m = p.merge(c[["folio", "f_exp_10121724"]].assign(in_supp=1), on="folio", how="left")
m["in_supp"] = m["in_supp"].fillna(0).astype(int)
print("Primary children listed:", len(p), "| in supplementary cohort:", int(m.in_supp.sum()), "| not in it:", int((1 - m.in_supp).sum()))
print("With four-wave weight among those in the supplementary cohort:", int(m[m.in_supp == 1].f_exp_10121724.notna().sum()))
for col in ["in_6295", "in_5016"]:
    if col in p.columns:
        print(col, int(p[col].sum()), "| in supplementary cohort:", int(m.loc[p[col] == 1, "in_supp"].sum()))
only = c[~c.folio.isin(p.folio)]
print("Supplementary children not in the primary list:", len(only), "| with four-wave weight:", int(only.f_exp_10121724.notna().sum()))
