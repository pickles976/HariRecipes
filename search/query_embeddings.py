# print("Loading recipes...")
# with open("./recipes_validated.json", "r") as f:
#     raw_data = json.load(f)["recipes"]
# recipes = [RecipeData(**item) for item in raw_data]
# print(f"Loaded {len(recipes)} recipes!")

# print("Running queries...")

# # Query sentences:
# queries = [
#     "Gay Pasta",
#     "Dirt Salad",
#     "Halo 3"
# ]

# # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
# top_k = min(10, len(corpus))
# for query in queries:
#     query_embedding = embedder.encode(query, convert_to_tensor=True)

#     # We use cosine-similarity and torch.topk to find the highest 5 scores
#     similarity_scores = embedder.similarity(query_embedding, corpus_embeddings)[0]
#     scores, indices = torch.topk(similarity_scores, k=top_k)

#     print("\nQuery:", query)
#     print("Top 10 most similar sentences in corpus:")

#     for score, idx in zip(scores, indices):
#         print(corpus[idx], f"(Score: {score:.4f})")

#     """
#     # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
#     hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=10)
#     hits = hits[0]      #Get the hits for the first query
#     for hit in hits:
#         print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
#     """