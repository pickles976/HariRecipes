import os
import csv

files = os.listdir("./recipe_lists")

for file in files:
    with open(file, "r") as f:
        reader = csv.reader(f, delimiter='\n')
        
        lines = reader.readlines()
        print(len(lines))