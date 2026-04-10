from __future__ import annotations

import argparse
import numpy as np

from fashion_engine.config import get_paths
from fashion_engine.data import load_catalog
from fashion_engine.embeddings import embed_images


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--limit", type=int, default=None, help="Use a small number for quick demos.")
    args = parser.parse_args()

    paths = get_paths()
    catalog = load_catalog(paths.catalog_csv)
    if args.limit:
        catalog = catalog.head(args.limit).copy()
        catalog.to_csv(paths.catalog_csv, index=False)
    embeddings = embed_images(catalog["image_path"].tolist(), batch_size=args.batch_size)
    paths.embeddings_npy.parent.mkdir(parents=True, exist_ok=True)
    np.save(paths.embeddings_npy, embeddings)
    print(f"Saved embeddings {embeddings.shape} to {paths.embeddings_npy}")


if __name__ == "__main__":
    main()
