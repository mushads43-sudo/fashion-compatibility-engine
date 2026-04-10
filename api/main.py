from __future__ import annotations

from pathlib import Path
import tempfile

import numpy as np
from fastapi import FastAPI, File, UploadFile

from fashion_engine.compatibility import compatibility_score, load_compatibility_model
from fashion_engine.config import get_paths
from fashion_engine.data import load_catalog
from fashion_engine.embeddings import embed_single_image
from fashion_engine.search import load_search_index, search_similar


app = FastAPI(title="Fashion Compatibility Engine", version="1.0.0")


def state() -> dict:
    paths = get_paths()
    if not hasattr(app.state, "loaded"):
        app.state.paths = paths
        app.state.catalog = load_catalog(paths.catalog_csv)
        app.state.search_index = load_search_index(paths.index_joblib)
        app.state.compatibility = load_compatibility_model(paths.compatibility_model)
        app.state.embeddings = np.load(paths.embeddings_npy)
        app.state.loaded = True
    return app.state.__dict__


async def save_upload(upload: UploadFile) -> Path:
    suffix = Path(upload.filename or "image.jpg").suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await upload.read())
        return Path(tmp.name)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/similar")
async def similar(file: UploadFile = File(...), top_k: int = 8) -> dict:
    s = state()
    path = await save_upload(file)
    query_embedding = embed_single_image(path)
    results = search_similar(query_embedding, s["search_index"], s["catalog"], top_k=top_k)
    return {"results": results}


@app.post("/compatibility")
async def compatibility(left: UploadFile = File(...), right: UploadFile = File(...)) -> dict:
    s = state()
    left_path = await save_upload(left)
    right_path = await save_upload(right)
    left_embedding = embed_single_image(left_path)
    right_embedding = embed_single_image(right_path)
    score = compatibility_score(left_embedding, right_embedding, s["compatibility"])
    return {"compatibility_score": round(score * 100, 2), "label": "compatible" if score >= 0.5 else "not compatible"}
