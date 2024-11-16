from jinja2 import Environment, PackageLoader, select_autoescape
from src.recipe_data import RecipeData

BASE_URL = "http://localhost:8000"

env = Environment(
    loader=PackageLoader("app"),
    autoescape=select_autoescape()
)

def home_template() -> str:
    template = env.get_template("home.html")
    return template.render()

def query_results_template(recipes: list[RecipeData, int, float]) -> str:
    template = env.get_template("query_results.html")
    return template.render(base_url=BASE_URL, recipes=recipes)