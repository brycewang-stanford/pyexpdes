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

## note: `minimaxdesign`, `zipcodeR` is excluded

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

