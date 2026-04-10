from __future__ import annotations

from pathlib import Path
import shutil

import numpy as np
import pandas as pd

from fashion_engine.config import get_paths


def main() -> None:
    paths = get_paths()
    root = paths.root
    deploy_dir = root / "deploy_data"
    image_dir = deploy_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    catalog = pd.read_csv(paths.catalog_csv)
    embeddings = np.load(paths.embeddings_npy)
    catalog = catalog.iloc[: len(embeddings)].copy().reset_index(drop=True)

    new_paths = []
    copied = 0
    for _, row in catalog.iterrows():
        source = Path(row["image_path"])
        suffix = source.suffix or ".jpg"
        target = image_dir / f"{row['item_id']}{suffix}"
        if source.exists() and not target.exists():
            shutil.copy2(source, target)
            copied += 1
        new_paths.append(str(target.relative_to(root)))

    catalog["image_path"] = new_paths
    catalog.to_csv(deploy_dir / "catalog.csv", index=False)
    shutil.copy2(paths.embeddings_npy, deploy_dir / "embeddings.npy")
    shutil.copy2(paths.index_joblib, deploy_dir / "search_index.joblib")
    shutil.copy2(paths.compatibility_model, deploy_dir / "compatibility_model.joblib")

    metrics = paths.artifacts_dir / "compatibility_metrics.json"
    if metrics.exists():
        shutil.copy2(metrics, deploy_dir / "compatibility_metrics.json")

    print(f"Deployment bundle written to {deploy_dir}")
    print(f"Catalog rows: {len(catalog):,}")
    print(f"Images copied this run: {copied:,}")
    print("Use `streamlit run app.py` to test the deploy entrypoint.")


if __name__ == "__main__":
    main()
