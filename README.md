# Fashion Visual Similarity + Outfit Compatibility Engine

Recruiter line:

> We are teaching machines fashion sense, not just recommendations.

This project builds an end-to-end fashion AI system that:

- finds visually similar fashion products from image embeddings,
- groups products into style clusters,
- predicts whether two clothing items are aesthetically compatible,
- exposes the model through FastAPI,
- provides a Streamlit demo for uploads,
- includes deployment files and PPT-ready documentation.

The implementation is intentionally professional but not overcomplicated: ResNet50 embeddings, PCA compression, KMeans style grouping, nearest-neighbor retrieval, and a pairwise compatibility classifier.

## Real Datasets Used

Use these real-world datasets:

| Purpose | Dataset | Direct link | Why it is used |
|---|---|---|---|
| Product image catalog for visual search | Fashion Product Images, Kaggle | https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset | Product images plus metadata such as category, color, season, usage |
| Smaller version for quick local demo | Fashion Product Images Small, Kaggle | https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small | Easier download for laptops |
| Real outfit compatibility labels | Polyvore Outfit Dataset | https://github.com/xthan/polyvore-dataset | Contains outfit splits and fashion compatibility labels |
| Academic retrieval benchmark | DeepFashion | https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html | Large-scale fashion retrieval/attribute benchmark, but access has research agreement constraints |

Important: DeepFashion is real and excellent, but it is not the easiest dataset for a student demo because some downloads require a signed agreement and passwords. This repo is designed to work smoothly with Kaggle Fashion Product Images first, then optionally extend to Polyvore/DeepFashion.

## GitHub Structure

```text
fashion-compatibility-engine/
  api/
    main.py                       # FastAPI backend
  app/
    streamlit_app.py              # Upload demo UI
  artifacts/
    .gitkeep                      # trained models live here, ignored by git
  configs/
    default.yaml
  data/
    raw/                          # downloaded datasets, ignored by git
    processed/                    # catalog, embeddings, search index, ignored by git
  docs/
    DATASETS.md
    PPT_OUTLINE.md
    PROJECT_REPORT.md
  scripts/
    download_polyvore_metadata.py
    prepare_catalog.py
    build_embeddings.py
    build_index.py
    train_compatibility.py
    run_pipeline.py
  src/fashion_engine/
    config.py
    data.py
    embeddings.py
    search.py
    compatibility.py
  tests/
    test_features.py
  Dockerfile
  pyproject.toml
  requirements.txt
```

## Setup in VS Code

```bash
cd fashion-compatibility-engine
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
export PYTHONPATH=$PWD/src
```

If PyTorch installation fails, your Python version is usually the reason. This repo allows `pip` to choose a compatible `torch` and `torchvision` version. Python 3.11 or 3.12 is the safest choice for ML projects; Python 3.13 can work only when matching PyTorch wheels are available for your machine.

On Windows PowerShell:

```powershell
cd fashion-compatibility-engine
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
$env:PYTHONPATH="$PWD\src"
```

## Download Data

Recommended beginner path:

1. Create a Kaggle account.
2. Go to Account settings and create a Kaggle API token.
3. Put `kaggle.json` in `~/.kaggle/kaggle.json`.
4. Run:

```bash
mkdir -p data/raw/fashion-product-images
kaggle datasets download -d paramaggarwal/fashion-product-images-small -p data/raw/fashion-product-images --unzip
```

If you want the larger dataset, use:

```bash
kaggle datasets download -d paramaggarwal/fashion-product-images-dataset -p data/raw/fashion-product-images --unzip
```

Optional Polyvore metadata:

```bash
python scripts/download_polyvore_metadata.py
```

## Train the System

For a fast laptop demo, start with a small subset:

```bash
python scripts/prepare_catalog.py
python scripts/build_embeddings.py --limit 2000 --batch-size 16
python scripts/build_index.py --pca-components 128 --clusters 16
python scripts/train_compatibility.py --max-pairs 20000
```

For the full dataset:

```bash
python scripts/run_pipeline.py
```

Outputs:

```text
data/processed/catalog.csv
data/processed/embeddings.npy
data/processed/search_index.joblib
artifacts/compatibility_model.joblib
artifacts/compatibility_metrics.json
```

## Run the Demo

Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

FastAPI backend:

```bash
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Docker Deployment

Build locally:

```bash
docker build -t fashion-compatibility-engine .
docker run -p 8000:8000 fashion-compatibility-engine
```

For Render/Railway deployment, upload the repo and set the start command:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

You must include trained artifacts in the deployment environment or attach persistent storage.

## Create the PPT

After installing requirements:

```bash
python scripts/make_ppt.py
```

This writes:

```text
docs/fashion_compatibility_engine.pptx
```

## Model Pipeline

```text
Image Dataset
  -> catalog cleaning
  -> ResNet50 image embeddings
  -> PCA compression
  -> KMeans style clusters
  -> nearest-neighbor visual similarity
  -> pair feature engineering
  -> compatibility classifier
  -> FastAPI + Streamlit deployment
```

## Why This Is Recruiter-Level

- It solves a real business problem in fashion e-commerce.
- It uses real image data rather than toy Fashion-MNIST.
- It separates training scripts, reusable source code, API, UI, docs, and tests.
- It includes both computer vision retrieval and pairwise outfit scoring.
- It is deployable and demo-friendly.

## Next Improvements

- Replace ResNet50 with CLIP or FashionCLIP embeddings.
- Train compatibility directly on Polyvore item images if you download the image archive.
- Add triplet-loss fine-tuning for better retrieval.
- Add MLflow or Weights & Biases experiment tracking.
- Add vector DB support with FAISS/Qdrant for larger production catalogs.
