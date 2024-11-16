import os
import sys
import time
import logging

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer

from src.recipe_data import RecipeData
from src.service.db import RecipeRepoSQLite
from src.service.search import FloatVectorSearch, BinaryVectorSearch
from src.service.templating import home_template, query_results_template
from src.common import load_binary_embeddings, load_full_embeddings

LOG_LEVEL = os.getenv("LOG_LEVEL", default="INFO")
FLOAT_32_SEARCH = os.getenv("FLOAT_32_SEARCH", default=0)
BINARY_EMBEDDINGS = os.getenv("BINARY_EMBEDDINGS", default=1)
CUDA = os.getenv("CUDA", default=0)
MODEL_NAME = "all-MiniLM-L6-v2"
MAX_RESULTS = 250

logger = logging.getLogger(__name__)
logging.basicConfig(filename='app.log', level=logging.getLevelNamesMapping()[LOG_LEVEL]) # throws exception if you use a nonsense value

logger.info(f"FLOAT_32_SEARCH: {FLOAT_32_SEARCH}")
logger.info(f"BINARY_EMBEDDINGS: {BINARY_EMBEDDINGS}")
logger.info(f"CUDA: {CUDA}")

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

@app.get("/", response_class=HTMLResponse)
async def home():
    return home_template()

@app.get("/recipe_query/{query}/{num_items}", response_class=HTMLResponse)
async def recipe_query(query, num_items: int = 20):
    start = time.time()
    top_k = min(num_items, MAX_RESULTS)
    data = vector_search.query(query_string=query, top_k=top_k)
    logger.debug(f"Got {top_k} results in {time.time() - start:.3f}s")
    return query_results_template(data)

@app.get("/recipe/{index}")
async def recipe(index: int):
    recipes = recipe_repo.list_recipes([index])

    if len(recipes) != 1:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return list(recipes.values())[0].model_dump()