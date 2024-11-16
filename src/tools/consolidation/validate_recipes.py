"""Filters out all recipes that don't adhere to our rules"""

import json
from tqdm import tqdm
from recipe_data import RecipeData

fields = [
    "language",
    "description",
    "nutrients",
    "cooking_method",
    "image",
    "prep_time",
    "ratings",
    "host",
    "cuisine",
    "category",
    "equipment",
    "author",
    "site_name",
    "yields",
    "canonical_url",
    "title",
    "total_time",
    "ingredient_groups",
    "instructions_list",
    "cook_time",
]
field_set = set(fields)

nutrient_fields = [
    "calories",
    "fatContent",
    "saturatedFatContent",
    "carbohydrateContent",
    "sugarContent",
    "fiberContent",
    "proteinContent",
    "sodiumContent",
]

print("Loading json...")
with open("./data/recipes.json", "r") as f:
    recipes = json.load(f)["recipes"]

print("Grabbing keys...")
valid_recipes = []
for i in tqdm(range(len(recipes))):
    item = recipes[i]

    # Non-optional fields
    if "title" not in item:
        continue
    if "canonical_url" not in item:
        continue
    if "instructions_list" not in item:
        continue
    if "ingredient_groups" not in item:
        continue

    # Remove useless info
    if "ratings" in item:
        del item["ratings"]

    # Nutrients is a nested field
    if "nutrients" in item:
        if item["nutrients"] == {}:
            item["nutrients"] = None
        else:
            for key in nutrient_fields:
                if key not in item["nutrients"]:
                    item["nutrients"][key] = None

    # Populate optional fields
    for key in field_set:
        if key not in item:
            item[key] = None

    valid_recipes.append(RecipeData(**item))

print("Saving json...")
with open("./data/recipes_validated.json", "w") as f:
    json.dump({"recipes": [item.model_dump() for item in valid_recipes]}, f)
