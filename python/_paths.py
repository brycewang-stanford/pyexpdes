from __future__ import annotations

from pathlib import Path


PYTHON_DIR = Path(__file__).resolve().parent
REPO_ROOT = PYTHON_DIR.parent


def figures_dir(module: str) -> Path:
    d = PYTHON_DIR / "figures" / module
    d.mkdir(parents=True, exist_ok=True)
    return d


