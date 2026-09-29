from uuid import uuid5, NAMESPACE_URL

from uipath_agent.embeddings.embedder import ErrorEmbedder
from uipath_agent.knowledge_loader import MarkdownKnowledgeLoader
from uipath_agent.vectorstore.knowledge_store import KnowledgeStore


class KnowledgeIngestor:

    def __init__(
        self,
        loader: MarkdownKnowledgeLoader,
        embedder: ErrorEmbedder,
        store: KnowledgeStore,
    ):
        self.loader = loader
        self.embedder = embedder
        self.store = store

    def ingest(self) -> int:

        documents = self.loader.load_documents()

        total_chunks = 0

        for document in documents:

            sections = (
                self.loader.split_into_sections(
                    document["content"]
                )
            )

            for section in sections:

                chunks = (
                    self.loader.split_large_section(
                        section
                    )
                )

                for index, chunk in enumerate(
                    chunks
                ):

                    vector = self.embedder.embed(
                        chunk["content"]
                    )

                    point_id = str(
                        uuid5(
                            NAMESPACE_URL,
                            (
                                f"{document['source']}:"
                                f"{section['heading']}:"
                                f"{index}"
                            ),
                        )
                    )

                    self.store.upsert_chunk(
                        point_id=point_id,
                        vector=vector,
                        source=document["source"],
                        heading=chunk["heading"],
                        content=chunk["content"],
                    )

                    total_chunks += 1

        return total_chunks
if __name__ == "__main__":

    loader = MarkdownKnowledgeLoader(
        "data/knowledge"
    )

    embedder = ErrorEmbedder()

    store = KnowledgeStore()

    store.create_collection()

    ingestor = KnowledgeIngestor(
        loader=loader,
        embedder=embedder,
        store=store,
    )

    total_chunks = ingestor.ingest()

    print(
        f"Ingested chunks: {total_chunks}"
    )

    print(
        f"Qdrant chunk count: "
        f"{store.count_chunks()}"
    )

    store.close()