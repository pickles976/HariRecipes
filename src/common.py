import json
from src.recipe_data import RecipeData

SQLITE_FILENAME = "./data/recipes.sqlite"
JSON_FILENAME = "./data/recipes_validated.json"
EMBEDDINGS_FILENAME = "./data/recipe_embeddings.pickle"
BINARY_EMBEDDINGS_FILENAME = "./data/recipe_embeddings_binary.pickle"

def read_recipe_json() -> list[RecipeData]:
    with open(JSON_FILENAME, "r") as f:
        raw_data = json.load(f)["recipes"]
    return [RecipeData(**item) for item in raw_data]