import json
from bs4 import BeautifulSoup
from urllib.request import urlopen

url="https://www.allrecipes.com/one-pan-chicken-gnocchi-recipe-8647662"
recipe_schema="allrecipes-schema"

def read_url(url: str) -> str:
    page = urlopen(url)
    html_bytes = page.read()
    return html_bytes.decode("utf-8")

current_page = read_url(url)
soup = BeautifulSoup(current_page, 'html.parser')
scripts = soup.find_all('script', type="application/ld+json")

# try:
for item in scripts:
    script_class = item.get("class")

    if script_class is None:
        continue
    
    if recipe_schema in script_class:
        data = json.loads(item.text)

        # Check for Recipe tag
        first = data[0]
        if "@type" in first and "Recipe" in first["@type"]:
            print(first)