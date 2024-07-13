import csv
import json
from datetime import datetime
from recipe_scrapers import scrape_me
from concurrent.futures import ThreadPoolExecutor

total = 0
start = datetime.now()

def scrape_url(url: str) -> dict:
    global total
    global start
    total += 1
    if total % 1000 == 0:
        print(f"Elapsed: {datetime.now() - start} Scraped {total} recipes...")
    scraper = scrape_me(url)
    scraper.host()
    return scraper.to_json()

urls = []
with open('./all_recipes.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\n')
    for row in reader:
        if len(row) == 1:
            urls.append(row[0])

with ThreadPoolExecutor(max_workers=64) as executor:
    res = executor.map(scrape_url, urls)
print(f"FINISHED IN: {datetime.now() - start}")

recipes = {"recipes" : list(res)}

with open('./recipes.json', 'w') as f:
    json.dump(recipes, f)

print(f"{len(recipes)} RECIPES!")
