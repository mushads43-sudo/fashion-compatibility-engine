from __future__ import annotations

from pathlib import Path
import json
import random
from typing import Iterable

import pandas as pd

from fashion_engine.config import IMAGE_EXTENSIONS


REQUIRED_STYLE_COLUMNS = [
    "id",
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "usage",
    "productDisplayName",
]


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def build_catalog_from_fashion_products(raw_dataset_dir: Path, output_csv: Path) -> pd.DataFrame:
    """Build a catalog from Kaggle Fashion Product Images.

    Expected layout:
      raw_dataset_dir/styles.csv
      raw_dataset_dir/images/<id>.jpg
    """
    styles_csv = raw_dataset_dir / "styles.csv"
    image_dir = raw_dataset_dir / "images"
    if not styles_csv.exists():
        raise FileNotFoundError(f"Missing styles.csv at {styles_csv}")
    if not image_dir.exists():
        raise FileNotFoundError(f"Missing images directory at {image_dir}")

    df = pd.read_csv(styles_csv, on_bad_lines="skip")
    missing = [col for col in REQUIRED_STYLE_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"styles.csv is missing columns: {missing}")

    rows = []
    for _, row in df.iterrows():
        item_id = str(row["id"]).strip()
        image_path = find_image(image_dir, item_id)
        if image_path is None:
            continue
        rows.append(
            {
                "item_id": item_id,
                "image_path": str(image_path.resolve()),
                "gender": clean_text(row["gender"]),
                "master_category": clean_text(row["masterCategory"]),
                "sub_category": clean_text(row["subCategory"]),
                "article_type": clean_text(row["articleType"]),
                "base_colour": clean_text(row["baseColour"]),
                "season": clean_text(row["season"]),
                "usage": clean_text(row["usage"]),
                "product_name": clean_text(row["productDisplayName"]),
            }
        )

    catalog = pd.DataFrame(rows).drop_duplicates("item_id").reset_index(drop=True)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    catalog.to_csv(output_csv, index=False)
    return catalog


def find_image(image_dir: Path, item_id: str) -> Path | None:
    for ext in IMAGE_EXTENSIONS:
        candidate = image_dir / f"{item_id}{ext}"
        if candidate.exists():
            return candidate
    return None


def load_catalog(catalog_csv: Path) -> pd.DataFrame:
    if not catalog_csv.exists():
        raise FileNotFoundError(
            f"Catalog not found at {catalog_csv}. Run scripts/prepare_catalog.py first."
        )
    return pd.read_csv(catalog_csv)


def load_polyvore_outfits(polyvore_dir: Path, split: str = "train") -> list[dict]:
    path = polyvore_dir / f"{split}_no_dup.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing Polyvore split file: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def category_aware_pairs(catalog: pd.DataFrame, max_pairs: int = 50000, seed: int = 42) -> pd.DataFrame:
    """Create practical compatibility pairs from real product metadata.

    This is a fallback when Polyvore item images are unavailable. It uses real catalog
    metadata and conservative fashion constraints: different complementary article
    types, same gender/usage, and non-identical colors are positive; same article type
    duplicates or mismatched usage are negative.
    """
    rng = random.Random(seed)
    catalog = catalog.dropna(subset=["article_type", "gender", "usage"]).reset_index(drop=True)
    indices = list(catalog.index)
    pairs = []

    complements = {
        "Shirts": {"Jeans", "Trousers", "Shorts", "Skirts"},
        "Tshirts": {"Jeans", "Trousers", "Shorts", "Skirts"},
        "Tops": {"Jeans", "Trousers", "Shorts", "Skirts"},
        "Kurtas": {"Leggings", "Churidar", "Salwar"},
        "Jeans": {"Shirts", "Tshirts", "Tops"},
        "Trousers": {"Shirts", "Tshirts", "Tops"},
        "Shoes": {"Jeans", "Trousers", "Dresses", "Skirts"},
        "Dresses": {"Heels", "Flats", "Shoes"},
    }

    attempts = 0
    while len(pairs) < max_pairs and attempts < max_pairs * 20:
        attempts += 1
        a, b = rng.sample(indices, 2)
        left = catalog.loc[a]
        right = catalog.loc[b]
        same_context = left["gender"] == right["gender"] and left["usage"] == right["usage"]
        left_type = str(left["article_type"])
        right_type = str(right["article_type"])
        complementary = right_type in complements.get(left_type, set()) or left_type in complements.get(right_type, set())
        same_duplicate = left_type == right_type
        label = int(same_context and complementary and not same_duplicate)
        if not label and rng.random() > 0.35:
            continue
        pairs.append({"left_idx": a, "right_idx": b, "label": label})

    return pd.DataFrame(pairs)
