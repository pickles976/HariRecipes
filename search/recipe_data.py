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
    ingredients: list[str]
    ingredient_groups: list[IngredientGroups]
    instructions: str
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



