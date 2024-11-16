import csv
import json
from datetime import datetime
from recipe_scrapers import scrape_me

def scrape_url(url: str) -> dict:
    try:
        scraper = scrape_me(url)
        scraper.host()
        return scraper.to_json()
    except:
        return {}

start = datetime.now()

urls = []
with open('./data/all_recipes.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\n')
    for row in reader:
        if len(row) == 1:
            urls.append(row[0])

recipes = []
for i, url in enumerate(urls):
    print(f"{i} : {url}")
    recipes.append(scrape_url(url))

print(f"FINISHED IN: {datetime.now() - start}")

with open('./data/recipes.json', 'w') as f:
    json.dump({"recipes" : recipes}, f)

print(f"{len(recipes)} RECIPES!")
