from jinja2 import Environment, PackageLoader, select_autoescape
from src.recipe_data import RecipeData

env = Environment(loader=PackageLoader("app"), autoescape=select_autoescape())


def home_template(base_url: str) -> str:
    template = env.get_template("index.html")
    return template.render()


def query_results_template(
    base_url: str, recipes: list[RecipeData, int, float], query: str, num_items: int
) -> str:
    template = env.get_template("index.html")
    return template.render(
        base_url=base_url, recipes=recipes, query=query, num_items=num_items
    )


def recipe_detail_template(base_url: str, recipe: RecipeData, index: int) -> str:
    template = env.get_template("index.html")
    return template.render(base_url=base_url, recipe=recipe, index=index)
