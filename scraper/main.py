import csv
import json
import pickle
from datetime import datetime
from recipe_scrapers import scrape_me
from concurrent.futures import ThreadPoolExecutor

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def scrape_url(url: str) -> dict:
    try:
        scraper = scrape_me(url)
        scraper.host()
        return scraper.to_json()
    except:
        return {}

start = datetime.now()

class Scraper:

    def __init__(self, urls : list[str],chunk_size : int, workers: int):

        self.workers = workers
        self.urls = urls
        self.url_chunks = list(divide_chunks(urls, chunk_size))
        self.recipes = []
        self.i = 0

    def scrape(self):
        chunk = self.url_chunks[self.i]
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            res = executor.map(scrape_url, chunk)
            self.recipes += list(res)
        print(f"ELAPSED: {datetime.now() - start} RECIPES: {len(self.recipes)}")

        with open('scraper.pickle', 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

        self.i += 1

urls = []
with open('./all_recipes.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\n')
    for row in reader:
        if len(row) == 1:
            urls.append(row[0])

scraper = Scraper(urls, chunk_size=2048, workers=256)
while len(scraper.url_chunks) > scraper.i:
    scraper.scrape()

print(f"FINISHED IN: {datetime.now() - start}")

with open('./recipes.json', 'w') as f:
    json.dump({"recipes" : scraper.recipes}, f)

print(f"{len(scraper.recipes)} RECIPES!")
