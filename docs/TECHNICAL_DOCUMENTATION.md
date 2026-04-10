# Technical Documentation

## Project Overview

This project is an end-to-end **Fashion Visual Similarity + Outfit Compatibility Engine**.

It performs two main tasks:

1. Given one clothing image, it finds visually similar products.
2. Given two fashion items, it predicts how well they match as an outfit.

The core machine learning flow is:

```text
Fashion image
  -> CNN embedding
  -> compressed vector
  -> similarity search / clustering / compatibility prediction
```

The goal is to build a real-world fashion AI system that goes beyond traditional recommender systems. Instead of relying only on user purchase history, this project uses visual product understanding.

## Repository Structure

```text
fashion-compatibility-engine/
  api/
    main.py
  app/
    streamlit_app.py
  artifacts/
    compatibility_metrics.json
    compatibility_model.joblib
  configs/
    default.yaml
  data/
    raw/
      fashion-product-images/
        styles.csv
        images/
    processed/
      catalog.csv
      embeddings.npy
      search_index.joblib
  docs/
    DATASETS.md
    PPT_OUTLINE.md
    PROJECT_REPORT.md
    TECHNICAL_DOCUMENTATION.md
    fashion_compatibility_engine.pptx
  scripts/
    build_embeddings.py
    build_index.py
    download_polyvore_metadata.py
    find_top_outfits.py
    make_ppt.py
    prepare_catalog.py
    run_pipeline.py
    train_compatibility.py
  src/
    fashion_engine/
      __init__.py
      compatibility.py
      config.py
      data.py
      embeddings.py
      search.py
  tests/
    test_features.py
  .env.example
  .gitignore
  Dockerfile
  pyproject.toml
  README.md
  requirements.txt
```

## Main Project Files

### README.md

`README.md` is the main project guide.

It explains:

- what the project does,
- which datasets are used,
- how to install dependencies,
- how to train the system,
- how to run the Streamlit app,
- how to run the FastAPI backend,
- how to deploy the project.

This is the first file a recruiter, evaluator, or GitHub visitor should read.

### requirements.txt

`requirements.txt` lists all Python libraries required by the project.

Important libraries include:

```text
torch
torchvision
fastapi
streamlit
pandas
numpy
scikit-learn
pillow
kaggle
python-pptx
pytest
```

These libraries are used for:

- computer vision,
- image preprocessing,
- model training,
- similarity search,
- web UI,
- API deployment,
- PPT generation,
- testing.

### pyproject.toml

`pyproject.toml` contains basic Python project settings.

It also tells `pytest` where the source code is located:

```toml
pythonpath = ["src"]
```

This helps Python import modules from:

```text
src/fashion_engine
```

### Dockerfile

`Dockerfile` is used for deployment.

It:

- creates a Python container,
- installs project dependencies,
- copies the project files,
- exposes port `8000`,
- runs the FastAPI app with Uvicorn.

The deployed API command is:

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### .gitignore

`.gitignore` prevents large or generated files from being pushed to GitHub.

It ignores files and folders such as:

```text
.venv/
data/raw/
data/processed/
artifacts/
__pycache__/
*.npy
*.joblib
*.pt
```

This is important because datasets, embeddings, and trained models can be large. GitHub should contain the code and documentation, not heavy generated artifacts.

### .env.example

`.env.example` shows example environment variables for configurable paths.

Example variables:

```text
FASHION_CATALOG_CSV
FASHION_EMBEDDINGS
FASHION_INDEX
FASHION_COMPAT_MODEL
```

This is useful if the user wants to store processed files or model artifacts in a different location.

### .streamlit/config.toml

`.streamlit/config.toml` configures Streamlit.

It contains:

```toml
[server]
fileWatcherType = "none"
```

This disables Streamlit's file watcher. It was added because Streamlit can sometimes show a PyTorch warning like:

```text
Examining the path of torch.classes raised...
```

The project can still run without this file, but the config makes the Streamlit experience cleaner.

## Core Source Code

### src/fashion_engine/config.py

This file manages important project paths.

It defines paths such as:

```text
data/raw/
data/processed/catalog.csv
data/processed/embeddings.npy
data/processed/search_index.joblib
artifacts/compatibility_model.joblib
```

Instead of hardcoding paths in every script, the project uses this file to keep path management consistent.

Important function:

```python
get_paths()
```

This returns a structured object containing all major file paths used across the project.

### src/fashion_engine/data.py

This file handles dataset loading, cleaning, and compatibility pair generation.

Main function:

```python
build_catalog_from_fashion_products()
```

This reads the Kaggle Fashion Product Images dataset:

```text
styles.csv
images/
```

