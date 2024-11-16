from jinja2 import Environment, PackageLoader, select_autoescape
from src.recipe_data import RecipeData

BASE_URL = "http://localhost:8000"

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

def home_template() -> str:
    template = env.get_template("index.html")
    return template.render()

def query_results_template(recipes: list[RecipeData, int, float], query: str, num_items: int) -> str:
    template = env.get_template("index.html")
    return template.render(base_url=BASE_URL, recipes=recipes, query=query, num_items=num_items)

def recipe_detail_template(recipe: RecipeData, index: int) -> str:
    template = env.get_template("index.html")
    return template.render(base_url=BASE_URL, recipe=recipe, index=index)