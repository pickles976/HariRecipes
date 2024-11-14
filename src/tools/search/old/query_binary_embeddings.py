# https://github.com/UKPLab/sentence-transformers/blob/master/examples/applications/embedding-quantization/semantic_search_faiss.py
import json
from tools.recipe_data import RecipeData
import time
import pickle

from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import quantize_embeddings, semantic_search_faiss

print("Loading recipes...")
with open("./recipes_validated.json", "r") as f:
    raw_data = json.load(f)["recipes"]
corpus = [RecipeData(**item) for item in raw_data]
print(f"Loaded {len(corpus)} recipes!")

model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

# 4. Choose a target precision for the corpus embeddings
corpus_precision = "ubinary"
# Valid options are: "float32", "uint8", "int8", "ubinary", and "binary"
# But FAISS only supports "float32", "uint8", and "ubinary"

# 5. Encode the corpus
with open('recipe_embeddings_binary.pickle', 'rb') as handle:
    full_corpus_embeddings = pickle.load(handle)
corpus_embeddings = quantize_embeddings(full_corpus_embeddings, precision=corpus_precision)

# Initially, we don't have a FAISS index yet, we can use semantic_search_faiss to create it
corpus_index = None
while True:
    query = input("Search for a recipe: ")
    queries = [query]
    start_time = time.time()
    query_embeddings = model.encode(queries, normalize_embeddings=True)
    print(f"Encoding time: {time.time() - start_time:.6f} seconds")

    # 8. Perform semantic search using FAISS
    results, search_time, corpus_index = semantic_search_faiss(
        query_embeddings,
        corpus_index=corpus_index,
        corpus_embeddings=corpus_embeddings if corpus_index is None else None,
        corpus_precision=corpus_precision,
        top_k=20,
        calibration_embeddings=full_corpus_embeddings,
        rescore=corpus_precision != "float32",
        rescore_multiplier=4,
        exact=True,
        output_index=True,
    )

    # 9. Output the results
    print("Precision:", corpus_precision)
    print(f"Search time: {search_time:.6f} seconds")
    for query, result in zip(queries, results):
        print(f"Query: {query}")
        for entry in result:
            print(corpus[entry['corpus_id']].model_dump()["title"], f"(Score: {entry['score']:.4f})")
        print("")

    print(f"Search took {time.time() - start_time}")