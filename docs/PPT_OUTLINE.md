# PPT Outline

## Slide 1: Title

Fashion Visual Similarity + Outfit Compatibility Engine

Killer line:

> We are teaching machines fashion sense, not just recommendations.

## Slide 2: Problem

Fashion e-commerce search is usually keyword-based or purchase-history-based.

Problem:

- users cannot describe style visually,
- recommendation systems fail for new products,
- matching outfits requires aesthetic understanding,
- retailers need better discovery and styling intelligence.

## Slide 3: Proposed Solution

Upload a clothing image and the system:

- finds visually similar products,
- groups products into style clusters,
- predicts outfit compatibility score,
- returns matching items and a percentage score.

Example:

```text
White linen shirt + beige chinos = 92% compatible
Running shoes + silk evening dress = 18% compatible
```

## Slide 4: Datasets

- Kaggle Fashion Product Images: product catalog images and metadata.
- Polyvore Outfit Dataset: real outfit compatibility labels.
- DeepFashion: large academic benchmark for retrieval and attributes.

Why real-world:

- real product photos,
- noisy metadata,
- many categories,
- deployable on uploaded images.

## Slide 5: System Architecture

```text
Image upload
  -> ResNet50 feature extractor
  -> normalized embedding
  -> PCA compression
  -> KMeans style cluster
  -> nearest neighbor search
  -> compatibility model
  -> API/UI response
```

## Slide 6: Machine Learning Concepts

- CNN embeddings using ResNet50.
- PCA for embedding compression.
- KMeans for unsupervised style grouping.
- Metric similarity using cosine distance.
- Pairwise classification for compatibility score.

## Slide 7: Visual Similarity

Image embeddings convert products into vectors.

Similar products have close vectors:

```text
query image -> top K nearest products
```

This works even when product names are different.

## Slide 8: Outfit Compatibility

Two item embeddings are transformed into pair features:

```text
cosine similarity
absolute embedding difference
embedding interaction/product
```

The classifier predicts:

```text
P(compatible | item A, item B)
```

## Slide 9: Demo Screens

Show:

- uploaded shirt,
- similar shirts/tops,
- uploaded shirt + pants,
- compatibility score,
- good outfit vs bad outfit examples.

## Slide 10: Deployment

Deployment stack:

- FastAPI backend,
- Streamlit demo,
- Docker container,
- Render/Railway/Hugging Face Spaces compatible.

## Slide 11: Business Impact

Use cases:

- visual product search,
- complete-the-look styling,
- outfit scoring,
- catalog deduplication,
- personalized stylist assistant,
- cold-start recommendation for new products.

## Slide 12: Future Scope

- FashionCLIP embeddings,
- triplet-loss fine-tuning,
- direct Polyvore image compatibility training,
- vector database at scale,
- body type/occasion-aware styling,
- multimodal search using text + image.

## Slide 13: Closing

This project goes beyond “people also bought.”

It learns visual style and predicts whether fashion items aesthetically work together.
