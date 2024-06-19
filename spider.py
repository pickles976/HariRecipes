import json
from typing import Optional
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

# We should easily find all recipes above this depth
DEPTH_LIMIT = 10
CHECKPOINT = 1000

def read_url(url: str) -> str:
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

class Spider:

    def __init__(
            self, 
            url: str,
            root_url: str, 
            recipe_prefix: Optional[str] = None, 
            recipe_schema: Optional[str] = None
        ) -> None:
        """
        An object for web scraping. Tracks visited links and identified recipes.

        Parameters:
            url (str): base url of the website
            root (str): url to start crawling from (often different from the website url)
            recipe_prefix (Optional[str]): prefix to a url that is only used for recipes
            recipe_schema (Optional[str]): schema class that identifies a page as a recipe or not
        """
        self.url = url
        self.root_url = root_url
        self.recipe_prefix = recipe_prefix
        self.recipe_schema = recipe_schema

        if self.recipe_schema is None and self.recipe_prefix is None:
            raise Exception("Must provide either Recipe URL Prefix or Recipe Schema!")
        
        self.visited = {}
        self.recipes = {}
        self.total = 1
        self.domain = urlparse(url).netloc
        
    def checkpoint(self):
        """Save the recipes at the current checkpoint"""
        print("CHECKPOINT REACHED! SAVING...")
        with open(f"./data/{self.domain}_recipes_{self.total}.json", "w") as f:
            json.dump(self.recipes, f)

        with open(f"./data/{self.domain}_links_{self.total}.json", "w") as f:
            json.dump(self.visited, f)

    # DFS walker
    def walk_page(self, url: str, depth: int=0):

        if depth > DEPTH_LIMIT:
            return

        if self.total % CHECKPOINT == 0:
            self.checkpoint()

        print(url)
        stack = []

        current_page = read_url(url)
        soup = BeautifulSoup(current_page, 'html.parser')

        if self.recipe_schema is not None:
            # Check if a script tag with the recipe schema exists
            scripts = soup.find_all('script', type="application/ld+json")
            for item in scripts:
                if self.recipe_schema in item.get("class"):
                    print(f"RECIPE: {url}")
                    self.recipes[url] = True
                    self.total += 1

        for link in soup.find_all('a'):

            link_url = link.get('href')

            # Ignore visited links
            if link_url in self.visited:
                continue

            # Ignore links from different websites
            if not self.url in link_url:
                continue

            # If a prefix URL is not sufficient to identify link as a valid recipe
            if self.recipe_prefix is None:
                stack.append(link_url)
                continue
        
            # URL is a recipe
            if self.recipe_prefix in link_url:
                print(f"RECIPE: {link_url}")
                self.recipes[link_url] = True
                self.visited[link_url] = True
                self.total += 1
            else:
                stack.append(link_url)

        for link in stack:
            self.visited[link] = True

            self.walk_page(link, depth+1)

    def start(self):
        self.walk_page(self.root_url)

if __name__ == "__main__":
    spider = Spider(
        url="https://www.allrecipes.com/",
        root_url="https://www.allrecipes.com/recipes/",
        recipe_prefix="https://www.allrecipes.com/recipe/",
        # recipe_schema="allrecipes-schema"
    )
    spider.start()

    print(f"Found: {len(spider.visited)} links!")
    print(f"Found: {len(spider.recipes)} recipes!")

    spider.checkpoint()