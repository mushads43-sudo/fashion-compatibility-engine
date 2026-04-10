from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Paths:
    root: Path
    raw_dir: Path
    processed_dir: Path
    artifacts_dir: Path
    catalog_csv: Path
    embeddings_npy: Path
    index_joblib: Path
    compatibility_model: Path


def get_paths() -> Paths:
    root = Path(os.getenv("FASHION_ENGINE_ROOT", ".")).resolve()
    return Paths(
        root=root,
        raw_dir=root / "data" / "raw",
        processed_dir=root / "data" / "processed",
        artifacts_dir=root / "artifacts",
        catalog_csv=Path(os.getenv("FASHION_CATALOG_CSV", root / "data" / "processed" / "catalog.csv")).resolve(),
        embeddings_npy=Path(os.getenv("FASHION_EMBEDDINGS", root / "data" / "processed" / "embeddings.npy")).resolve(),
        index_joblib=Path(os.getenv("FASHION_INDEX", root / "data" / "processed" / "search_index.joblib")).resolve(),
        compatibility_model=Path(
            os.getenv("FASHION_COMPAT_MODEL", root / "artifacts" / "compatibility_model.joblib")
        ).resolve(),
    )


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
