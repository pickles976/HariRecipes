import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

visited = {}
recipes = {}

def read_url(url: str) -> str:
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

base_url = "https://www.allrecipes.com/recipes/"
recipe_url = "https://www.allrecipes.com/recipe"

# DFS walker
def walk_page(url: str):

    global visited
    print(url)
    stack = []

    current_page = read_url(url)
    soup = BeautifulSoup(current_page, 'html.parser')

    for link in soup.find_all('a'):

        link_url = link.get('href')

        if link_url in visited:
            continue

        # Sub-links are categories
        if base_url in link_url:
            stack.append(link_url)
        elif recipe_url in link_url: # Non sub-links are recipes
            print(f"RECIPE: {link_url}")
            recipes[recipe_url] = recipe_url
            visited[recipe_url] = recipe_url
    
    for link in stack:
        visited[link] = link
        walk_page(link)

walk_page(base_url)

print(f"Visited: {len(visited)} links!")
print(f"Found: {len(recipes)} recipes!")

with open("allrecipes_links.json", "w") as f:
    json.dump(visited, f)


with open("allrecipes.json", "w") as f:
    json.dump(recipes, f)