# Project Report

## Abstract

This project implements an end-to-end fashion intelligence system for visual product similarity and outfit compatibility prediction. Given uploaded clothing images, the system extracts visual embeddings, retrieves similar products, groups catalog items into style clusters, and predicts whether two items aesthetically work together.

## Objective

The objective is to build a real-world machine learning project that solves two practical fashion e-commerce tasks:

1. Visual similarity search.
2. Outfit compatibility scoring.

Unlike collaborative filtering, this system does not depend on user purchase history. It uses the visual appearance of products.

## Dataset

The primary implementation uses Kaggle Fashion Product Images because it provides product photos and useful metadata. Polyvore Outfit Dataset is included as the real compatibility-label reference. DeepFashion is documented as an academic retrieval benchmark.

## Methodology

### Image Embeddings

A pretrained ResNet50 model is used as a feature extractor. The final classification layer is removed, producing a 2048-dimensional embedding for each product image.

### Embedding Compression

PCA compresses embeddings to a lower-dimensional representation. This reduces storage and speeds up retrieval while preserving the most important visual variance.

### Style Clustering

KMeans groups products into style clusters. These clusters are useful for explaining search results and showing that the system has learned visual product groups.

### Similarity Search

Nearest-neighbor search with cosine distance returns the most visually similar products for an uploaded image.

### Compatibility Prediction

The compatibility classifier receives pair features generated from two item embeddings:

- cosine similarity,
- absolute difference,
- element-wise interaction.

It outputs a probability score between 0 and 1.

## Evaluation

The training script reports:

- accuracy,
- ROC-AUC,
- train pair count,
- test pair count.

For demos, visual quality is evaluated by checking whether retrieved items share product type, color, texture, and style.

## Deployment

The project contains:

- FastAPI service for backend inference,
- Streamlit app for a simple upload UI,
- Dockerfile for container deployment.

## Conclusion

The project demonstrates a complete machine learning workflow: real datasets, feature extraction, retrieval, classification, API deployment, UI demo, documentation, and testing.
