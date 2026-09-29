from uipath_agent.embeddings.embedder import ErrorEmbedder
from uipath_agent.vectorstore.qdrant_store import QdrantStore


class ErrorRetriever:

    def __init__(
        self,
        embedder: ErrorEmbedder,
        store: QdrantStore,
        similarity_threshold: float = 0.20,
    ):
        self.embedder = embedder
        self.store = store
        self.similarity_threshold = similarity_threshold

    def retrieve(
        self,
        error_text: str,
        limit: int = 5,
    ):

        vector = self.embedder.embed(
            error_text
        )

        results = self.store.search_similar(
            vector=vector,
            limit=limit,
        )

        relevant_results = [
            result
            for result in results
            if result.score
            >= self.similarity_threshold
        ]

        return relevant_results