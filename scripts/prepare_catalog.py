from __future__ import annotations

from pathlib import Path
import argparse

from fashion_engine.config import get_paths
from fashion_engine.data import build_catalog_from_fashion_products


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=None,
        help="Folder containing styles.csv and images/. Default: data/raw/fashion-product-images",
    )
    args = parser.parse_args()
    paths = get_paths()
    raw_dir = args.raw_dir or paths.raw_dir / "fashion-product-images"
    catalog = build_catalog_from_fashion_products(raw_dir, paths.catalog_csv)
    print(f"Saved {len(catalog):,} catalog rows to {paths.catalog_csv}")


if __name__ == "__main__":
    main()
