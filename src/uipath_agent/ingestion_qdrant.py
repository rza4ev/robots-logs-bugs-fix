from uipath_agent.log_reader import read_error_logs
from uipath_agent.vectorstore.qdrant_store import QdrantStore
from uipath_agent.embeddings.embedder import ErrorEmbedder

file_path = "data/uipath_error_logs.xlsx"

errors = read_error_logs(file_path)

embedder=ErrorEmbedder()
store=QdrantStore()
try:
    store.create_collection()

    for error in errors:

        text = store.build_text(error)

        vector = embedder.embed(text)

        store.upsert_error(
            error=error,
            vector=vector,
        )

    print(f"{len(errors)} errors inserted into Qdrant")

finally:
    store.close()