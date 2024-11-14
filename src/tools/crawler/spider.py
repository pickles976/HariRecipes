import json
import csv
from typing import Optional
from bs4 import BeautifulSoup
from urllib.request import urlopen
import tldextract
import pickle

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
            visited_links: Optional[list[str]] = None,
            visited_recipes: Optional[list[str]] = None,
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
        self.current_url = root_url

        self.recipe_prefix = recipe_prefix
        self.recipe_schema = recipe_schema
        self.ignore = ignore
        self.subdomain = subdomain
        
        self.seen = set()
        self.recipes = set()
        self.domain = tldextract.extract(url).domain

        # Load checkpoints if they exist
        if visited_links is not None:
            self.seen = set(visited_links)

        if visited_recipes is not None:
            self.recipes = set(visited_recipes)

        print(f"Received extra arguments: {args} {kwargs}. Ignoring...")

    def should_ignore_link(self, url: str) -> bool:
                
        # Ignore links from different websites
        if tldextract.extract(url).domain != self.domain:
            return True
        
        # Ignore other subdomains if that matters (for example, if we want cooking.en, don't go to cooking.fr)
        if self.subdomain is not None:
            if tldextract.extract(url).subdomain != self.subdomain:
                return True
        
        # Ignore URLs with keywords
        if self.ignore is not None:
            for item in self.ignore:
                if item in url:
                    return True
        
        return False
        
    def checkpoint(self):

        """Save the recipes at the current checkpoint"""
        print("CHECKPOINT REACHED! SAVING...")
        with open(f'{self.domain}.pickle', 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def add_recipe(self, recipe_url: str):
        print(f"RECIPE: {recipe_url}")
        self.recipes.add(recipe_url)
        if len(self.recipes) % CHECKPOINT == 0:
            self.checkpoint()

    # DFS walker
    def walk_page(self, url: str, depth: int=0):

        self.current_url = url

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

                # html tag can have multiple classes, so it's a list.
                # also, recipe schemas like "yoast-schema-graph" DOES NOT MEAN A PAGE HAS A RECIPE.
                # people sometimes use the schema even with articles. Better to just save the link anyways.
                if self.recipe_schema in item.get("class"):
                    self.add_recipe(url)
                    break

            # If the recipe schema is unknown, look to see if the ld+json content has a recipe tag in it somewhere.
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

        # This only works for grouprecipes.com
        if self.domain == "grouprecipes":
            body = soup.find_all('body')
            if body is not None:
                for item in body:
                    tag_class = item.get("class")
                    if tag_class is None:
                        continue

                    if "hrecipe" in tag_class:
                        self.add_recipe(url)
                        break
                

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
        return self.walk_page(self.current_url)