# Dataset Guide

This project intentionally avoids toy datasets. The core data sources are real fashion product and outfit datasets.

## 1. Fashion Product Images

Link: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset

Small version: https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small

Use for:

- product image catalog,
- visual similarity search,
- style clustering,
- deployed upload demo.

Expected local layout:

```text
data/raw/fashion-product-images/
  styles.csv
  images/
    1163.jpg
    1164.jpg
```

Download:

```bash
mkdir -p data/raw/fashion-product-images
kaggle datasets download -d paramaggarwal/fashion-product-images-small -p data/raw/fashion-product-images --unzip
```

Use the full dataset when your laptop can handle more images:

```bash
kaggle datasets download -d paramaggarwal/fashion-product-images-dataset -p data/raw/fashion-product-images --unzip
```

## 2. Polyvore Outfit Dataset

Link: https://github.com/xthan/polyvore-dataset

Raw metadata archive:

```text
https://raw.githubusercontent.com/xthan/polyvore-dataset/master/polyvore.tar.gz
```

Use for:

- real outfit compatibility labels,
- fill-in-the-blank fashion recommendation evaluation,
- research discussion in the PPT.

Download metadata:

```bash
python scripts/download_polyvore_metadata.py
```

Important limitation: the Polyvore README states that the original image URLs are no longer available because Polyvore was acquired. That means the labels are still useful, but image-based training requires an alternate image archive or Kaggle mirror.

## 3. DeepFashion

Link: https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html

Use for:

- academic retrieval benchmark,
- attribute prediction,
- in-shop retrieval,
- consumer-to-shop retrieval.

Important limitation: DeepFashion is available for non-commercial research and some image downloads require an agreement/password. It is excellent for research but less convenient than Kaggle Fashion Product Images for a quick GitHub demo.

## Recommended Dataset Choice

For your GitHub project:

```text
Main demo: Kaggle Fashion Product Images Small
Advanced discussion: Polyvore Outfit Dataset compatibility labels
Research benchmark mention: DeepFashion
```

This gives you a project that actually runs on a normal laptop while still being grounded in real-world fashion datasets.
