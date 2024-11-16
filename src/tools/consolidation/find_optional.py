import json
from tqdm import tqdm
from collections import Counter


print("Loading json...")
with open("./data/recipes_validated.json", "r") as f:
    recipes = json.load(f)["recipes"]

cnt = Counter()

print("Grabbing keys...")
for item in tqdm(recipes):
    for key in item.keys():
        cnt[key] += 1

# Show all optional keys
optional = set()
non_optional = set()
for key in cnt.keys():
    if cnt[key] != len(recipes):
        optional.add(key)
    else:
        non_optional.add(key)

print(cnt)

print(f"Optional: {optional}")
print(f"Non-Optional: {non_optional}")
