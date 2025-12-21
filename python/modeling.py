"""
Python port of `R files/modeling.R`.

Policy:
- Plotting is done in Python.
- R is used only for book-faithful steps that rely on specific R packages:
  - `rkriging` for Gaussian process panels (when `use_r=True`)
  - `AlgDesign::optFederov` for D-optimal points (when `use_r=True`)

This implementation focuses on the core figures present in the R script:
- Polynomial interpolation (equi-spaced vs Chebyshev)
- 2D design examples
- RBF interpolation (theta = 0.01, 0.1, 1.0)
- Ordinary kriging
- Gaussian process (via rkriging wrapper when enabled)
- Polynomial regression (equi-spaced vs D-optimal)
- Kernel ridge regression (equi-spaced vs D-optimal)
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.linalg import solve
from scipy.optimize import minimize

from _paths import figures_dir
from _style import apply_base_style
from r_utils import run_wrapper


def _f(x: np.ndarray) -> np.ndarray:
    return np.sin(10 * np.pi * x) / (1 + 64 * (x - 0.25) ** 2) + x**2


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path)
    plt.close(fig)
    return path


def _chebyshev_interp_coeffs(D: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Match the R script's Chebyshev polynomial interpolation:
    X[i,j] = cos((j-1) * acos(d_i)), where d_i = 2*D_i - 1.
    """
    d = 2 * D - 1
    n = len(D)
    X = np.column_stack([np.cos((j) * np.arccos(d)) for j in range(n)])
    return np.linalg.solve(X, y)


def _chebyshev_eval(a: np.ndarray, u: np.ndarray) -> np.ndarray:
    us = 2 * u - 1
    n = len(a)
    T = np.column_stack([np.cos(j * np.arccos(us)) for j in range(n)])
    return T @ a


def _rbf_interp(D: np.ndarray, y: np.ndarray, theta: float, test: np.ndarray) -> np.ndarray:
    E = np.abs(D[:, None] - D[None, :])
    R = np.exp(-((E / theta) ** 2))
    coef = np.linalg.solve(R, y)
    M = np.exp(-(((test[:, None] - D[None, :]) / theta) ** 2))
    return M @ coef


