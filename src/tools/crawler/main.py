import os
import csv
import json
import pickle
from src.tools.crawler.spider import Spider
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


def crawl_site_threaded(item: dict) -> tuple[str, datetime]:

    url = item['url']
    print(f"CRAWLING DOMAIN: {url}")

    spider=Spider(**item)

    # Check for pickle
    picklename = f'{spider.domain}.pickle'
    if os.path.exists(picklename):
        with open(picklename, 'rb') as handle:
            spider = pickle.load(handle)
            print(f"Restored pickle file with: {len(spider.recipes)} recipes!")

    start = datetime.now()
    spider.start()
    elapsed = datetime.now() - start
    print(f"Crawled {url} in: {elapsed}")
    print(f"Found: {len(spider.seen)} links!")
    print(f"Found: {len(spider.recipes)} recipes!")
    print("SAVING RECIPES")
    with open(f"./src/data/recipe_lists/{spider.domain}_recipes_{len(spider.recipes)}.csv", "w") as f:
        writer = csv.writer(f, delimiter='\n')
        writer.writerows([list(spider.recipes)])

    return (url, elapsed)

if __name__ == "__main__":
    
    with open("./src/data/websites.json") as f:
        items = json.load(f)["sources"]

    start = datetime.now()

    with ThreadPoolExecutor(max_workers=64) as executor:
        res = executor.map(crawl_site_threaded, items)

    print(f"FINISHED IN: {datetime.now() - start}")
