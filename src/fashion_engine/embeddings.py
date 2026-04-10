from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageOps
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
from tqdm import tqdm


class ImagePathDataset(Dataset):
    def __init__(self, image_paths: list[str], transform):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        path = self.image_paths[idx]
        image = Image.open(path).convert("RGB")
        image = ImageOps.exif_transpose(image)
        return self.transform(image)


def build_resnet50(device: str | None = None) -> tuple[nn.Module, transforms.Compose, str]:
    resolved_device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    weights = models.ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)
    model.fc = nn.Identity()
    model.eval().to(resolved_device)
    return model, weights.transforms(), resolved_device


@torch.inference_mode()
def embed_images(
    image_paths: list[str],
    batch_size: int = 32,
    num_workers: int = 0,
    device: str | None = None,
) -> np.ndarray:
    model, transform, resolved_device = build_resnet50(device)
    dataset = ImagePathDataset(image_paths, transform)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    vectors = []
    for batch in tqdm(loader, desc="Embedding images"):
        batch = batch.to(resolved_device)
        emb = model(batch).detach().cpu().numpy().astype("float32")
        vectors.append(emb)
    if not vectors:
        raise ValueError("No images were embedded. Check your catalog image paths.")
    embeddings = np.vstack(vectors)
    return l2_normalize(embeddings)


@torch.inference_mode()
def embed_single_image(image_path: Path | str, device: str | None = None) -> np.ndarray:
    model, transform, resolved_device = build_resnet50(device)
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.exif_transpose(image)
    tensor = transform(image).unsqueeze(0).to(resolved_device)
    embedding = model(tensor).detach().cpu().numpy().astype("float32")
    return l2_normalize(embedding)[0]


def l2_normalize(values: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    norms = np.linalg.norm(values, axis=1, keepdims=True)
    return values / np.maximum(norms, eps)
