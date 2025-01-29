from abc import ABC
from src.recipe_data import RecipeData
from src.service.db import AbstractRecipeRepo
from src.common import load_binary_embeddings, load_full_embeddings  # noqa
import torch
from torch import tensor
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import (
    quantize_embeddings,
    semantic_search_faiss,
)


class BaseVectorSearch(ABC):
    recipe_repo: AbstractRecipeRepo
    embeddings: tensor
    model: SentenceTransformer

    def __init__(
        self,
        recipe_repo: AbstractRecipeRepo,
        embeddings: tensor,
        model: SentenceTransformer,
    ):
        self.recipe_repo = recipe_repo
        self.embeddings = embeddings
        self.model = model

    def _query(
        self, query_string: str, top_k: int = 50
    ) -> list[tuple[RecipeData, int, float]]:
        raise NotImplementedError()

    def query(
        self, query_string: str, top_k: int = 50
    ) -> list[tuple[RecipeData, int, float]]:
        return self._query(query_string, top_k)


class FloatVectorSearch(BaseVectorSearch):
    def __init__(
        self,
        recipe_repo: AbstractRecipeRepo,
        embeddings: tensor,
        model: SentenceTransformer,
    ):
        super().__init__(recipe_repo, embeddings, model)

    def _query(
        self, query_string: str, top_k: int = 50
    ) -> list[tuple[RecipeData, int, float]]:
        query_embedding = self.model.encode(query_string)

        similarity_scores = self.model.similarity(query_embedding, self.embeddings)[0]
        scores, indices = torch.topk(similarity_scores, k=top_k)

        recipes = self.recipe_repo.list_recipes(indices)

        data = []
        for index, score in zip(indices, scores):
            recipe = recipes[index]
            data.append((recipe, index, score))
        return data


class BinaryVectorSearch(BaseVectorSearch):
    has_float_embeddings: bool
    binary_embeddings: tensor
    corpus_precision: str

    def __init__(
        self,
        recipe_repo: AbstractRecipeRepo,
        embeddings: tensor,
        model: SentenceTransformer,
    ):
        super().__init__(recipe_repo, embeddings, model)

        self.corpus_index = None
        self.corpus_precision = "ubinary"

        # Check if we provided full-precision embeddings
        self.has_float_embeddings = self.embeddings.dtype == torch.float32
        print(f"Loaded embeddings with precision level: {self.embeddings.dtype}")

        if self.has_float_embeddings:
            self.binary_embeddings = quantize_embeddings(
                self.embeddings, precision=self.corpus_precision
            )
        else:
            self.binary_embeddings = embeddings

    def _query(
        self, query_string: str, top_k: int = 50
    ) -> list[tuple[RecipeData, int, float]]:
        query_embeddings = self.model.encode([query_string], normalize_embeddings=True)

        if self.has_float_embeddings:
            results, search_time, self.corpus_index = semantic_search_faiss(
                query_embeddings,
                corpus_index=self.corpus_index,
                corpus_embeddings=self.binary_embeddings
                if self.corpus_index is None
                else None,
                corpus_precision=self.corpus_precision,
                top_k=top_k,
                calibration_embeddings=self.embeddings,
                rescore=self.corpus_precision != "float32",
                rescore_multiplier=4,
                exact=True,
                output_index=True,
            )
        else:
            results, search_time, self.corpus_index = semantic_search_faiss(
                query_embeddings,
                corpus_index=self.corpus_index,
                corpus_embeddings=self.binary_embeddings
                if self.corpus_index is None
                else None,
                corpus_precision=self.corpus_precision,
                top_k=top_k,
                exact=True,
                output_index=True,
            )

        indices = [entry["corpus_id"] for entry in results[0]]
        scores = [entry["score"] for entry in results[0]]
        recipes = self.recipe_repo.list_recipes(indices)

        data = []
        for index, score in zip(indices, scores):
            recipe = recipes[index]
            data.append((recipe, index, score))
        return data


if __name__ == "__main__":
    import time
    from src.service.db import RecipeRepoJSON, RecipeRepoSQLite

    try:
        recipe_repo = RecipeRepoSQLite()
    except Exception as e:
        print(f"Failed to load sqlite with exception: {e}")
        print("Loading recipes from json. This will consume more memory...")
        recipe_repo = RecipeRepoJSON()

    # embeddings = load_full_embeddings()
    embeddings = load_binary_embeddings()

    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    # searcher = FloatVectorSearch(recipes, embeddings, model)
    searcher = BinaryVectorSearch(recipe_repo, embeddings, model)

    while True:
        query = input("Enter a query: ")
        start = time.time()
        items = searcher.query(query)
        for recipe, index, score in items:
            print(f"{recipe.title} {score:.4f}")
        print(f"Query ran in: {time.time() - start}s")
