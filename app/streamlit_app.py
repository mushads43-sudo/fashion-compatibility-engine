from __future__ import annotations

from pathlib import Path
import tempfile

import numpy as np
import pandas as pd
import streamlit as st

from fashion_engine.compatibility import compatibility_score, load_compatibility_model
from fashion_engine.config import get_paths
from fashion_engine.data import load_catalog
from fashion_engine.embeddings import embed_single_image
from fashion_engine.search import load_search_index, search_similar


st.set_page_config(page_title="Fashion Compatibility Engine", layout="wide")


@st.cache_resource
def load_assets():
    paths = get_paths()
    return {
        "paths": paths,
        "catalog": load_catalog(paths.catalog_csv),
        "index": load_search_index(paths.index_joblib),
        "compat": load_compatibility_model(paths.compatibility_model),
    }


def persist_upload(uploaded_file) -> Path:
    suffix = Path(uploaded_file.name).suffix or ".jpg"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        return Path(tmp.name)


st.title("Fashion Visual Similarity + Outfit Compatibility")
st.caption("Upload clothing images to find visually similar products and estimate whether two items work together.")

try:
    assets = load_assets()
except Exception as exc:
    st.error(str(exc))
    st.stop()

tab_search, tab_pair = st.tabs(["Find similar products", "Score outfit pair"])

with tab_search:
    query = st.file_uploader("Upload one clothing image", type=["jpg", "jpeg", "png", "webp"])
    top_k = st.slider("Number of matches", 4, 16, 8)
    if query:
        query_path = persist_upload(query)
        query_embedding = embed_single_image(query_path)
        results = search_similar(query_embedding, assets["index"], assets["catalog"], top_k=top_k)
        st.image(str(query_path), caption="Query image", width=220)
        cols = st.columns(4)
        for i, item in enumerate(results):
            with cols[i % 4]:
                st.image(item["image_path"], use_container_width=True)
                st.metric("Similarity", f"{item['similarity'] * 100:.1f}%")
                st.write(item.get("product_name", ""))
                st.caption(f"{item.get('article_type', '')} | {item.get('base_colour', '')} | cluster {item['style_cluster']}")

with tab_pair:
    left_file = st.file_uploader("Upload first item", type=["jpg", "jpeg", "png", "webp"], key="left")
    right_file = st.file_uploader("Upload second item", type=["jpg", "jpeg", "png", "webp"], key="right")
    if left_file and right_file:
        left_path = persist_upload(left_file)
        right_path = persist_upload(right_file)
        left_embedding = embed_single_image(left_path)
        right_embedding = embed_single_image(right_path)
        score = compatibility_score(left_embedding, right_embedding, assets["compat"])
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.image(str(left_path), caption="Item 1", use_container_width=True)
        with col2:
            st.image(str(right_path), caption="Item 2", use_container_width=True)
        with col3:
            st.metric("Aesthetic compatibility", f"{score * 100:.1f}%")
            st.progress(float(score))
            st.write("Compatible" if score >= 0.5 else "Needs a better match")
