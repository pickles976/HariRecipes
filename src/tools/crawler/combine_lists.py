import os
import csv

DIR = "./data/recipe_lists"

files = os.listdir(DIR)

recipes = []

for file in files:
    filepath = os.path.join(DIR, file)
    with open(filepath, "r") as f:
        reader = csv.reader(f, delimiter='\n')
        for row in reader:
            if len(row) == 1:
                # Filtering out some duplicate URLs
                # url = row[0]
                # if "respond" in url or "print" in url:
                #     continue
                recipes.append(row[0])

with open(f"./data/all_recipes.csv", "w") as f:
    writer = csv.writer(f, delimiter='\n')
    writer.writerows([recipes])