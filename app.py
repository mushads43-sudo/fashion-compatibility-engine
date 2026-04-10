"""Deployment entrypoint for Streamlit Cloud and Hugging Face Spaces.

This file points the app to the lightweight deploy_data/ bundle when it exists.
For local development, app/streamlit_app.py can still be run directly.
"""

from __future__ import annotations

import os
from pathlib import Path
import runpy


DEPLOY_DATA = Path("deploy_data")

if DEPLOY_DATA.exists():
    os.environ.setdefault("FASHION_CATALOG_CSV", str(DEPLOY_DATA / "catalog.csv"))
    os.environ.setdefault("FASHION_EMBEDDINGS", str(DEPLOY_DATA / "embeddings.npy"))
    os.environ.setdefault("FASHION_INDEX", str(DEPLOY_DATA / "search_index.joblib"))
    os.environ.setdefault("FASHION_COMPAT_MODEL", str(DEPLOY_DATA / "compatibility_model.joblib"))

runpy.run_path("app/streamlit_app.py", run_name="__main__")
