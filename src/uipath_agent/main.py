from qdrant_client import QdrantClient

from uipath_agent.analyzer import ErrorAnalyzer
from uipath_agent.config import OPENROUTER_API_KEY
from uipath_agent.context_builder import ContextBuilder
from uipath_agent.embeddings.embedder import ErrorEmbedder
from uipath_agent.knowledge_retriever import KnowledgeRetriever
from uipath_agent.retriever import ErrorRetriever
from uipath_agent.vectorstore.knowledge_store import KnowledgeStore
from uipath_agent.vectorstore.qdrant_store import QdrantStore


def main():
    # Create one shared Qdrant client.
    client = QdrantClient(path="data/qdrant")

    error_store = QdrantStore(
        client=client,
        collection_name="uipath_errors",
    )

    knowledge_store = KnowledgeStore(
        client=client,
        collection_name="uipath_knowledge",
    )

    embedder = ErrorEmbedder()

    error_retriever = ErrorRetriever(
        embedder=embedder,
        store=error_store,
        similarity_threshold=0.20,
    )

    knowledge_retriever = KnowledgeRetriever(
        embedder=embedder,
        store=knowledge_store,
    )

    context_builder = ContextBuilder()

    analyzer = ErrorAnalyzer(
        api_key=OPENROUTER_API_KEY,
    )

    try:
        query_text = (
            "America is capital of US"
        )

        print("\nNew UiPath Error:")
        print(query_text)

        # Retrieve similar historical errors.
        historical_errors = error_retriever.retrieve(
            error_text=query_text,
            limit=5,
        )

        if not historical_errors:
            print(
                "\nNo relevant historical errors were found. "
                "LLM analysis was skipped."
            )
            return

        # Retrieve relevant UiPath knowledge.
        knowledge_chunks = knowledge_retriever.retrieve(
            query=query_text,
            limit=5,
        )

        print("\nKnowledge Used by the LLM:")

        for index, result in enumerate(
            knowledge_chunks,
            start=1,
        ):
            payload = result.payload

            print(f"\n--- Knowledge Chunk {index} ---")
            print(f"Similarity Score: {result.score:.3f}")
            print(f"Source: {payload.get('source')}")
            print(f"Section: {payload.get('heading')}")
            print("\nContent:")
            print(payload.get("content"))

        # Build the context that will be sent to the LLM.
        context = context_builder.build(
            query=query_text,
            historical_errors=historical_errors,
            knowledge_chunks=knowledge_chunks,
        )

        # Send the context to the LLM.
        analysis = analyzer.analyze(context)

        print("\n========== LLM ANALYSIS ==========")

        print("\nRoot Cause:")
        print(analysis.root_cause)

        print("\nExplanation:")
        print(analysis.explanation)

        print("\nRecommended Solution:")
        print(analysis.recommended_solution)

        print("\nPrevention:")
        print(analysis.prevention)

        print("\nConfidence:")
        print(analysis.confidence)

        print("\n===================================")

    finally:
        client.close()


if __name__ == "__main__":
    main()