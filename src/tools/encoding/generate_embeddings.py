from src.recipe_data import data_to_str
from common import read_recipe_json, EMBEDDINGS_FILENAME

import time
import pickle

from sentence_transformers import SentenceTransformer

print("Loading recipes...")
recipes = read_recipe_json()
print(f"Loaded {len(recipes)} recipes!")

print("Loading Sentence Transformer...")
try:
    embedder = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
except Exception as e:
    print(e)
    print("CUDA NOT FOUND! Defaulting to CPU...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Corpus consisting of example titles
print("Extracting recipe info...")
corpus = [data_to_str(item) for item in recipes]

print("Example Recipe: ")
print("\n\n\n")
print(corpus[1])
print("\n\n\n")

# Use "convert_to_tensor=True" to keep the tensors on GPU (if available)
print("Generating corpus embeddings...")
start = time.time()
corpus_embeddings = embedder.encode(
    corpus, convert_to_tensor=True, normalize_embeddings=True, show_progress_bar=True
)
print(f"Generated embeddings in {int(time.time() - start)}s")

# Save as pickle
print("Pickling embeddings...")
with open(EMBEDDINGS_FILENAME, "wb") as handle:
    pickle.dump(corpus_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)
