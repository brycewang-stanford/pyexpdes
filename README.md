# pyexpdes

Python codes for the book Experimental Design for Data Science and Engineering by V. Roshan Joseph

## Pythonized R scripts

The `python/` directory mirrors the original content from `R files/` without
modifying the R sources. Each translation preserves fidelity to the original R
behavior:

- `python/src/introduction.py` and `python/notebooks/introduction.ipynb` replicate
  `R files/introduction.R`.
- R-only functionality (e.g., `support::sp`, `rkriging::Fit.Kriging`) is invoked
  through [`rpy2`](https://rpy2.github.io/) wrappers so the numerical results
  match the R implementation. Ensure the R packages **support** and **rkriging**
  are installed in your R environment.

Run the notebook or import the module to generate the same figures as the R
script.
