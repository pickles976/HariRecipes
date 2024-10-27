import json
from recipe_data import RecipeData

with open("./recipes_validated.json", "r") as f:
    raw_data = json.load(f)["recipes"]
recipes = [RecipeData(**item) for item in raw_data]
print(len(recipes))