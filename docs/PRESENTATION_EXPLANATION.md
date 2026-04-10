# Fashion Visual Similarity and Outfit Compatibility Engine

## 1. Project Title

**Fashion Visual Similarity + Outfit Compatibility Engine**

Project line:

```text
We are teaching machines fashion sense, not just recommendations.
```

## 2. Problem Statement

Fashion e-commerce platforms contain thousands or millions of clothing products. Users often struggle to find products that match their taste because fashion search is usually based on text keywords, filters, or purchase history.

Traditional recommendation systems usually answer questions like:

```text
People who bought this also bought that.
```

However, this does not directly solve visual fashion problems such as:

- Which products look visually similar to this shirt?
- Which pants match this top?
- Does this shoe go well with this dress?
- Can we recommend matching products even for new users or new catalog items?

The main problem this project solves is:

```text
Given clothing images, find visually similar fashion products and predict whether two fashion items are aesthetically compatible.
```

This project focuses on visual understanding instead of only user behavior.

## 3. Motivation

Fashion is highly visual. Two products may have completely different names but may look very similar. Similarly, two items may belong to different categories but still look good together.

For example:

```text
blue checked shirt + navy jeans = good casual outfit
formal trousers + formal shoes = good formal outfit
sports t-shirt + formal shoes = weak outfit match
```

Real fashion companies use visual AI for:

- visual product search,
- complete-the-look recommendation,
- catalog deduplication,
- outfit generation,
- personalized styling,
- e-commerce product discovery.

This project demonstrates a simplified but realistic version of such a system.

## 4. Project Objectives

The objectives of this project are:

1. Build a real-world machine learning system using actual fashion product images.
2. Extract meaningful visual features from clothing images using a CNN.
3. Find visually similar products using embedding similarity.
4. Group products into style clusters using unsupervised learning.
5. Predict compatibility between two fashion items.
6. Build a deployable system with a web UI and API.
7. Prepare documentation, report, and PPT material for presentation.

## 5. What the Project Does

The project has two main features.

### Feature 1: Visual Similarity Search

The user uploads one fashion image.

The system then:

1. Converts the uploaded image into a numerical embedding.
2. Compares it with embeddings of all catalog products.
3. Finds the most visually similar products.
4. Displays similar products with similarity scores.

Example:

```text
Input: blue checked shirt
Output: similar blue shirts, checked shirts, casual shirts
```

### Feature 2: Outfit Compatibility Prediction

The user uploads two fashion item images.

The system then:

1. Converts both images into embeddings.
2. Creates pairwise features from both embeddings.
3. Sends those features to a trained classifier.
4. Outputs an aesthetic compatibility score.

Example:

```text
Input: black polo t-shirt + blue shorts
Output: 74.4% compatible
```

## 6. Datasets Used

This project uses real-world fashion datasets.

### 6.1 Fashion Product Images Dataset

Dataset link:

```text
https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset
```

Small version:

```text
https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small
```

This is the main dataset used in the working project.

It contains:

- fashion product images,
- product IDs,
- gender,
- category,
- subcategory,
- article type,
- base color,
- season,
- usage,
- product display name.

Important files:

```text
styles.csv
images/
```

Example metadata columns:

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

Why this dataset is used:

- It contains real product images.
- It has useful metadata.
- It is easy to download from Kaggle.
- It works well for visual search and compatibility prototype training.
- It is practical for a student laptop demo.

### 6.2 Polyvore Outfit Dataset

Dataset link:

```text
https://github.com/xthan/polyvore-dataset
```

This dataset contains real outfit combinations and compatibility labels.

It is useful for:

- outfit compatibility prediction,
- fill-in-the-blank fashion recommendation,
- research-level fashion AI discussion.

Important limitation:

The original Polyvore image URLs are mostly unavailable because Polyvore was acquired and shut down. Therefore, this project documents Polyvore as an important real dataset, but the working implementation mainly uses Kaggle product images.

### 6.3 DeepFashion Dataset

Dataset link:

```text
https://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html
```

DeepFashion is a large academic fashion dataset.

It is useful for:

- fashion attribute prediction,
- clothing retrieval,
- consumer-to-shop retrieval,
- landmark detection,
- category prediction.

Important limitation:

Some parts of DeepFashion require a research agreement or password. So it is excellent for academic reference, but less convenient for immediate project deployment.

## 7. Dataset Preparation

The raw Kaggle dataset contains:

```text
styles.csv
images/
```

The project prepares a clean catalog from this raw dataset.

The cleaned catalog contains:

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

This catalog is saved as:

```text
data/processed/catalog.csv
```

This step is important because the model needs a clean mapping between:

```text
product metadata <-> image file path
```

## 8. System Architecture

