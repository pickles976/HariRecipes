import re
import json
import time
import requests
from requests import Response

CHECKPOINT = 1000
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

def save_json(items: list[dict]):
    with open(f"./data/cleaned/{len(items)}.json", "w") as f:
        json.dump({
            "recipes": items
        }, f)

print("Loading recipes...")
filepath = "./data/recipes_validated.json"
# filepath = "./test.json"
with open(filepath, "r") as f:
    all_recipes = json.load(f)["recipes"]

print("Starting inference...")
items = []
for i, recipe in enumerate(all_recipes):

    print(recipe["title"])
    start = time.time()
    res = requests.post(url=url, json=format(recipe), headers=headers)
    if res.status_code != 200:
        raise Exception(f"Error: {res.status_code} {res.content}")
    
    valid = is_valid(response=res)
    print(f"{str(valid).upper()} {time.time() - start:.2f}")
    if valid:
        items.append(recipe)
    
    if i % CHECKPOINT == 0:
        save_json(items)

save_json(items)
