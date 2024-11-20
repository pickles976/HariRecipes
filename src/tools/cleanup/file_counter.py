# Make csv lists of all filepaths, organized by extension
import os
from tqdm import tqdm
import shutil
import pathlib

all_files = {
    "txt": [],
    "html": []
}

print("Walking dirs...")
for root, dir, files in os.walk("./data/recipe_archive"):
    for file in files:
        suffix = pathlib.Path(file).suffix.replace(".", "")
        if suffix in all_files:
            all_files[suffix].append(os.path.join(root, file))

print(all_files.keys())

# copy files
for key in all_files:
    print(f"Copying all {key} files")
    dir = f"./data/archive/{key}"
    os.makedirs(dir, exist_ok=True)
    for file in tqdm(all_files[key]):
        dest = os.path.join(dir, os.path.basename(file))
        shutil.copy(file, dest)