"""
    Script for validating recipes with an LLM. Very bad, do not copy.
"""

import re
import json
import time
import requests
from requests import Response

url = "http://127.0.0.1:1234/v1/chat/completions"
headers = {"Content-Type": "application/json"}

def format(data: dict) -> dict:
    return {
        "messages": [
        { "role": "user", "content": json.dumps(data) }
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    
def is_valid(response: Response) -> bool:
    """Invalid recipe will end with @N"""
    content = response.json()["choices"][0]["message"]["content"]
    if len(re.findall("@N", content)) == 1:
        return False
    return True

print("Loading recipes...")
filepath = "./data/recipes_validated.json"
with open(filepath, "r") as f:
    all_recipes = json.load(f)["recipes"]


items = []
print("Starting inference...")
for i, recipe in enumerate(all_recipes):

    print(recipe["title"])
    start = time.time()
    res = requests.post(url=url, json=format(recipe), headers=headers)
    if res.status_code != 200:
        print(f"ERROR: {res.content}")
        continue
    
    valid = is_valid(response=res)
    print(f"{str(valid).upper()} {time.time() - start:.2f}")
    if valid:
        items.append(recipe)

print("SAVING JSON...")
with open(f"./data/cleaned/{len(items)}.json", "w") as f:
    json.dump({
        "recipes": items
    }, f)

# print("Opening")
# filepath = "./data/recipes_cleaned.json"
# with open(filepath, "r") as f:
#     all_recipes = json.load(f)["recipes"]

# print(f"Consolidating {len(all_recipes)} recipes...")
# recipes = [json.dumps(item) for item in all_recipes]
# recipes = list(set(recipes))
# recipes = [json.loads(item) for item in recipes]
# print(f"Consolidated {len(recipes)} recipes...")

# with open("./data/recipes_consolidated.json", "w") as f:
#     json.dump({"recipes": recipes}, f)



