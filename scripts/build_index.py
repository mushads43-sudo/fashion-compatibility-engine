from __future__ import annotations

import argparse
import numpy as np

from fashion_engine.config import get_paths
from fashion_engine.search import train_search_index


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pca-components", type=int, default=256)
    parser.add_argument("--clusters", type=int, default=24)
    args = parser.parse_args()

    paths = get_paths()
    embeddings = np.load(paths.embeddings_npy)
    artifacts = train_search_index(
        embeddings,
        paths.index_joblib,
        pca_components=args.pca_components,
        n_clusters=args.clusters,
    )
    print(
        f"Saved search index to {paths.index_joblib}. "
        f"Compressed shape: {artifacts.compressed_embeddings.shape}"
    )


if __name__ == "__main__":
    main()
