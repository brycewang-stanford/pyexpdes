# pyexpdes

Python-first reimplementation of selected examples from _Experimental Design for Data Science and Engineering_
by V. Roshan Joseph

## What this repo is trying to achieve

- **Source code** is shipped as Python modules (one per original R file).
- **Plots are generated from notebooks** (one notebook per original R file).

## Project structure

```
pyexpdes/
├── R files/                   # Original R scripts
│   ├── introduction.R
│   ├── ch3.R
│   ├── ch4.R
│   ├── Ch5.R
│   ├── Ch6.R
│   ├── Ch7.R
│   └── modeling.R
└── python/
    ├── introduction.py        # Python port of introduction.R (R wrappers only where required)
    ├── ch3.py                 # Python port of ch3.R (pure Python)
    ├── ch4.py                 # Python port of ch4.R (Python-first + optional small R wrappers)
    ├── ch5.py                 # Python port of Ch5.R (Representative Points)
    ├── ch6.py                 # Python port of Ch6.R (Screening Designs)
    ├── ch7.py                 # Python port of Ch7.R (Sequential Designs)
    ├── modeling.py            # Python port of modeling.R (R wrappers only where required)
    ├── r_utils.py             # Minimal R wrapper runner (CSV handoff)
    ├── r_wrappers/            # R scripts called from Python
    ├── figures/               # Output figures (generated)
    └── notebooks/             # Jupyter notebooks that call the Python modules
        ├── introduction.ipynb
        ├── ch3.ipynb
        ├── ch4.ipynb
        ├── ch5.ipynb
        ├── ch6.ipynb
        ├── ch7.ipynb
        └── modeling.ipynb
```

## Notes

- `minimaxdesign`, `zipcodeR` are excluded due to package conflicts.
- Ch5 PQMC section (Figure 5.9) is excluded due to external GitHub dependency.

## How to run (recommended)

Open the notebooks and run all cells:

```bash
jupyter lab python/notebooks/introduction.ipynb
jupyter lab python/notebooks/ch3.ipynb
jupyter lab python/notebooks/ch4.ipynb
jupyter lab python/notebooks/modeling.ipynb
```

Figures are written to `python/figures/<module>/` and displayed in the notebook.

## Dependencies

### Python

- `numpy`, `scipy`, `pandas`, `matplotlib`

### R (only for wrapper-backed steps)

- `Rscript` must be on PATH.

**Core packages:**
- `support` (for `support::sp`)
- `rkriging` (for GP regression)
- `AlgDesign` (for `optFederov`, D-optimal designs)

**Ch5 (Representative Points):**
- `SFDesign`, `spacefillr` (uniform designs, Sobol sequences)
- `mnormt` (multivariate normal)
- `adaptMCMC` (MCMC sampling)

**Ch6 (Screening Designs):**
- `sensitivity` (Sobol indices, DELSA, Morris)
- `MOFAT` (MOFAT designs)

**Ch7 (Sequential Designs):**
- `MaxPro` (MaxPro LHD)
- `OSFD` (output space filling design)
- `FNN`, `pdist` (nearest neighbor, distance calculations)

