"""Test that all recipes can be parsed to a Pydantic model"""
import json
from tools.recipe_data import RecipeData

print("Reading json...")
with open("./recipes_validated.json", "r") as f:
    raw_data = json.load(f)["recipes"]

print("Parsing recipes...")
recipes = [RecipeData(**item) for item in raw_data]
print(len(recipes))