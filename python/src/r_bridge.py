"""Utilities to call R packages from Python using rpy2.

This module centralizes package import/installation and a couple of thin wrappers
needed for the translated R scripts.
"""
from __future__ import annotations

import logging
from typing import Iterable

from rpy2 import robjects
from rpy2.robjects import numpy2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr

logger = logging.getLogger(__name__)

# Enable automatic numpy <-> R conversion
numpy2ri.activate()


def ensure_r_package(package: str) -> None:
    """Import an R package, attempting to install it if missing.

    Parameters
    ----------
    package:
        Name of the R package to load.

    Raises
    ------
    ImportError
        If the package cannot be imported (and installation fails when attempted).
    """

    try:
        importr(package)
        return
    except Exception:  # noqa: BLE001 - propagate a clearer error below
        logger.info("Attempting to install missing R package %s", package)

    # Fall back to installation via utils if the package is missing.
    utils = importr("utils")
    try:
        utils.install_packages(package)
    except Exception as exc:  # noqa: BLE001 - provide actionable message
        raise ImportError(
            f"R package '{package}' is required but could not be installed: {exc}"
        ) from exc
    importr(package)


def space_filling_design(samples: Iterable[float], n: int) -> robjects.vectors.Vector:
    """Replicate ``support::sp`` to produce a one-dimensional space-filling design.

    This calls the R ``support`` package directly to preserve the original behavior
    from the R scripts.
    """

    ensure_r_package("support")
    support_pkg = importr("support")

    with localconverter(robjects.default_converter + numpy2ri.converter):
        # ``dist.samp`` expects a column matrix of candidate samples
        dist_samp = robjects.r["matrix"](samples, ncol=1)
        design = support_pkg.sp(n=n, t=1, dist_samp=dist_samp)
    return design.rx2("sp")


def fit_rkriging(x, y):
    """Fit a Gaussian kriging model using the R ``rkriging`` package."""

    ensure_r_package("rkriging")
    rkriging_pkg = importr("rkriging")

    # ``kernel.parameters`` becomes ``kernel_parameters`` under rpy2 naming rules
    fit = rkriging_pkg.Fit_Kriging(
        x,
        y,
        interpolation=False,
        fit=True,
        model="OK",
        kernel_parameters={"type": "Gaussian"},
    )
    return fit


def predict_rkriging(model, x_new):
    """Predict using an ``rkriging`` model, returning mean and standard deviation."""

    ensure_r_package("rkriging")
    rkriging_pkg = importr("rkriging")

    predictions = rkriging_pkg.Predict_Kriging(model, x_new)
    mean = predictions.rx2("mean")
    sd = predictions.rx2("sd")
    return mean, sd
