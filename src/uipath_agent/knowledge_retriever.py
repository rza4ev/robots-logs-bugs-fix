from uipath_agent.embeddings.embedder import ErrorEmbedder
from uipath_agent.vectorstore.knowledge_store import KnowledgeStore


class KnowledgeRetriever:

    def __init__(
        self,
        embedder: ErrorEmbedder,
        store: KnowledgeStore,
    ):
        self.embedder = embedder
        self.store = store

    def retrieve(
        self,
        query: str,
        limit: int = 2,
    ):

        vector = self.embedder.embed(query)

        results = self.store.search_similar(
            vector=vector,
            limit=limit,
        )

        return results
if __name__ == "__main__":

    embedder = ErrorEmbedder()

    store = KnowledgeStore()

    retriever = KnowledgeRetriever(
        embedder=embedder,
        store=store,
    )

    query = (
        "The Confirm button cannot be found "
        "on the screen."
    )

    results = retriever.retrieve(
        query=query,
        limit=2,
    )

    print(
        f"Retrieved knowledge chunks: "
        f"{len(results)}"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        print(
            f"\nResult {index}"
        )

        print(
            f"Score: {result.score:.3f}"
        )

        print(
            f"Source: "
            f"{result.payload.get('source')}"
        )

        print(
            f"Heading: "
            f"{result.payload.get('heading')}"
        )

        print(
            f"Content:\n"
            f"{result.payload.get('content')}"
        )

    store.close()