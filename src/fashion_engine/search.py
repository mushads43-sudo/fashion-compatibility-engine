from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


@dataclass
class SearchArtifacts:
    pca: PCA
    nn: NearestNeighbors
    clusters: KMeans
    compressed_embeddings: np.ndarray


def train_search_index(
    embeddings: np.ndarray,
    output_path: Path,
    pca_components: int = 256,
    n_clusters: int = 24,
    random_state: int = 42,
) -> SearchArtifacts:
    components = min(pca_components, embeddings.shape[1], embeddings.shape[0] - 1)
    if components < 2:
        raise ValueError("Need at least 3 images to build a PCA search index.")
    pca = PCA(n_components=components, random_state=random_state)
    compressed = pca.fit_transform(embeddings).astype("float32")
    compressed = compressed / np.maximum(np.linalg.norm(compressed, axis=1, keepdims=True), 1e-12)

    cluster_count = min(n_clusters, len(compressed))
    clusters = KMeans(n_clusters=cluster_count, random_state=random_state, n_init="auto")
    clusters.fit(compressed)

    nn = NearestNeighbors(metric="cosine", algorithm="brute")
    nn.fit(compressed)
    artifacts = SearchArtifacts(pca=pca, nn=nn, clusters=clusters, compressed_embeddings=compressed)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifacts, output_path)
    return artifacts


def load_search_index(path: Path) -> SearchArtifacts:
    if not path.exists():
        raise FileNotFoundError(f"Search index not found at {path}. Run scripts/build_index.py.")
    return joblib.load(path)


def search_similar(
    query_embedding: np.ndarray,
    artifacts: SearchArtifacts,
    catalog: pd.DataFrame,
    top_k: int = 8,
) -> list[dict]:
    query = artifacts.pca.transform(query_embedding.reshape(1, -1)).astype("float32")
    query = query / np.maximum(np.linalg.norm(query, axis=1, keepdims=True), 1e-12)
    distances, indices = artifacts.nn.kneighbors(query, n_neighbors=min(top_k, len(catalog)))
    results = []
    for distance, idx in zip(distances[0], indices[0]):
        row = catalog.iloc[int(idx)].to_dict()
        row["similarity"] = float(1.0 - distance)
        row["style_cluster"] = int(artifacts.clusters.labels_[int(idx)])
        results.append(row)
    return results
