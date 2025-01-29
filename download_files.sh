#!/bin/bash
echo "Downloading full-sized embedding vectors..."
curl -L "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings.pickle" > ./data/recipe_embeddings.pickle

echo "Downloading Binarized embedding vectors..."
curl -L  "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings_binary.pickle" > ./data/recipe_embeddings_binary.pickle

echo "Downloading sqlite file..."
curl -L "https://github.com/pickles976/HariRecipes/releases/download/data/recipes.sqlite.gz" > ./data/recipes.sqlite.gz

echo "Unzipping sqlite..."
gzip -d -k ./data/recipes.sqlite.gz

