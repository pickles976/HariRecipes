import torch
from torch import tensor
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import quantize_embeddings, semantic_search_faiss

from src.tools.recipe_data import RecipeData



class VectorSearch:

    recipes: list[RecipeData]
    embeddings: tensor
    model:SentenceTransformer

    def __init__(self, recipes: list[RecipeData], embeddings: tensor, model:SentenceTransformer):
        self.recipes = recipes
        self.embeddings = embeddings
        self.model = model

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        raise NotImplementedError()

    def query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        return self._query(query_string, top_k)


class FloatVectorSearch(VectorSearch):

    def __init__(self, recipes: list[RecipeData], embeddings: tensor, model:SentenceTransformer):
        super().__init__(recipes, embeddings, model)

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:

        query_embedding = self.model.encode(query_string)

        similarity_scores = self.model.similarity(query_embedding, self.embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=top_k)

        data = []
        for score, idx in zip(scores, indices):
            data.append((self.recipes[idx], score))
        return data

    
class BinaryVectorSearch(VectorSearch):

    binary_embeddings: tensor
    corpus_precision: str

    def __init__(self, recipes: list[RecipeData], embeddings: tensor, model:SentenceTransformer):
        super().__init__(recipes, embeddings, model)
        self.corpus_precision = "ubinary"
        self.binary_embeddings = quantize_embeddings(
            self.embeddings, 
            precision=self.corpus_precision
        )
        self.corpus_index = None

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        
        query_embeddings = model.encode([query_string], normalize_embeddings=True)

        # 8. Perform semantic search using FAISS
        results, search_time, self.corpus_index = semantic_search_faiss(
            query_embeddings,
            corpus_index=self.corpus_index,
            corpus_embeddings=self.binary_embeddings if self.corpus_index is None else None,
            corpus_precision=self.corpus_precision,
            top_k=20,
            calibration_embeddings=self.embeddings,
            rescore=self.corpus_precision != "float32",
            rescore_multiplier=4,
            exact=True,
            output_index=True,
        )

        data = []
        for entry in results[0]:
            data.append((self.recipes[entry["corpus_id"]], entry["score"]))
        return data

if __name__ == "__main__":

    import json
    import time
    import pickle

    print("Loading recipes...")
    with open("./data/recipes_validated.json", "r") as f:
        raw_data = json.load(f)["recipes"]
    recipes = [RecipeData(**item) for item in raw_data]
    print(f"Loaded {len(recipes)} recipes!")

    with open('./data/recipe_embeddings.pickle', 'rb') as handle:
        embeddings = pickle.load(handle)

    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    # searcher = FloatVectorSearch(recipes, embeddings, model)
    searcher = BinaryVectorSearch(recipes, embeddings, model)
    
    while True:
        query = input("Enter a query: ")
        start = time.time()
        items = searcher.query(query)
        for recipe, score in items:
            print(f"{recipe.title} {score:.4f}")
        print(f"Query ran in: {time.time() - start}s")