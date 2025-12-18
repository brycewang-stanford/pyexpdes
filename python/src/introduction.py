"""Python translation of ``R files/introduction.R``.

This module mirrors the original R script while keeping R-only functionality
via thin wrappers around ``support`` and ``rkriging`` using ``rpy2``.
"""
from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from rpy2 import robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects.conversion import localconverter

from .r_bridge import fit_rkriging, predict_rkriging, space_filling_design

np.random.seed(1)


# Helper functions -----------------------------------------------------------------

def _mixture_beta_density(x: np.ndarray) -> np.ndarray:
    return (2 / 3) * robjects.r["dbeta"](x, 2, 10) + (1 / 3) * robjects.r["dbeta"](x, 10, 2)


def _rough_function(x: np.ndarray) -> np.ndarray:
    return np.sin(10 * np.pi * x) / (1 + 64 * (x - 0.5) ** 2)


def _smooth_function(x: np.ndarray) -> np.ndarray:
    return 1 / (1 + 64 * (x - 0.5) ** 2)


def _gp_truth(x: np.ndarray) -> np.ndarray:
    return np.sin(10 * np.pi * x) / (1 + 64 * (x - 0.25) ** 2) + x**2


# Plotting routines ----------------------------------------------------------------

def plot_design_objectives(n: int = 15) -> None:
    """Recreate the four-panel plot from ``introduction.R``."""

    x = np.linspace(0, 1, 301)
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Approximate a rough function
    y1 = _rough_function(x)
    D1 = (np.arange(1, n + 1) - 0.5) / n
    axes[0, 0].plot(x, y1, "k-", linewidth=3)
    axes[0, 0].scatter(D1, np.full_like(D1, np.min(y1) - 0.05), color="blue", s=64)
    axes[0, 0].set_title("approximate a rough function")
    axes[0, 0].axis("off")

    # 2. Approximate a smooth function
    y2 = _smooth_function(x)
    D2 = robjects.r["qbeta"]((np.arange(1, n + 1) - 0.5) / n, 0.5, 0.5)
    axes[0, 1].plot(x, y2, "k-", linewidth=3)
    axes[0, 1].scatter(D2, np.full_like(D2, np.min(y2) - 0.05), color="blue", s=64)
    axes[0, 1].set_title("approximate a smooth function")
    axes[0, 1].axis("off")

    # 3. Optimization
    n1 = int(n * 2 / 3)
    n2 = int(n / 3)
    y3 = _mixture_beta_density(x)
    D0 = (np.arange(1, n2 + 1) - 0.5) / n2
    D_beta = robjects.r["qbeta"]((np.arange(1, n1 + 1) - 0.5) / n1, 2, 10)
    D3 = np.concatenate([D0, np.array(D_beta)])
    axes[1, 0].plot(x, y3, "k-", linewidth=3)
    axes[1, 0].scatter(D3, np.full_like(D3, np.min(y3) - 0.05), color="blue", s=64)
    axes[1, 0].set_title("optimization")
    axes[1, 0].axis("off")

    # 4. Uncertainty propagation (delegates to support::sp)
    y4 = _mixture_beta_density(x)
    samples = np.concatenate(
        [np.random.beta(2, 10, 1000 * n1), np.random.beta(10, 2, 1000 * n2)]
    )
    with localconverter(robjects.default_converter + numpy2ri.converter):
        D4 = np.array(space_filling_design(samples, n))
    axes[1, 1].plot(x, y4, "k-", linewidth=3)
    axes[1, 1].scatter(D4, np.full_like(D4, np.min(y4) - 0.05), color="blue", s=64)
    axes[1, 1].set_title("uncertainty propagation")
    axes[1, 1].axis("off")

    fig.tight_layout()


def compare_regressors(n: int = 10) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return prediction summaries for linear regression and R-based Gaussian process."""

    x_obs = np.repeat([0, 1], repeats=n // 2)
    y_obs = _gp_truth(x_obs) + 0.1 * np.random.normal(size=n)

    test_grid = np.linspace(-0.1, 1.1, 1000)
    truth = _gp_truth(test_grid)

    # Linear regression via numpy (matches R's lm for this simple design)
    X = np.vstack([np.ones_like(x_obs), x_obs]).T
    beta_hat = np.linalg.lstsq(X, y_obs, rcond=None)[0]
    pred_mean = beta_hat[0] + beta_hat[1] * test_grid

    # Classical prediction interval as in the R example
    residuals = y_obs - (beta_hat[0] + beta_hat[1] * x_obs)
    mse = np.mean(residuals**2)
    leverage = 1 / n + (test_grid - x_obs.mean()) ** 2 / np.sum((x_obs - x_obs.mean()) ** 2)
    pred_std = np.sqrt(mse * (1 + leverage))
    pred_lower = pred_mean - 2 * pred_std
    pred_upper = pred_mean + 2 * pred_std

    # Gaussian process regression using rkriging
    with localconverter(robjects.default_converter + numpy2ri.converter):
        fit = fit_rkriging(x_obs, y_obs)
        gp_mean, gp_sd = predict_rkriging(fit, test_grid)
        gp_mean = np.array(gp_mean)
        gp_sd = np.array(gp_sd)

    return (
        test_grid,
        truth,
        pred_mean,
        pred_lower,
        pred_upper,
        gp_mean,
        gp_sd,
        x_obs,
        y_obs,
    )


def plot_regression_comparison() -> None:
    (
        test_grid,
        truth,
        pred_mean,
        pred_lower,
        pred_upper,
        gp_mean,
        gp_sd,
        x_obs,
        y_obs,
    ) = compare_regressors()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Linear regression panel
    axes[0].plot(test_grid, truth, "k-", linewidth=2, label="truth")
    axes[0].fill_between(test_grid, pred_lower, pred_upper, color="pink", alpha=0.6)
    axes[0].plot(test_grid, pred_mean, "g--", linewidth=3, label="prediction")
    axes[0].scatter(x_obs, y_obs, color="blue", s=60)
    axes[0].set_xlim(-0.1, 1.1)
    axes[0].set_ylim(-0.5, 1.5)
    axes[0].set_title("Linear regression")
    axes[0].legend()

    # Gaussian process panel
    axes[1].plot(test_grid, truth, "k-", linewidth=2, label="truth")
    axes[1].fill_between(test_grid, gp_mean - 2 * gp_sd, gp_mean + 2 * gp_sd, color="pink", alpha=0.6)
    axes[1].plot(test_grid, gp_mean, "g--", linewidth=3, label="prediction")
    axes[1].scatter(x_obs, y_obs, color="blue", s=60)
    axes[1].set_xlim(-0.1, 1.1)
    axes[1].set_ylim(-0.5, 1.5)
    axes[1].set_title("Gaussian process regression (rkriging)")
    axes[1].legend()

    fig.tight_layout()
