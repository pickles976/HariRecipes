from typing import Optional
from pydantic import BaseModel

class IngredientGroups(BaseModel):
    ingredients: list[str]
    purpose: Optional[str]

class Nutrients(BaseModel):
    calories: Optional[str]
    fatContent: Optional[str]
    saturatedFatContent: Optional[str]
    carbohydrateContent: Optional[str]
    sugarContent: Optional[str]
    fiberContent: Optional[str]
    proteinContent: Optional[str]
    sodiumContent: Optional[str]

class RecipeData(BaseModel):

    # Recipe info
    title: str
    canonical_url: str
    ingredient_groups: list[IngredientGroups]
    instructions_list: list[str]

    # Metadata
    author: Optional[str]
    image: Optional[str]
    language: str
    host: str

    # Details
    site_name: Optional[str]
    category: Optional[str]
    cook_time: Optional[int]
    cooking_method: Optional[str]
    cuisine: Optional[str]
    prep_time: Optional[int]
    yields: Optional[str]
    total_time: Optional[int]
    nutrients: Optional[Nutrients]
    equipment: Optional[list[str]]
    description: Optional[str]

def data_to_str(data: RecipeData) -> str:

    ingredients = f"Ingredients: \n"
    for ingredient in data.ingredients:
        ingredients += f"- {ingredient}\n"

    text = f"""
{data.title}
{ingredients}
Instructions: 
{data.instructions}"""
    
    if data.description:
        text += "\n"
        text += data.description

    return text