The overall architecture is:

```text
Dataset
  -> catalog preparation
  -> image embedding extraction
  -> PCA compression
  -> KMeans clustering
  -> nearest-neighbor visual search
  -> compatibility model training
  -> Streamlit app and FastAPI backend
```

For visual search:

```text
Uploaded image
  -> ResNet50 embedding
  -> PCA transform
  -> nearest-neighbor search
  -> similar products
```

For compatibility:

```text
Item A image + Item B image
  -> ResNet50 embeddings
  -> pair feature generation
  -> compatibility classifier
  -> compatibility percentage
```

## 9. Machine Learning Concepts Used

### 9.1 Convolutional Neural Network

A Convolutional Neural Network, or CNN, is a deep learning model commonly used for image understanding.

CNNs learn visual patterns such as:

- edges,
- colors,
- textures,
- shapes,
- object parts,
- higher-level object representations.

In this project, a pretrained CNN called ResNet50 is used.

### 9.2 ResNet50

ResNet50 is a deep CNN architecture with 50 layers.

It uses residual connections, which help train deep neural networks more effectively.

Normally, ResNet50 is used for image classification:

```text
image -> ResNet50 -> class label
```

In this project, the final classification layer is removed:

```python
model.fc = nn.Identity()
```

So the model becomes a feature extractor:

```text
image -> ResNet50 -> 2048-dimensional embedding
```

This embedding represents the visual style and appearance of the product.

### 9.3 Image Embeddings

An image embedding is a vector representation of an image.

Instead of storing only pixels, the system stores meaningful visual features.

Example:

```text
shirt image -> [0.12, -0.04, 0.88, ..., 0.31]
```

Images that look similar should have embeddings that are close to each other in vector space.

This is the foundation of visual similarity search.

### 9.4 L2 Normalization

L2 normalization scales each embedding so that its length becomes 1.

This is useful because similarity comparison becomes based on direction instead of magnitude.

After normalization, cosine similarity becomes more reliable.

### 9.5 Cosine Similarity

Cosine similarity measures the angle between two vectors.

If two vectors point in a similar direction, their cosine similarity is high.

In this project:

```text
high cosine similarity = visually similar products
low cosine similarity = visually different products
```

Cosine similarity is used for visual search.

### 9.6 PCA

PCA stands for Principal Component Analysis.

It is a dimensionality reduction technique.

The original ResNet50 embedding has:

```text
2048 dimensions
```

PCA compresses it to:

```text
128 or 256 dimensions
```

Benefits of PCA:

- faster search,
- less memory usage,
- reduced noise,
- easier clustering,
- more efficient deployment.

### 9.7 KMeans Clustering

KMeans is an unsupervised learning algorithm.

It groups similar data points into clusters.

In this project, KMeans groups fashion items based on their visual embeddings.

Possible clusters:

```text
cluster 0 -> sports shoes
cluster 1 -> casual shirts
cluster 2 -> jeans
cluster 3 -> dresses
cluster 4 -> women tops
```

The model is not manually told these categories. It discovers patterns from image embeddings.

This helps show that the model has learned visual style groups.

### 9.8 Nearest Neighbor Search

Nearest neighbor search finds the closest items to a query vector.

In this project:

```text
query image embedding -> nearest catalog embeddings -> similar products
```

The search uses cosine distance.

This allows the app to return top matching products for an uploaded image.

### 9.9 Pairwise Feature Engineering

Compatibility is not exactly the same as similarity.

Two similar items may not form a good outfit.

Example:

```text
shirt + shirt = visually similar but not a useful outfit pair
shirt + jeans = different but compatible
```

So the project creates pairwise features from two item embeddings.

The pair features are:

```text
cosine similarity
absolute difference
element-wise product
```

These features help the model understand the relationship between two fashion items.

### 9.10 Classification

The compatibility task is treated as a classification problem.

The classifier predicts whether two items are compatible or not.

The model used is:

```text
HistGradientBoostingClassifier
```

It outputs a probability:

```text
0.744 = 74.4% compatible
```

This probability is shown as the aesthetic compatibility score.

## 10. How Similar Products Are Found

The similarity search process works like this:

1. A product image is uploaded.
2. The image is resized and preprocessed.
3. ResNet50 converts the image into a 2048-dimensional embedding.
4. The embedding is normalized.
5. PCA compresses the embedding.
6. The compressed embedding is compared with all catalog embeddings.
7. The nearest products are selected using cosine distance.
8. The app displays the most similar products.

Simplified flow:

```text
query image
  -> embedding
  -> compressed embedding
  -> cosine nearest neighbors
  -> top K similar products
```

This is why the system can find visually similar products even if their names or descriptions are different.

## 11. How Outfit Compatibility Is Found

