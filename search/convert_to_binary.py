import pickle
import numpy as np
from sentence_transformers.quantization import quantize_embeddings

print("Loading embeddings...")
with open('recipe_embeddings.pickle', 'rb') as handle:
    recipe_embeddings = pickle.load(handle)

print("Converting embeddings to binary...")
int8_embeddings = quantize_embeddings(
    recipe_embeddings,
    precision="binary"
)

print("Saving binary embeddings...")
with open('recipe_embeddings_binary.pickle', 'wb') as handle:
    pickle.dump(int8_embeddings, handle, protocol=pickle.HIGHEST_PROTOCOL)