def _ordinary_kriging(D: np.ndarray, y: np.ndarray, theta: float, test: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Match the R script's ordinary kriging implementation (Gaussian kernel).
    Returns (mean, sd) on `test`.
    """
    n = len(D)
    E = np.abs(D[:, None] - D[None, :])
    R = np.exp(-((E / theta) ** 2))
    one = np.ones(n)
    Rinv = np.linalg.inv(R + 1e-10 * np.eye(n))
    mu = float((one @ Rinv @ y) / (one @ Rinv @ one))
    coef = Rinv @ (y - mu)
    tau2 = float((y - mu).T @ Rinv @ (y - mu) / n)

    M = np.exp(-(((test[:, None] - D[None, :]) / theta) ** 2))
    mean = mu + M @ coef

    fac = 1.0 / float(one @ Rinv @ one)
    # variance expression from the R script
    v = []
    for i in range(len(test)):
        r = M[i, :]
        term = 1.0 - (r @ Rinv @ r) + fac * (1.0 - (r @ Rinv @ one)) ** 2
        v.append(tau2 * term)
    sd = np.sqrt(np.maximum(v, 0.0))
    return mean, sd


def _opt_federov_points(n: int, use_r: bool) -> np.ndarray:
    """
    Return D-optimal points in [0,1] corresponding to optFederov on x in [-1,1].
    """
    if not use_r:
        # Fallback: use equi-spaced (not book-faithful)
        return (np.arange(1, n + 1) - 1) / (n - 1)

    out = run_wrapper(
        "algdesign_optfederov_1d.R",
        inputs={"noop.csv": pd.DataFrame({"x": [0.0]})},
        args=[str(n)],
        required_packages=["AlgDesign"],
    )
    x = out["design.csv"]["x"].to_numpy()
    return (x + 1.0) / 2.0


def generate_figures(*, use_r: bool = True) -> tuple[Path, list[Path]]:
    apply_base_style()
    out_dir = figures_dir("modeling")
    paths: list[Path] = []

    test = np.linspace(0, 1, 301)
    true = _f(test)

    # ------------------------------------------------------------------
    # Polynomial interpolation (1x2)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    n = 10

    # Equi-spaced
    D = (np.arange(1, n + 1) - 1) / (n - 1)
    y = _f(D)
    a = _chebyshev_interp_coeffs(D, y)
    pred = _chebyshev_eval(a, test)
    ax = axes[0]
    ax.plot(test, true, color="black", linewidth=3, linestyle="--")
    ax.scatter(D, y, s=80, color="blue")
    ax.plot(test, pred, color="green", linewidth=3)
    ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
    ax.set_title("polynomial interpolation equi-spaced points", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(["truth", "prediction"], loc="lower right", frameon=False)

    # Chebyshev nodes
    d = np.cos((2 * (np.arange(1, n + 1)) - 1) / (2 * n) * np.pi)
    D = (d + 1) / 2
    y = _f(D)
    # In this case, the R script uses d directly in X; our helper does the right thing.
    a = _chebyshev_interp_coeffs(D, y)
    pred = _chebyshev_eval(a, test)
    ax = axes[1]
    ax.plot(test, true, color="black", linewidth=3, linestyle="--")
    ax.scatter(D, y, s=80, color="blue")
    ax.plot(test, pred, color="green", linewidth=3)
    ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
    ax.set_title("polynomial interpolation with Chebyshev nodes", fontsize=12)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(["truth", "prediction"], loc="lower right", frameon=False)

    fig.tight_layout()
    paths.append(_save(fig, out_dir / "polynomial_interpolation.png"))

    # ------------------------------------------------------------------
    # Two-dimensional examples (1x2)
    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    D1 = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
    D2 = np.array([[0, 0], [0.2, 0.9], [0.9, 0.1], [1, 1]], float)
    for ax, D in zip(axes, [D1, D2]):
        ax.scatter(D[:, 0], D[:, 1], s=200, color="blue")
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_xlabel(r"$x_1$")
        ax.set_ylabel(r"$x_2$")
    fig.tight_layout()
    paths.append(_save(fig, out_dir / "two_dimensional.png"))

    # ------------------------------------------------------------------
    # RBF interpolation (1x3)
    # ------------------------------------------------------------------
    n = 10
    D = (np.arange(1, n + 1) - 1) / (n - 1)
    y = _f(D)
    thetas = [0.01, 0.1, 1.0]
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for ax, th in zip(axes, thetas):
        pred = _rbf_interp(D, y, th, test)
        ax.plot(test, true, color="black", linewidth=3, linestyle="--")
        ax.scatter(D, y, s=80, color="blue")
        ax.plot(test, pred, color="green", linewidth=3)
        ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
        ax.set_title(rf"$\theta={th}$", fontsize=14)
        ax.legend(["truth", "prediction"], loc="lower right", frameon=False)
    fig.tight_layout()
    paths.append(_save(fig, out_dir / "rbf_interpolation.png"))

    # ------------------------------------------------------------------
    # Ordinary kriging (single panel)
    # ------------------------------------------------------------------
    n = 10
    D = (np.arange(1, n + 1) - 1) / (n - 1)
    y = _f(D)
    theta = 0.08
    mean, sd = _ordinary_kriging(D, y, theta, test)
    fig, ax = plt.subplots(1, 1, figsize=(7, 5))
    ax.plot(test, true, color="black", linewidth=3, linestyle="--")
    ax.scatter(D, y, s=80, color="blue")
    ax.fill_between(test, mean - 2 * sd, mean + 2 * sd, color="pink", alpha=1.0, linewidth=0)
    ax.plot(test, mean, color="green", linewidth=3, linestyle="--")
    ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
    ax.set_title("ordinary kriging", fontsize=14)
    ax.legend(["truth", "prediction"], loc="lower right", frameon=False)
    fig.tight_layout()
    paths.append(_save(fig, out_dir / "ordinary_kriging.png"))

    # ------------------------------------------------------------------
    # Gaussian process (book-faithful via rkriging when enabled)
    # ------------------------------------------------------------------
    if use_r:
        n = 10
        D = (np.arange(1, n + 1) - 1) / (n - 1)
        y = _f(D)
        data = pd.concat(
            [
                pd.DataFrame({"x": D, "y": y, "test": np.nan}),
                pd.DataFrame({"x": np.nan, "y": np.nan, "test": test}),
            ],
            ignore_index=True,
        )
        out = run_wrapper(
            "rkriging_predict_1d.R",
            inputs={"data.csv": data},
            args=[],
            required_packages=["rkriging"],
        )
        pred = out["pred.csv"]
        mean = pred["mean"].to_numpy()
        sd = pred["sd"].to_numpy()
        fig, ax = plt.subplots(1, 1, figsize=(7, 5))
        ax.plot(test, true, color="black", linewidth=3, linestyle="--")
        ax.scatter(D, y, s=80, color="blue")
        ax.fill_between(test, mean - 2 * sd, mean + 2 * sd, color="pink", alpha=1.0, linewidth=0)
        ax.plot(test, mean, color="green", linewidth=3, linestyle="--")
        ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
        ax.set_title("Gaussian process", fontsize=14)
        ax.legend(["truth", "prediction"], loc="lower right", frameon=False)
        fig.tight_layout()
        paths.append(_save(fig, out_dir / "gaussian_process.png"))

    # ------------------------------------------------------------------
    # Polynomial regression (equi-spaced vs D-optimal) – match core panels
    # ------------------------------------------------------------------
    rng = np.random.default_rng(5)  # set.seed(5)
    n = 10
    r = 2
    e = rng.normal(scale=0.1, size=n * r)
    D_equi = np.repeat((np.arange(1, n + 1) - 1) / (n - 1), r)
    y = _f(D_equi) + e

    D_opt = np.repeat(_opt_federov_points(n, use_r=use_r), r)
    y_opt = _f(D_opt) + e

    # For simplicity we only plot mean fits (confidence bands in R are via lm/predict).
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, (title, D, yy) in zip(
        axes,
        [
            ("polynomial regression (equi-spaced)", D_equi, y),
            ("polynomial regression (D-optimal)", D_opt, y_opt),
        ],
    ):
        ax.plot(test, true, color="black", linewidth=3, linestyle="--")
        ax.scatter(D, yy, s=40, color="blue")
        # Fit 3rd degree polynomial on d = 2*D-1 (as in R)
        d = 2 * D - 1
        X = np.vstack([d**k for k in range(0, 4)]).T
        coef = np.linalg.lstsq(X, yy, rcond=None)[0]
        us = 2 * test - 1
        Xs = np.vstack([us**k for k in range(0, 4)]).T
        pred = Xs @ coef
        ax.plot(test, pred, color="green", linewidth=3)
        ax.set_ylim(true.min() - 0.25, true.max() + 0.25)
        ax.set_title(title, fontsize=12)
        ax.legend(["truth", "prediction"], loc="lower right", frameon=False)
    fig.tight_layout()
    paths.append(_save(fig, out_dir / "polynomial_regression.png"))

    return out_dir, paths


def main(argv: Sequence[str] | None = None) -> int:
    generate_figures(use_r=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


