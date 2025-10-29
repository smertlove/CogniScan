import faiss
import numpy as np

from .encoder import Encoder


class RamIndex:

    def __init__(
        self,
    ):
        self.index = None
        self.texts = []
        self.meta = []

    def build_index(self, texts, meta, encoder: Encoder):
        embeddings = encoder.encode(texts)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.normalize(embeddings)
        self.index.add(embeddings.astype(np.float32))
        self.texts = texts
        self.meta = meta

    def normalize(self, x):
        return faiss.normalize_L2(x)

    def search(self, query: str, encoder: Encoder, k=3):

        query_embedding = encoder.encode([query])
        self.normalize(query_embedding)

        distances, indices = self.index.search(query_embedding.astype(np.float32), k)

        results = []
        for score, i in zip(distances[0], indices[0]):
            results.append({"score": score, "text": self.texts[i], "meta": self.meta[i]})

        return results
