import numpy as np

from fashion_engine.compatibility import pair_features
from fashion_engine.embeddings import l2_normalize


def test_l2_normalize_rows():
    values = np.array([[3.0, 4.0], [0.0, 0.0]], dtype="float32")
    normalized = l2_normalize(values)
    assert np.isclose(np.linalg.norm(normalized[0]), 1.0)
    assert np.allclose(normalized[1], [0.0, 0.0])


def test_pair_features_shape():
    left = np.ones((2, 4), dtype="float32")
    right = np.zeros((2, 4), dtype="float32")
    features = pair_features(left, right)
    assert features.shape == (2, 9)