It creates a cleaned catalog containing:

```text
item_id
image_path
gender
master_category
sub_category
article_type
base_colour
season
usage
product_name
```

The cleaned catalog is saved as:

```text
data/processed/catalog.csv
```

Another important function:

```python
category_aware_pairs()
```

This creates compatibility training pairs from real product metadata.

Example positive pairs:

```text
shirt + jeans
top + skirt
track pants + sports shoes
formal trousers + formal shoes
```

Example weaker or negative pairs:

```text
shirt + shirt
sports item + formal item
same product type duplicates
```

This metadata-based pair generation is a practical fallback because the original Polyvore image URLs are mostly unavailable.

### src/fashion_engine/embeddings.py

This file creates image embeddings.

It uses:

```python
torchvision.models.resnet50
```

ResNet50 is a pretrained convolutional neural network. Normally, it predicts image labels. In this project, the final classification layer is removed:

```python
model.fc = nn.Identity()
```

Because of this, ResNet50 outputs a **2048-dimensional embedding vector** instead of a class label.

Important functions:

```python
embed_images()
```

Used during training. It converts all catalog images into embeddings.

```python
embed_single_image()
```

Used during app/API inference. It converts one uploaded image into an embedding.

```python
l2_normalize()
```

Normalizes embeddings so similarity comparison works better.

In simple form:

```text
Image -> ResNet50 -> 2048-dimensional vector
```

### src/fashion_engine/search.py

This file handles:

- visual similarity search,
- PCA compression,
- KMeans clustering,
- nearest-neighbor indexing.

Main function:

```python
train_search_index()
```

This function performs three major steps.

First, it applies PCA:

```text
2048 dimensions -> 128 or 256 dimensions
```

This makes the search faster and reduces storage.

Second, it applies KMeans clustering:

```python
clusters = KMeans(...)
clusters.fit(compressed)
```

KMeans groups similar products into style clusters.

Example clusters could represent:

```text
cluster 0 -> sports shoes
cluster 1 -> casual shirts
cluster 2 -> blue jeans
cluster 3 -> dresses
```

Third, it trains a nearest-neighbor search model:

```python
NearestNeighbors(metric="cosine")
```

This allows the system to find products whose embeddings are closest to the uploaded image.

Main inference function:

```python
search_similar()
```

This takes an uploaded image embedding and returns visually similar products.

### src/fashion_engine/compatibility.py

This file handles outfit compatibility scoring.

It receives two item embeddings and creates pair features.

Important function:

```python
pair_features(left, right)
```

The pair features include:

```text
cosine similarity
absolute difference between embeddings
element-wise product of embeddings
```

These features help the model understand:

- how visually close two items are,
- how they differ,
- how their visual features interact.

The compatibility model is:

```python
HistGradientBoostingClassifier
```

It predicts:

```text
P(compatible | item A, item B)
```

If the model outputs:

```text
0.744
```

the app shows:

```text
74.4% aesthetic compatibility
```

Important functions:

```python
train_compatibility_model()
load_compatibility_model()
compatibility_score()
```

### src/fashion_engine/__init__.py

This marks `fashion_engine` as a Python package.

It allows imports like:

```python
from fashion_engine.embeddings import embed_images
```

## Training and Pipeline Scripts

### scripts/prepare_catalog.py

This is the first script in the pipeline.

Command:

```bash
python scripts/prepare_catalog.py
```

It reads:

```text
data/raw/fashion-product-images/styles.csv
data/raw/fashion-product-images/images/
```

It creates:

```text
data/processed/catalog.csv
```

This cleaned catalog links each image with its product metadata.

### scripts/build_embeddings.py

This script creates image embeddings.

Command:

```bash
python scripts/build_embeddings.py --limit 500 --batch-size 8
```

It:

1. Loads `catalog.csv`.
2. Reads product images.
3. Passes each image through ResNet50.
4. Saves the embedding matrix.

Output:

```text
data/processed/embeddings.npy
```

This is one of the most important generated files in the project.

### scripts/build_index.py

This script builds the search and clustering artifacts.

Command:

```bash
python scripts/build_index.py --pca-components 128 --clusters 16
```

It loads:

```text
data/processed/embeddings.npy
```

Then builds:

```text
PCA model
KMeans clusters
Nearest-neighbor search model
```

Output:

```text
data/processed/search_index.joblib
```

The app and API use this file for visual search.

### scripts/train_compatibility.py

This script trains the outfit compatibility model.

Command:

```bash
python scripts/train_compatibility.py --max-pairs 10000
```

It:

