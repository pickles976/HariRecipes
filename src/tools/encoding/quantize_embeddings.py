import pickle
from sentence_transformers.quantization import quantize_embeddings
from src.common import EMBEDDINGS_FILENAME, BINARY_EMBEDDINGS_FILENAME

print("Loading embeddings...")
with open(EMBEDDINGS_FILENAME, "rb") as handle:
    embeddings = pickle.load(handle)

print("Quantizing embeddings...")
binary_embeddings = quantize_embeddings(embeddings, precision="ubinary")

print("Saving embeddings...")
with open(BINARY_EMBEDDINGS_FILENAME, "wb") as handle:
    pickle.dump(binary_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)
