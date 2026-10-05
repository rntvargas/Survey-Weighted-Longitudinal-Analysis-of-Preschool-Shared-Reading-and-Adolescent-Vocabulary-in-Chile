# Survey-Weighted Longitudinal Analysis of Preschool Shared Reading and Adolescent Vocabulary in Chile

Code and aggregate outputs accompanying the paper *Survey-Weighted Longitudinal Analysis of Preschool Shared Reading and Adolescent Vocabulary in Chile* (ICICCDS 2027 submission).

**Authors:** Renato Quispe Vargas, Ana Madeley Yana Yucra, Dina Maribel Yana Yucra (corresponding author), Richar Andre Vilca Solorzano.

## Repository structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── code/
│   ├── loro_ridge.py              # leave-one-region-out ridge validation (pooled and macro RMSE, region bootstrap)
│   ├── reconcile_cohorts.py       # folio-level reconciliation of the primary and supplementary cohorts
│   └── verify_refresh_sample.py   # Panel/Nueva check (tipol) in the original 2012 assessment file
├── data/
│   └── README.md                  # how to rebuild the child-level file (not redistributed)
├── docs/
│   ├── diccionario_cohorte.csv    # data dictionary of the supplementary cohort file
│   ├── etiquetas_stata_originales.json  # original Stata variable and value labels
│   └── inventario.csv             # rows and unique identifiers read from each source file
└── results/
    ├── loro_summary.csv           # LORO accuracy with 95% region-bootstrap intervals (paper Table 3)
    ├── loro_by_region.csv         # RMSE by held-out region (paper Fig. 3C)
    ├── auditoria_ponderadores.csv # audit of the ELPI weights (paper Table 1)
    ├── flujo_cohorte.csv          # flow of the supplementary cohort
    ├── faltantes.csv              # missing data by variable
    ├── descriptivos.csv           # descriptive statistics
    ├── libros_y_vocabulario.csv   # 2024 TVIP by the ten-book criterion
    ├── seleccion_seguimiento.csv  # children retained vs not retained
    ├── metricas_prueba.csv        # original fixed hold-out (regions 1, 10, 12); not used for inference
    └── resumen_ejecucion.json     # run summary and software versions
```

## Data

Child-level files are not redistributed (see `data/README.md` and `.gitignore`). Download the public ELPI microdata from the Observatorio Social:

- 2012, second round: https://observatorio.ministeriodesarrollosocial.gob.cl/elpi-segunda-ronda
- 2024, fourth round: https://observatorio.ministeriodesarrollosocial.gob.cl/elpi-cuarta-ronda

## Reproducing the leave-one-region-out analysis

1. Rebuild `data/cohorte_2012_2024.csv` as described in `data/README.md`.
2. From the repository root:

```bash
pip install -r requirements.txt
python code/loro_ridge.py
```

The script rewrites `results/loro_summary.csv` and `results/loro_by_region.csv`. With the original cohort file it reproduces the paper: pooled RMSE 15.32 (training-fold mean), 14.30 (basic ridge) and 14.04 (ridge with all variables); R-squared 0.16 for the latter.

## Other checks

```bash
python code/reconcile_cohorts.py primary_folios.csv
python code/verify_refresh_sample.py path/to/evaluaciones_2012.dta data/cohorte_2012_2024.csv
```

## Notes

- The survey-weighted primary analysis was run in R (survey 4.5; imputation with smcfcs 2.0.2); its script is not included in this repository.
- Python scripts were written for Python 3.12 and scikit-learn 1.8.0.
- The study was exploratory and not preregistered.
