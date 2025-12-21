# pyexpdes

Python-first reimplementation of selected examples from _Experimental Design for Data Science and Engineering_
by V. Roshan Joseph, with **book-faithful figure settings** and **minimal R usage**.

## What this repo is trying to achieve

- **Source code** is shipped as Python modules (one per original R file).
- **Plots are generated from notebooks** (one notebook per original R file).
- **R is used only when necessary** to match the book outputs (via small CSV-based wrappers).

## Project structure

```
pyexpdes/
├── R files/                   # Original R scripts
│   ├── introduction.R
│   ├── ch3.R
│   ├── ch4.R
│   └── modeling.R
└── python/
    ├── introduction.py        # Python port of introduction.R (R wrappers only where required)
    ├── ch3.py                 # Python port of ch3.R (pure Python)
    ├── ch4.py                 # Python port of ch4.R (Python-first + optional small R wrappers)
    ├── modeling.py            # Python port of modeling.R (R wrappers only where required)
    ├── r_utils.py             # Minimal R wrapper runner (CSV handoff)
    ├── r_wrappers/            # Small R scripts called from Python
    ├── figures/               # Output figures (generated)
    └── notebooks/             # Jupyter notebooks that call the Python modules
        ├── introduction.ipynb
        ├── ch3.ipynb
        ├── ch4.ipynb
        └── modeling.ipynb
```

## Important note: `minimaxdesign` is excluded

The R package **`minimaxdesign` is intentionally not used** due to package conflicts (as discussed).
Any code paths that would depend on `minimaxdesign` are omitted, and this is documented in the Chapter 4 notebook/module.

## Important note: `zipcodeR` is excluded

The R package **`zipcodeR` is intentionally not used** (dataset/package availability varies and it is not required for the core chapter concepts).
This means the **"Minimum energy designs" example that pulls `zip_code_db` cannot be reproduced exactly** from the book without an equivalent dataset.
All other Chapter 4 sections are implemented Python-first, using small CSV-based R wrappers only where the book relies on specialized R algorithms.

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
- `support` (for `support::sp`)
- `rkriging` (for GP regression panels matching the book)
- `AlgDesign` (for `optFederov`, when matching D-optimal designs in the book)