1. Loads the catalog.
2. Loads image embeddings.
3. Creates category-aware fashion pairs.
4. Trains a compatibility classifier.
5. Saves the model and metrics.

Outputs:

```text
artifacts/compatibility_model.joblib
artifacts/compatibility_metrics.json
```

### scripts/run_pipeline.py

This runs the complete training pipeline automatically.

Command:

```bash
python scripts/run_pipeline.py
```

It runs:

```text
prepare catalog
build embeddings
build search index
train compatibility model
```

This is useful when rebuilding the project from scratch.

### scripts/find_top_outfits.py

This script finds high-scoring outfit combinations from the trained model.

Command:

```bash
python scripts/find_top_outfits.py --top-k 20
```

It checks combinations such as:

```text
tops + bottoms
tops + shoes
bottoms + shoes
dresses + shoes
```

Then it prints the best matching image filenames and compatibility scores.

This is useful for:

- Streamlit demos,
- PPT screenshots,
- project explanation,
- testing whether the compatibility model is working.

### scripts/download_polyvore_metadata.py

This script downloads Polyvore metadata.

Polyvore is a real outfit dataset, but the original Polyvore image URLs are mostly unavailable. This script is included for advanced dataset reference and future extension.

### scripts/make_ppt.py

This script generates a PowerPoint presentation.

Command:

```bash
python scripts/make_ppt.py
```

Output:

```text
docs/fashion_compatibility_engine.pptx
```

## App and API Files

### app/streamlit_app.py

This is the web demo UI.

Command:

```bash
streamlit run app/streamlit_app.py
```

It has two main tabs:

```text
Find similar products
Score outfit pair
```

In the **Find similar products** tab:

1. The user uploads one clothing image.
2. The app embeds the image using ResNet50.
3. The app searches for nearest neighbors.
4. The app displays similar products.
5. The app shows similarity percentage and style cluster.

In the **Score outfit pair** tab:

1. The user uploads two fashion item images.
2. The app embeds both images.
3. The app creates pair features.
4. The app runs the compatibility model.
5. The app displays an aesthetic compatibility percentage.

### api/main.py

This is the FastAPI backend.

Command:

```bash
uvicorn api.main:app --reload
```

API documentation opens at:

```text
http://127.0.0.1:8000/docs
```

Endpoints:

```text
GET /health
POST /similar
POST /compatibility
```

`/similar` accepts one uploaded image and returns visually similar products.

`/compatibility` accepts two uploaded images and returns a compatibility score.

## Data Files

### data/raw/fashion-product-images/styles.csv

This is the raw Kaggle metadata file.

It contains columns such as:

```text
id
gender
masterCategory
subCategory
articleType
baseColour
season
usage
productDisplayName
```

### data/raw/fashion-product-images/images/

This folder contains the actual product images.

Example image files:

```text
17240.jpg
54924.jpg
49653.jpg
51499.jpg
```

### data/processed/catalog.csv

This is the cleaned catalog created by `prepare_catalog.py`.

It connects image paths with metadata.

### data/processed/embeddings.npy

This stores all image embeddings.

Shape:

```text
number_of_images x 2048
```

Each row is the ResNet50 embedding for one product image.

### data/processed/search_index.joblib

This stores the trained search artifacts:

```text
PCA
NearestNeighbors
KMeans
compressed embeddings
```

The app loads this file to find similar products quickly.

### artifacts/compatibility_model.joblib

This is the trained outfit compatibility model.

The Streamlit app and FastAPI backend use it to score two uploaded images.

### artifacts/compatibility_metrics.json

This stores evaluation metrics from training.

Example metrics:

```text
accuracy
roc_auc
train_pairs
test_pairs
```

## Documentation Files

### docs/DATASETS.md

This explains the datasets used in the project:

```text
Kaggle Fashion Product Images
Polyvore Outfit Dataset
DeepFashion
```

It also explains which dataset is easiest to use and which one is more academic.

### docs/PPT_OUTLINE.md

This provides slide-by-slide PPT content.

It includes:

```text
problem
solution
datasets
architecture
ML concepts
deployment
business impact
future scope
```

### docs/PROJECT_REPORT.md

This is a written project report that can be used for college submission, GitHub documentation, or viva preparation.

### docs/fashion_compatibility_engine.pptx

This is the generated PowerPoint file.

It is created by:

```bash
python scripts/make_ppt.py
```

## Tests

### tests/test_features.py

This contains small tests for important utility functions.

It tests:

```python
test_l2_normalize_rows()
test_pair_features_shape()
```

These check that:

- embedding normalization works correctly,
- compatibility pair features have the expected shape.

Run tests with:

```bash
pytest
```

## Generated and Ignored Files

The project may also contain:

