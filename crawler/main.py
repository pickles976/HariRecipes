import os
import csv
import json
import pickle
from crawler.spider import Spider
from datetime import datetime
from urllib.request import urlopen


if __name__ == "__main__":
    
    with open("./websites.json") as f:
        items = json.load(f)["sources"]

    for item in items:

        spider=Spider(**item)

        # Check for pickle
        picklename = f'{spider.domain}.pickle'
        if os.path.exists(picklename):
            with open(picklename, 'rb') as handle:
                spider = pickle.load(handle)
                print(f"Restored pickle file with: {len(spider.recipes)} recipes!")

        start = datetime.now()
        
        spider.start()

        print(f"Elapsed: {datetime.now() - start}")

        print(f"Found: {len(spider.seen)} links!")
        print(f"Found: {len(spider.recipes)} recipes!")

        print("SAVING RECIPES")
        with open(f"./recipe_lists/{spider.domain}_recipes_{len(spider.recipes)}.csv", "w") as f:
            writer = csv.writer(f, delimiter='\n')
            writer.writerows([list(spider.recipes)])