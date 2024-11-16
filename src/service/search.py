from src.recipe_data import RecipeData
from src.service.db import RecipeRepo
from src.common import EMBEDDINGS_FILENAME

import torch
from torch import tensor
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import quantize_embeddings, semantic_search_faiss


class VectorSearch:

    recipe_repo: RecipeRepo
    embeddings: tensor
    model:SentenceTransformer

    def __init__(self, recipe_repo: RecipeRepo, embeddings: tensor, model:SentenceTransformer):
        self.recipe_repo = recipe_repo
        self.embeddings = embeddings
        self.model = model

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        raise NotImplementedError()

    def query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        return self._query(query_string, top_k)


class FloatVectorSearch(VectorSearch):

    def __init__(self, recipe_repo: RecipeRepo, embeddings: tensor, model:SentenceTransformer):
        super().__init__(recipe_repo, embeddings, model)

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:

        query_embedding = self.model.encode(query_string)

        similarity_scores = self.model.similarity(query_embedding, self.embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=top_k)

        recipes = self.recipe_repo.list_recipes(indices)

        data = []
        for score, recipe in zip(scores, recipes):
            data.append((recipe, score))
        return data

    
class BinaryVectorSearch(VectorSearch):

    binary_embeddings: tensor
    corpus_precision: str

    def __init__(self, recipe_repo: RecipeRepo, embeddings: tensor, model:SentenceTransformer):
        super().__init__(recipe_repo, embeddings, model)
        self.corpus_precision = "ubinary"
        self.binary_embeddings = quantize_embeddings(
            self.embeddings, 
            precision=self.corpus_precision
        )
        self.corpus_index = None

    def _query(self, query_string: str, top_k:int = 20) -> list[tuple[RecipeData, float]]:
        
        query_embeddings = model.encode([query_string], normalize_embeddings=True)

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

        indices = [entry["corpus_id"] for entry in results[0]]
        scores = [entry["score"] for entry in results[0]]
        recipes = self.recipe_repo.list_recipes(indices)

        data = []
        for score, recipe in zip(scores, recipes):
            data.append((recipe, score))
        return data

if __name__ == "__main__":

    import time
    import pickle
    from src.service.db import RecipeRepoJSON, RecipeRepoSQLite

    try:
        recipe_repo = RecipeRepoSQLite()
    except Exception as e:
        print(f"Failed to load sqlite with exception: {e}")
        print("Loading recipes from json. This will consume more memory...")
        recipe_repo = RecipeRepoJSON()

    with open(EMBEDDINGS_FILENAME, 'rb') as handle:
        embeddings = pickle.load(handle)

    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    # searcher = FloatVectorSearch(recipes, embeddings, model)
    searcher = BinaryVectorSearch(recipe_repo, embeddings, model)
    
    while True:
        query = input("Enter a query: ")
        start = time.time()
        items = searcher.query(query)
        for recipe, score in items:
            print(f"{recipe.title} {score:.4f}")
        print(f"Query ran in: {time.time() - start}s")