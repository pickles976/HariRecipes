import json
import pickle
from recipe_data import RecipeData
import torch
from sentence_transformers import SentenceTransformer
import time

print("Loading recipes...")
with open("./recipes_validated.json", "r") as f:
    raw_data = json.load(f)["recipes"]
recipes = [RecipeData(**item) for item in raw_data]
print(f"Loaded {len(recipes)} recipes!")

with open('recipe_embeddings.pickle', 'rb') as handle:
    recipe_embeddings = pickle.load(handle)

print("Loading Sentence Transformer...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

query = ""
while query != "exit":
    query = input("Enter a search query for a recipe: ")

    start = time.time()

    top_k = min(20, len(recipes))
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    similarity_scores = embedder.similarity(query_embedding, recipe_embeddings)[0]
    scores, indices = torch.topk(similarity_scores, k=top_k)

    print("\nQuery:", query)
    print("Top 20 most similar sentences in corpus:")

    for score, idx in zip(scores, indices):
        print(recipes[idx].model_dump()["title"], f"(Score: {score:.4f})")

    print(f"Search took {time.time() - start}s")
