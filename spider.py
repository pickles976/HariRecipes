import json
import csv
from typing import Optional
from bs4 import BeautifulSoup
from urllib.request import urlopen
import tldextract

# We should easily find all recipes above this depth
DEPTH_LIMIT = 10
CHECKPOINT = 5000

def read_url(url: str) -> str:
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

def is_json_recipe(data) -> bool:

    # Type of recipe or article
    if "@type" in data and (
        "Recipe" in data["@type"]
        # or "Article" in data["@type"]
    ):
        return True
    
    # Type of Recipe/Article is in graph
    if "@graph" in data:
        if isinstance(data["@graph"], list):
            for item in data["@graph"]:
                if "@type" in item and (
                    "Recipe" in item["@type"]
                    # or "Article" in item["@type"]
                ):
                    return True

    return False

class Spider: 

    def __init__(
            self, 
            url: str,
            root_url: str, 
            recipe_prefix: Optional[str] = None, 
            recipe_schema: Optional[str] = None,
            ignore: Optional[list[str]] = None,
            subdomain: Optional[str] = None,
            *args,
            **kwargs
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
        self.ignore = ignore
        self.subdomain = subdomain
        
        self.seen = set()
        self.recipes = set()
        self.domain = tldextract.extract(url).domain

        print(f"Received extra arguments: {args} {kwargs}. Ignoring...")

    def should_ignore_link(self, url: str) -> bool:
                
        # Ignore links from different websites
        if tldextract.extract(url).domain != self.domain:
            return True
        
        # Ignore subdomain if that matters
        if self.subdomain is not None:
            if tldextract.extract(url).subdomain != self.subdomain:
                return True
        
        if self.ignore is not None:
            for item in self.ignore:
                if item in url:
                    return True
        
        return False
        
    def checkpoint(self):
        """Save the recipes at the current checkpoint"""
        print("CHECKPOINT REACHED! SAVING...")
        with open(f"./data/{self.domain}_recipes_{len(self.recipes)}.csv", "w") as f:
            writer = csv.writer(f, delimiter='\n')
            writer.writerows([list(self.recipes)])

        # with open(f"./data/{self.domain}_links_{len(self.seen)}.csv", "w") as f:
        #     writer = csv.writer(f, delimiter='\n')
        #     writer.writerows([list(self.seen)])

    def add_recipe(self, recipe_url: str):
        print(f"RECIPE: {recipe_url}")
        self.recipes.add(recipe_url)
        if len(self.recipes) % CHECKPOINT == 0:
            self.checkpoint()

    # DFS walker
    def walk_page(self, url: str, depth: int=0):

        if depth > DEPTH_LIMIT:
            return

        print(url)
        stack = []

        try:
            current_page = read_url(url)
        except Exception as e:
            print(f"Failed to reach url with exception: {e}")
            return

        soup = BeautifulSoup(current_page, 'html.parser')

        # Check if a script tag with the recipe schema exists
        scripts = soup.find_all('script', type="application/ld+json")

        for item in scripts:

            # Check that script has the correct class, if we provided a schema (saves us time)
            if self.recipe_schema is not None:
                if item.get("class") is None:
                    continue

            try:
                data = json.loads(item.text)

                if isinstance(data, list):
                    for item in data:
                        if is_json_recipe(item):
                            self.add_recipe(url)
                            break
                else:
                    if is_json_recipe(data):
                        self.add_recipe(url)
                        break
            except Exception as e:
                print(f"Failed to parse script text with exception: {e}")

        # Loop over every link on the page
        for link in soup.find_all('a'):

            link_url = link.get('href')

            if link_url is None:
                continue

            # Handle routes
            if tldextract.extract(link_url).domain == "":
                link_url = self.url + link_url
            
            # Filter out authentication, etc
            if self.should_ignore_link(link_url):
                continue

            # Ignore previously visited links
            if link_url in self.seen:
                continue

            # Mark link as seen
            self.seen.add(link_url)

            # If a prefix URL is not sufficient to identify link as a valid recipe
            if self.recipe_prefix is None:
                stack.append(link_url)
                continue
        
            # URL is a recipe
            if self.recipe_prefix in link_url:
                self.add_recipe(link_url)
            else:
                stack.append(link_url)

        for link in stack:
            self.walk_page(link, depth+1)

    def start(self):
        self.walk_page(self.root_url)