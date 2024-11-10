import json
from recipe_data import RecipeData
import time
import pickle

import torch
from sentence_transformers import SentenceTransformer

print("Loading recipes...")
with open("./recipes_validated.json", "r") as f:
    raw_data = json.load(f)["recipes"]
recipes = [RecipeData(**item) for item in raw_data]
print(f"Loaded {len(recipes)} recipes!")

print("Loading Sentence Transformer...")
embedder = SentenceTransformer("all-MiniLM-L6-v2", model_kwargs={"torch_dtype": "float16"})

# Corpus consisting of example titles
# TODO: map titles to recipe data
print("Extracting titles...")
corpus = [item.title for item in recipes]

# Use "convert_to_tensor=True" to keep the tensors on GPU (if available)
print("Generating corpus embeddings...")
start = time.time()
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
print(f"Generated embeddings in {time.time() - start}s")

# Save as pickle
with open('title_embeddings.pickle', 'wb') as handle:
    pickle.dump(corpus_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)