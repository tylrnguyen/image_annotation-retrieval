import faiss
import numpy as np


class FaissVectorIndex:
    def __init__(self, dimension=128):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.image_ids = []

    def add_embedding(self, image_id, embedding):
        vector = np.array([embedding], dtype="float32")

        if vector.shape[1] != self.dimension:
            raise ValueError(
                f"Expected embedding dimension {self.dimension}, got {vector.shape[1]}"
            )

        self.index.add(vector)
        self.image_ids.append(image_id)

    def search(self, query_embedding, top_k=3):
        if self.index.ntotal == 0:
            return []

        vector = np.array([query_embedding], dtype="float32")

        if vector.shape[1] != self.dimension:
            raise ValueError(
                f"Expected query dimension {self.dimension}, got {vector.shape[1]}"
            )

        distances, indices = self.index.search(vector, top_k)

        results = []

        for distance, index_id in zip(distances[0], indices[0]):
            if index_id == -1:
                continue

            results.append({
                "image_id": self.image_ids[index_id],
                "distance": float(distance)
            })

        return results

    def count(self):
        return self.index.ntotal