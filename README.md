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
│   ├── Ch1.R (introduction)
│   ├── Ch2.R (modeling)
│   ├── ch3.R
│   ├── ch4.R
│   ├── Ch5.R
│   ├── Ch6.R
│   ├── Ch7.R
│   ├── Ch8.R
│   ├── Ch9.R
│   ├── Ch10.R
│   └── Ch11.R
├── datasets/                  # Data files
│   ├── cast.txt              # Ch8 (cast fatigue)
│   ├── so2.csv               # Ch9 (SO2 nonlinear model)
│   ├── wind10.csv            # Ch10, Ch11 (wind power)
│   ├── Concrete_Data.csv     # Ch11 (concrete strength)
│   └── functional/           # Ch9 (VPI functional output data)
└── python/
    ├── ch1.py                 # Python port of Ch1.R (Introduction)
    ├── ch2.py                 # Python port of Ch2.R (Modeling)
    ├── ch3.py                 # Python port of ch3.R (pure Python)
    ├── ch4.py                 # Python port of ch4.R
    ├── ch5.py                 # Python port of Ch5.R (Representative Points)
    ├── ch6.py                 # Python port of Ch6.R (Screening Designs)
    ├── ch7.py                 # Python port of Ch7.R (Sequential Designs)
    ├── ch8.py                 # Python port of Ch8.R (Multi-level and Mixture Designs)
    ├── ch9.py                 # Python port of Ch9.R (Model Calibration)
    ├── ch10.py                # Python port of Ch10.R (Data Subsampling)
    ├── ch11.py                # Python port of Ch11.R (Data Analysis)
    ├── r_utils.py             # Minimal R wrapper runner (CSV handoff)
    ├── r_wrappers/            # R scripts called from Python
    ├── figures/               # Output figures (generated)
    └── notebooks/             # Jupyter notebooks that call the Python modules
        ├── ch1.ipynb
        ├── ch2.ipynb
        ├── ch3.ipynb
        ├── ch4.ipynb
        ├── ch5.ipynb
        ├── ch6.ipynb
        ├── ch7.ipynb
        ├── ch8.ipynb
        ├── ch9.ipynb
        ├── ch10.ipynb
        └── ch11.ipynb
```

## Notes

- `minimaxdesign`, `zipcodeR` are excluded due to package conflicts.
- Ch5 PQMC section (Figure 5.9) is excluded due to external GitHub dependency.

## How to run (recommended)

Open the notebooks and run all cells:

```bash
jupyter lab python/notebooks/ch1.ipynb   # Introduction
jupyter lab python/notebooks/ch2.ipynb   # Modeling
jupyter lab python/notebooks/ch3.ipynb
jupyter lab python/notebooks/ch4.ipynb
# ... up to ch11.ipynb
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

**Ch8 (Multi-level and Mixture Designs):**
- `HiGarrote` (automated variable selection)
- `DoE.base` (orthogonal arrays L9, L18)
- `twinning` (MaxPro criterion, energy distance)
- `mixexp` (simplex lattice/centroid designs)

**Ch9 (Model Calibration):**
- `ICAOD` (optimal design algorithms)
- `numDeriv` (numerical differentiation)

**Ch10 (Data Subsampling):**
- `SPlit` (stratified data splitting)
- `BalancedSampling` (LPM1, LPM2, energy, spatial balance)
- `supercompress` (supervised compression)

**Ch11 (Data Analysis):**
- `first` (factor importance ranking)
- `randomForest` (random forest regression)
- `twingp` (twin-Gaussian process)

