from recipe_scrapers import scrape_me

scraper = scrape_me(
    "https://www.allrecipes.com/recipe/158968/spinach-and-feta-turkey-burgers/"
)

# Q: What if the recipe site I want to extract information from is not listed below?
# A: You can give it a try with the wild_mode option! If there is Schema/Recipe available it will work just fine.
scraper = scrape_me("https://www.feastingathome.com/tomato-risotto/", wild_mode=True)

scraper.host()
scraper.title()
scraper.total_time()
scraper.image()
scraper.ingredients()
scraper.ingredient_groups()
scraper.instructions()
scraper.instructions_list()
scraper.yields()
scraper.to_json()
scraper.links()
scraper.nutrients()  # not always available
scraper.canonical_url()  # not always available
scraper.equipment()  # not always available
scraper.cooking_method()  # not always available
scraper.keywords()  # not always available
scraper.dietary_restrictions()  # not always available
