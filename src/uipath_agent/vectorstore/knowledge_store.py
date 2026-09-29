from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


class KnowledgeStore:

    def __init__(
        self,
        client,
        collection_name: str = "uipath_knowledge",
    ):
        self.client = client
        self.collection_name = collection_name

    def create_collection(self):

        collections = (
            self.client
            .get_collections()
            .collections
        )

        exists = any(
            collection.name
            == self.collection_name
            for collection in collections
        )

        if not exists:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE,
                ),
            )

    def upsert_chunk(
        self,
        point_id,
        vector,
        source: str,
        heading: str,
        content: str,
    ):

        point = PointStruct(
            id=point_id,
            vector=vector,
            payload={
                "source": source,
                "heading": heading,
                "content": content,
            },
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

    def count_chunks(self):

        collection_info = (
            self.client.get_collection(
                collection_name=self.collection_name
            )
        )

        return collection_info.points_count

    def search_similar(
        self,
        vector,
        limit: int = 5,
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            limit=limit,
        )

        return results.points