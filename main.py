import os
import csv
import json
import pickle
from spider import Spider
from datetime import datetime
from urllib.request import urlopen

URL = "https://minimalistbaker.com/"

if __name__ == "__main__":
    
    try:
        urlopen(URL).read()
    except Exception as e:
        print(e)
        print(f"{URL} does not allow scraping!")
        exit()

    with open("./websites.json") as f:
        items = json.load(f)["sources"]

    for item in items:
        if item["url"] != URL: 
            continue

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
        with open(f"./data/{spider.domain}_recipes_{len(spider.recipes)}.csv", "w") as f:
            writer = csv.writer(f, delimiter='\n')
            writer.writerows([list(spider.recipes)])