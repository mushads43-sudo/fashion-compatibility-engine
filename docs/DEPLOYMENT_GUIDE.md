# Deployment Guide

This project can be deployed as a Streamlit web app.

The easiest recommended deployment options are:

1. Hugging Face Spaces
2. Streamlit Community Cloud

## Why a Deployment Bundle Is Needed

The full raw Kaggle dataset is large:

```text
data/raw/fashion-product-images/ -> about 1.2 GB
```

That is too large for a simple free deployment.

The trained processed files are much smaller:

```text
data/processed/ -> about 28 MB
artifacts/ -> about 8 MB
```

The deployment bundle uses only the images that match the trained embeddings.

## Step 1: Create Deployment Bundle

Run:

```bash
cd "/Users/muskaansheth/Documents/New project/fashion-compatibility-engine"
source .venv/bin/activate
export PYTHONPATH=$PWD/src
python scripts/export_deploy_bundle.py
```

This creates:

```text
deploy_data/
  catalog.csv
  embeddings.npy
  search_index.joblib
  compatibility_model.joblib
  compatibility_metrics.json
  images/
```

## Step 2: Test Deployment Entry Point Locally

Run:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

If this works locally, the same entrypoint can be deployed.

## Option A: Deploy on Hugging Face Spaces

Hugging Face Spaces is recommended for ML demos.

### Steps

1. Create a Hugging Face account.
2. Go to:

```text
https://huggingface.co/spaces
```

3. Click **Create new Space**.
4. Select:

```text
SDK: Streamlit
Visibility: Public or Private
```

5. Push/upload these project files:

```text
app.py
app/
src/
deploy_data/
requirements.txt
.streamlit/
```

6. Hugging Face will install dependencies and run:

```bash
streamlit run app.py
```

## Option B: Deploy on Streamlit Community Cloud

### Steps

1. Push the project to GitHub.
2. Make sure these are included in the repo:

```text
app.py
app/
src/
deploy_data/
requirements.txt
.streamlit/
```

3. Go to:

```text
https://share.streamlit.io/
```

4. Connect your GitHub repository.
5. Set the main file path as:

```text
app.py
```

6. Deploy.

## Important GitHub Note

The project `.gitignore` ignores the full raw dataset and normal training artifacts.

For deployment, commit only:

```text
deploy_data/
```

Do not commit:

```text
data/raw/
data/processed/
artifacts/
.venv/
```

## If GitHub Rejects Large Files

If any file is larger than GitHub's normal file size limit, use one of these options:

1. Reduce the training limit and recreate artifacts:

```bash
python scripts/build_embeddings.py --limit 500 --batch-size 8
python scripts/build_index.py --pca-components 128 --clusters 16
python scripts/train_compatibility.py --max-pairs 10000
python scripts/export_deploy_bundle.py
```

2. Use Git LFS for large files.
3. Use Hugging Face Spaces and upload files directly through the web UI.

## Deployment Command Summary

```bash
cd "/Users/muskaansheth/Documents/New project/fashion-compatibility-engine"
source .venv/bin/activate
export PYTHONPATH=$PWD/src
python scripts/export_deploy_bundle.py
streamlit run app.py
```

## What to Tell Your Sir

The deployed application uses a lightweight production-style bundle instead of the complete raw dataset. This is common in real ML deployment because raw training data is large, while inference only needs trained artifacts and the product catalog required for display.
