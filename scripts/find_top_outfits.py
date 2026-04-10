from __future__ import annotations

import argparse

import numpy as np
import pandas as pd

from fashion_engine.compatibility import compatibility_score, load_compatibility_model
from fashion_engine.config import get_paths


TOPS = {"Shirts", "Tshirts", "Tops", "Kurtas", "Sweatshirts", "Jackets", "Sweaters"}
BOTTOMS = {"Jeans", "Trousers", "Shorts", "Skirts", "Leggings", "Track Pants"}
SHOES = {"Casual Shoes", "Sports Shoes", "Formal Shoes", "Flats", "Heels", "Sandals", "Flip Flops"}
DRESSES = {"Dresses"}


def subset(catalog: pd.DataFrame, article_types: set[str], limit: int) -> pd.DataFrame:
    return catalog[catalog["article_type"].isin(article_types)].head(limit)


def add_pairs(
    pairs: list[tuple[float, int, int]],
    left_df: pd.DataFrame,
    right_df: pd.DataFrame,
    embeddings: np.ndarray,
    model,
) -> None:
    for left_idx, left in left_df.iterrows():
        for right_idx, right in right_df.iterrows():
            if left_idx == right_idx:
                continue
            if str(left.get("gender", "")) != str(right.get("gender", "")):
                continue
            if str(left.get("usage", "")) and str(right.get("usage", "")) and left.get("usage") != right.get("usage"):
                continue
            score = compatibility_score(embeddings[left_idx], embeddings[right_idx], model)
            pairs.append((score, left_idx, right_idx))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-per-type", type=int, default=160)
    parser.add_argument("--top-k", type=int, default=20)
    args = parser.parse_args()

    paths = get_paths()
    catalog = pd.read_csv(paths.catalog_csv).reset_index(drop=True)
    embeddings = np.load(paths.embeddings_npy)
    catalog = catalog.iloc[: len(embeddings)].copy().reset_index(drop=True)
    model = load_compatibility_model(paths.compatibility_model)

    pairs: list[tuple[float, int, int]] = []
    add_pairs(pairs, subset(catalog, TOPS, args.limit_per_type), subset(catalog, BOTTOMS, args.limit_per_type), embeddings, model)
    add_pairs(pairs, subset(catalog, TOPS, args.limit_per_type), subset(catalog, SHOES, args.limit_per_type), embeddings, model)
    add_pairs(pairs, subset(catalog, BOTTOMS, args.limit_per_type), subset(catalog, SHOES, args.limit_per_type), embeddings, model)
    add_pairs(pairs, subset(catalog, DRESSES, args.limit_per_type), subset(catalog, SHOES, args.limit_per_type), embeddings, model)

    for rank, (score, left_idx, right_idx) in enumerate(sorted(pairs, reverse=True)[: args.top_k], start=1):
        left = catalog.loc[left_idx]
        right = catalog.loc[right_idx]
        print(f"\n{rank}. Score: {score * 100:.1f}%")
        print(f"   A: {left['item_id']}.jpg | {left['gender']} | {left['article_type']} | {left['base_colour']} | {left['usage']} | {left['product_name']}")
        print(f"      {left['image_path']}")
        print(f"   B: {right['item_id']}.jpg | {right['gender']} | {right['article_type']} | {right['base_colour']} | {right['usage']} | {right['product_name']}")
        print(f"      {right['image_path']}")


if __name__ == "__main__":
    main()
