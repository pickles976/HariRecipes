import sys
import os

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI
from sentence_transformers import SentenceTransformer

from src.recipe_data import RecipeData
from src.service.db import RecipeRepoSQLite
from src.service.search import FloatVectorSearch, BinaryVectorSearch
from src.common import load_binary_embeddings, load_full_embeddings

FLOAT_32_SEARCH = os.getenv("FLOAT_32_SEARCH", default=0)
BINARY_EMBEDDINGS = os.getenv("BINARY_EMBEDDINGS", default=1)
CUDA = os.getenv("CUDA", default=0)
MODEL_NAME = "all-MiniLM-L6-v2"

print(f"FLOAT_32_SEARCH: {FLOAT_32_SEARCH}")
print(f"BINARY_EMBEDDINGS: {BINARY_EMBEDDINGS}")
print(f"CUDA: {CUDA}")

recipe_repo = RecipeRepoSQLite()

if CUDA == 1:
    model = SentenceTransformer(MODEL_NAME, device="cuda")
else:
    model = SentenceTransformer(MODEL_NAME, device="cpu")

if FLOAT_32_SEARCH:
    embeddings = load_full_embeddings()
    vector_search = FloatVectorSearch(recipe_repo, embeddings, model)
else:
    if BINARY_EMBEDDINGS:
        embeddings = load_binary_embeddings()
    else:
        embeddings = load_full_embeddings()
    vector_search = BinaryVectorSearch(recipe_repo, embeddings, model)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}