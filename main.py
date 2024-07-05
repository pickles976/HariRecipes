import json
from spider import Spider
from datetime import datetime
from urllib.request import urlopen

URL = "https://bowlofdelicious.com/"

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

        start = datetime.now()
        spider.start()
        print(f"Elapsed: {datetime.now() - start}")

        print(f"Found: {len(spider.seen)} links!")
        print(f"Found: {len(spider.recipes)} recipes!")

        spider.checkpoint()