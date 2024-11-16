import json
from src.recipe_data import RecipeData

SQLITE_FILENAME = "./src/data/recipes.sqlite"
JSON_FILENAME = "./src/data/recipes_validated.json"
EMBEDDINGS_FILENAME = "./src/data/recipe_embeddings.pickle"

def read_recipe_json() -> list[RecipeData]:
    with open(JSON_FILENAME, "r") as f:
        raw_data = json.load(f)["recipes"]
    return [RecipeData(**item) for item in raw_data]