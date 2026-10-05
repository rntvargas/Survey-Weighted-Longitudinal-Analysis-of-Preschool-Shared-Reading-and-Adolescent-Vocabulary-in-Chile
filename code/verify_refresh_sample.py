"""Checks the Panel/Nueva split (variable tipol: 1 = Panel, 2 = Nueva) in the ORIGINAL 2012 assessment file.

Usage (from the repository root):
    python code/verify_refresh_sample.py path/to/evaluaciones_2012.dta data/cohorte_2012_2024.csv
Targets in the paper: Panel = 11,692; Panel aged 36-71 months = 9,561; all aged 36-71 months = 9,669."""
import sys
import pandas as pd

ev = pd.read_stata(sys.argv[1], convert_categoricals=False, columns=["folio", "tipol", "edad_meses"])
c = pd.read_csv(sys.argv[2])
ev["tipo"] = ev.tipol.map({1: "Panel", 2: "Nueva"})
ev["edad_ok"] = ev.edad_meses.between(36, 71)
print(len(ev), "assessments;", ev.folio.nunique(), "unique folio")
print(ev.tipo.value_counts(dropna=False).to_string())
print("Aged 36-71 months:")
print(ev[ev.edad_ok].tipo.value_counts(dropna=False).to_string())
print("Supplementary cohort members:")
print(ev[ev.folio.isin(c.folio)].tipo.value_counts(dropna=False).to_string())
