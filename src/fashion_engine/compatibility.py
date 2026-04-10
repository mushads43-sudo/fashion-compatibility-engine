from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class CompatibilityArtifacts:
    model: Pipeline
    metrics: dict


def pair_features(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    if left.ndim == 1:
        left = left.reshape(1, -1)
    if right.ndim == 1:
        right = right.reshape(1, -1)
    cosine = np.sum(left * right, axis=1, keepdims=True)
    absolute_diff = np.abs(left - right)
    product = left * right
    return np.hstack([cosine, absolute_diff, product]).astype("float32")


def train_compatibility_model(
    pairs: pd.DataFrame,
    embeddings: np.ndarray,
    output_path: Path,
    random_state: int = 42,
) -> CompatibilityArtifacts:
    if pairs.empty:
        raise ValueError("No compatibility pairs available for training.")

    left = embeddings[pairs["left_idx"].to_numpy()]
    right = embeddings[pairs["right_idx"].to_numpy()]
    x = pair_features(left, right)
    y = pairs["label"].astype(int).to_numpy()

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=random_state, stratify=y
    )
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                HistGradientBoostingClassifier(
                    max_iter=180,
                    learning_rate=0.06,
                    max_leaf_nodes=31,
                    random_state=random_state,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "roc_auc": float(roc_auc_score(y_test, probabilities)) if len(set(y_test)) > 1 else None,
        "train_pairs": int(len(x_train)),
        "test_pairs": int(len(x_test)),
    }
    artifacts = CompatibilityArtifacts(model=model, metrics=metrics)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifacts, output_path)
    return artifacts


def load_compatibility_model(path: Path) -> CompatibilityArtifacts:
    if not path.exists():
        raise FileNotFoundError(
            f"Compatibility model not found at {path}. Run scripts/train_compatibility.py."
        )
    return joblib.load(path)


def compatibility_score(left_embedding: np.ndarray, right_embedding: np.ndarray, artifacts: CompatibilityArtifacts) -> float:
    features = pair_features(left_embedding, right_embedding)
    return float(artifacts.model.predict_proba(features)[0, 1])
