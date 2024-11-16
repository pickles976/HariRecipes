import os
import json
import sqlite3
from abc import ABC

from src.recipe_data import RecipeData
from src.common import SQLITE_FILENAME, JSON_FILENAME


class AbstractRecipeRepo(ABC):
    """Abstract interface for Recipe access"""

    def list_recipes(self, indices: list[int]) -> list[RecipeData]:
        raise NotImplementedError()


class RecipeRepoSQLite(AbstractRecipeRepo):
    """Concrete implementation using SQLite for persistence"""

    conn: sqlite3.Connection
    cursor: sqlite3.Cursor

    def __init__(self):
        if not os.path.exists(SQLITE_FILENAME):
            raise Exception("Recipe SQLite file not found!")

        self.conn = sqlite3.connect(SQLITE_FILENAME)
        self.cursor = self.conn.cursor()

    def list_recipes(self, indices: list[int]) -> dict[int, RecipeData]:
        """Return a dict mapping indices to RecipeData because order is not guaranteed"""
        indices_plus_one = [i + 1 for i in indices]  # SQLite IDs start at 1
        query = f"SELECT * FROM recipes WHERE id IN ({','.join(['?'] * len(indices))})"
        self.cursor.execute(query, indices_plus_one)
        recipe_items = self.cursor.fetchall()
        # Convert sqlite id to zero-index
        return {item[0] - 1: RecipeData(**json.loads(item[1])) for item in recipe_items}


class RecipeRepoJSON(AbstractRecipeRepo):
    """Concrete implementation that loads all recipes into memory"""

    recipes: list[RecipeData]

    def __init__(self):
        print("Loading recipes...")
        with open(JSON_FILENAME, "r") as f:
            raw_data = json.load(f)["recipes"]
        self.recipes = [RecipeData(**item) for item in raw_data]

    def list_recipes(self, indices: list[int]) -> dict[int, RecipeData]:
        recipes = {}
        for index in indices:
            recipes[index] = self.recipes[index]
        return recipes


if __name__ == "__main__":
    """
        Run this file as a script to generate the sqlite data from json:
        `python -m src.service.db`
    """

    if not os.path.exists(SQLITE_FILENAME):
        print("Loading recipes...")
        with open(JSON_FILENAME, "r") as f:
            raw_data = json.load(f)["recipes"]
        recipes = [RecipeData(**item) for item in raw_data]

        print("Populating SQLite file...")
        conn = sqlite3.connect(SQLITE_FILENAME)
        cursor = conn.cursor()

        # CREATE TABLE
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_data JSON
        )
        """)
        conn.commit()

        # INSERT RECIPES
        query = "INSERT INTO recipes (recipe_data) VALUES (?)"
        data_to_insert = [(json.dumps(item.model_dump()),) for item in recipes]
        cursor.executemany(query, data_to_insert)

        conn.commit()
        conn.close()

    # Test the repo
    recipe_repo = RecipeRepoSQLite()
    recipes = recipe_repo.list_recipes([0, 1, 2, 1000])

    # first recipe should be Sabor Sazon
    print(recipes)
