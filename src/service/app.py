import os
import sys
import time
import logging

# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from sentence_transformers import SentenceTransformer

from src.service.db import RecipeRepoSQLite
from src.service.search import FloatVectorSearch, BinaryVectorSearch
from src.service.templating import (
    home_template,
    query_results_template,
    recipe_detail_template,
)
from src.common import load_binary_embeddings, load_full_embeddings

MAX_RESULTS = 250
LOG_LEVEL = os.getenv("LOG_LEVEL", default="DEBUG")
BASE_URL = os.getenv("BASE_URL", default="http://localhost:8000")
FLOAT_32_SEARCH = os.getenv("FLOAT_32_SEARCH", default=0)
BINARY_EMBEDDINGS = os.getenv("BINARY_EMBEDDINGS", default=1)
CUDA = os.getenv("CUDA", default=0)
MODEL_NAME = "all-MiniLM-L6-v2"

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="app.log", level=logging.getLevelNamesMapping()[LOG_LEVEL]
)  # throws exception if you use a nonsense value
logger.addHandler(logging.StreamHandler())

logger.info(f"BASE_URL: {BASE_URL}")
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


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("./src/service/templates/favicon.ico")


@app.get("/recipe_query/", response_class=HTMLResponse)
async def recipe_query(query, num_items: str = "20"):
    start = time.time()

    # Try to parse int
    try:
        num_items = int(num_items)
    except Exception:
        num_items = 20

    top_k = max(min(num_items, MAX_RESULTS), 10)
    data = vector_search.query(query_string=query, top_k=top_k)
    logger.debug(f"Query: {query}")
    logger.debug(f"Num Items: {num_items}")
    logger.debug(f"Got {top_k} results in {time.time() - start:.3f}s")
    return query_results_template(BASE_URL, data, query, num_items)


@app.get("/recipe/", response_class=HTMLResponse)
async def recipe(index: int):
    recipes = recipe_repo.list_recipes([index])

    if len(recipes) != 1:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe_detail_template(BASE_URL, list(recipes.values())[0], index)


@app.get("/recipe/json/")
async def recipe_json(index: int):
    recipes = recipe_repo.list_recipes([index])

    if len(recipes) != 1:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return list(recipes.values())[0].model_dump()
