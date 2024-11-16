echo "Downloading full-sized embedding vectors..."
curl -o ./data/recipe_embeddings.pickle "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings.pickle"

echo "Downloading full-sized embedding vectors..."
curl -o ./data/recipe_embeddings_binary.pickle "https://github.com/pickles976/HariRecipes/releases/download/data/recipe_embeddings_binary.pickle"

echo "Downloading sqlite file..."
curl -o ./data/recipes.sqlite.gz "https://github.com/pickles976/HariRecipes/releases/download/data/recipes.sqlite.gz"

