from __future__ import annotations

import argparse
import json
import numpy as np

from fashion_engine.compatibility import train_compatibility_model
from fashion_engine.config import get_paths
from fashion_engine.data import category_aware_pairs, load_catalog


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pairs", type=int, default=50000)
    args = parser.parse_args()

    paths = get_paths()
    catalog = load_catalog(paths.catalog_csv)
    embeddings = np.load(paths.embeddings_npy)
    pairs = category_aware_pairs(catalog, max_pairs=args.max_pairs)
    artifacts = train_compatibility_model(pairs, embeddings, paths.compatibility_model)
    metrics_path = paths.artifacts_dir / "compatibility_metrics.json"
    metrics_path.write_text(json.dumps(artifacts.metrics, indent=2), encoding="utf-8")
    print(f"Saved compatibility model to {paths.compatibility_model}")
    print(json.dumps(artifacts.metrics, indent=2))


if __name__ == "__main__":
    main()
