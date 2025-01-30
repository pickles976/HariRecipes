import os
import json
from src.recipe_data import RecipeData

def is_valid(recipe: RecipeData) -> bool:
    if len(recipe.instructions_list) == 0:
        return False
    
    if len(recipe.ingredient_groups) == 0:
        return False
    
    if len(recipe.ingredient_groups[0].ingredients) == 0:
        return False
    
    return True

with open("./data/recipes_cleaned.json", "r") as f:
    recipes = json.load(f)["recipes"]

print(len(recipes))

parsed = [RecipeData(**item) for item in recipes]
filtered = [item for item in parsed if is_valid(item)]

print(len(filtered))

with open("./data/recipes.json", "w") as f:
    json.dump({"recipes": [item.model_dump() for item in filtered]}, f)