```text
.venv/
__pycache__/
.DS_Store
```

These are not part of the main project logic.

`.venv` is the Python virtual environment.

`__pycache__` contains Python cache files.

`.DS_Store` is created automatically by macOS.

These files should not be explained in the main project presentation.

## Machine Learning Concepts

### 1. CNN Image Embeddings

The project uses ResNet50, a convolutional neural network.

Normally, ResNet50 performs classification:

```text
image -> ResNet50 -> label
```

This project removes the final classification layer, so the model becomes a feature extractor:

```text
image -> ResNet50 -> embedding vector
```

The embedding is a numerical summary of the image.

For example, a fashion image becomes:

```text
[0.12, -0.04, 0.88, ..., 0.31]
```

This vector captures visual information such as:

- shape,
- color,
- texture,
- sleeves,
- pattern,
- object type,
- overall style.

This allows the project to compare images mathematically.

### 2. L2 Normalization

After embeddings are created, they are normalized.

Normalization makes every vector have length 1.

This is useful because the model compares the direction of vectors rather than their raw magnitude.

It improves cosine similarity comparison.

### 3. Visual Similarity Search

Similar products are found using vector similarity.

Flow:

```text
uploaded image
  -> ResNet50 embedding
  -> PCA transform
  -> compare with catalog vectors
  -> return closest products
```

The project uses cosine distance.

If two images have similar embeddings, their cosine similarity is high.

Example:

```text
blue checked shirt query
  -> similar blue shirts
  -> checked shirts
  -> casual shirts
```

This is visual search, not keyword search. Even if product names are different, visually similar items can still be found.

### 4. PCA Compression

ResNet50 embeddings have 2048 dimensions.

PCA reduces this:

```text
2048 dimensions -> 128 or 256 dimensions
```

PCA is used because it:

- speeds up search,
- reduces storage,
- removes noise,
- keeps the most important visual variation.

PCA is trained in:

```text
src/fashion_engine/search.py
```

It is run by:

```text
scripts/build_index.py
```

### 5. KMeans Clustering

KMeans groups similar fashion items into clusters.

Example:

```text
Cluster 0: sports shoes
Cluster 1: casual shirts
Cluster 2: jeans
Cluster 3: women's tops
Cluster 4: dresses
```

The model is not given these names. It discovers groups automatically using visual embeddings.

This is unsupervised learning.

In the Streamlit app, each result can show a cluster number:

```text
cluster 4
```

This means the product belongs to a learned visual style group.

Clustering shows that the project is learning structure in the fashion catalog, not only comparing one image at a time.

### 6. Outfit Compatibility Prediction

Compatibility is different from similarity.

Two compatible items may not look identical.

Example:

```text
white shirt + blue jeans = good outfit
white shirt + another white shirt = not a useful outfit pair
```

The project takes two image embeddings:

```text
embedding A
embedding B
```

Then creates pair features:

```text
cosine similarity
absolute difference
element-wise product
```

These features tell the model:

- how visually close the items are,
- where they are different,
- how their visual features interact.

The classifier then predicts:

```text
compatible or not compatible
```

The output is a probability:

```text
0.744 -> 74.4% compatible
```

This is shown in Streamlit as:

```text
Aesthetic compatibility: 74.4%
```

## Why Compatibility Scores Can Be Low

The current model is conservative.

The model was trained using real product images and metadata-based compatibility rules. It has not yet been fully trained on human-curated Polyvore outfit images because the original Polyvore image URLs are mostly unavailable.

For the current version:

```text
50-75% = good match
30-50% = possible match
below 30% = weak match
```

For demos, use top combinations generated by:

```bash
python scripts/find_top_outfits.py --top-k 20
```

## Complete Working Flow

### Training Flow

```text
1. Download Kaggle dataset
2. Prepare catalog
3. Generate ResNet50 embeddings
4. Build PCA + KMeans + nearest-neighbor index
5. Train compatibility classifier
6. Save artifacts
```

### App Flow

```text
1. User uploads image/images
2. App loads trained artifacts
3. Image is converted into embedding
4. Similarity search or compatibility model runs
5. Result is displayed
```

## Why This Project Is Advanced

This project is advanced because it combines:

- computer vision,
- image embeddings,
- unsupervised clustering,
- dimensionality reduction,
- similarity search,
- pairwise classification,
- real datasets,
- API deployment,
- web UI,
- Docker,
- PPT/report generation.

It is more professional than a basic classifier because it behaves like a real fashion AI system used in e-commerce.

## Strong PPT Line

```text
This project goes beyond recommendations by learning visual style representations and predicting outfit compatibility directly from product images.
```