The compatibility process works like this:

1. The user uploads two item images.
2. Each image is converted into a ResNet50 embedding.
3. Pairwise features are created from the two embeddings.
4. The compatibility classifier predicts a probability.
5. The probability is converted into a percentage.

Simplified flow:

```text
item A image -> embedding A
item B image -> embedding B
embedding A + embedding B -> pair features
pair features -> classifier
classifier -> compatibility score
```

Example:

```text
score = 0.744
display = 74.4% compatible
```

## 12. Training Pipeline

The training pipeline has five major steps.

### Step 1: Prepare Catalog

Command:

```bash
python scripts/prepare_catalog.py
```

This creates:

```text
data/processed/catalog.csv
```

### Step 2: Build Image Embeddings

Command:

```bash
python scripts/build_embeddings.py --limit 500 --batch-size 8
```

This creates:

```text
data/processed/embeddings.npy
```

### Step 3: Build Search Index

Command:

```bash
python scripts/build_index.py --pca-components 128 --clusters 16
```

This creates:

```text
data/processed/search_index.joblib
```

### Step 4: Train Compatibility Model

Command:

```bash
python scripts/train_compatibility.py --max-pairs 10000
```

This creates:

```text
artifacts/compatibility_model.joblib
artifacts/compatibility_metrics.json
```

### Step 5: Run Application

Command:

```bash
streamlit run app/streamlit_app.py
```

This opens the user interface.

## 13. Deployment

This project supports two deployment styles.

### Streamlit App

Used for visual demo.

Command:

```bash
streamlit run app/streamlit_app.py
```

### FastAPI Backend

Used for API deployment.

Command:

```bash
uvicorn api.main:app --reload
```

API docs:

```text
http://127.0.0.1:8000/docs
```

### Docker

The `Dockerfile` allows the backend to run inside a container.

This is useful for cloud platforms such as:

- Render,
- Railway,
- AWS,
- Azure,
- Google Cloud.

## 14. Results Interpretation

The compatibility score is shown as a percentage.

Suggested interpretation:

```text
70% and above = strong match
50% to 70% = good match
30% to 50% = possible match
below 30% = weak match
```

Since this is a prototype trained using metadata-based compatibility pairs, the model is conservative. Scores above 50% can still be considered useful for demonstration.

For high-scoring demo examples, use:

```bash
python scripts/find_top_outfits.py --top-k 20
```

## 15. Why This Is Not Just a Basic Recommendation System

A normal recommendation system often depends on:

```text
user clicks
purchase history
ratings
co-purchase behavior
```

This project uses:

```text
image content
visual embeddings
style clusters
pairwise compatibility prediction
```

So it can work even when:

- a product is new,
- there is no user history,
- the user only provides an image,
- products have poor text descriptions.

This makes it more suitable for fashion visual intelligence.

## 16. Advantages

Advantages of this project:

- Uses real-world fashion product images.
- Combines computer vision and machine learning.
- Provides both search and compatibility scoring.
- Has a deployable UI and API.
- Uses a clean GitHub-ready structure.
- Can be extended with more advanced models.
- Demonstrates practical e-commerce use cases.

## 17. Limitations

Current limitations:

- Compatibility model uses metadata-based pair generation.
- Full human-labeled outfit image training is limited because Polyvore image URLs are mostly unavailable.
- ResNet50 is general-purpose, not fashion-specific.
- Compatibility scores are useful for demo but not production-perfect.
- The current version does not include user personalization.

## 18. Future Scope

Future improvements:

- Use FashionCLIP or CLIP embeddings for better fashion understanding.
- Train using full human-curated outfit datasets.
- Add triplet loss or contrastive learning for better similarity.
- Use FAISS or a vector database for faster large-scale retrieval.
- Add text + image multimodal search.
- Add occasion-based styling, such as party, formal, casual, sports.
- Add color harmony and seasonal trend analysis.
- Build a complete outfit generation system.

## 19. Real-World Applications

This project can be used in:

- e-commerce fashion platforms,
- visual search engines,
- online stylist assistants,
- complete-the-look recommendation systems,
- catalog organization,
- product similarity detection,
- outfit planning apps.

## 20. Conclusion

This project demonstrates a complete fashion AI system that uses real product images to perform visual similarity search and outfit compatibility prediction.

It combines:

- CNN embeddings,
- PCA,
- KMeans clustering,
- cosine nearest-neighbor search,
- pairwise classification,
- Streamlit UI,
- FastAPI backend,
- Docker deployment.

The system goes beyond traditional recommendation systems by learning visual style representations from images.

Final presentation line:

```text
This project teaches a machine to understand fashion visually, so it can find similar products and predict which items aesthetically work together.
```
