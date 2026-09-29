from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


class QdrantStore:

    def __init__(
        self,
        client: QdrantClient | None = None,
        collection_name: str = "uipath_errors",
    ):
        if client is None:
            self.client = QdrantClient(
                path="data/qdrant"
            )
            self._owns_client = True
        else:
            self.client = client
            self._owns_client = False

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

    def build_text(self, error):

        return (
            f"Process: {error.process_name}\n"
            f"Workflow: {error.workflow}\n"
            f"Robot: {error.robot}\n"
            f"Environment: {error.environment}\n"
            f"Status: {error.status}\n"
            f"Error code: {error.error_code}\n"
            f"Category: {error.error_category}\n"
            f"Severity: {error.severity}\n"
            f"Message: {error.error_message}"
        )

    def upsert_error(
        self,
        error,
        vector,
    ):

        point = PointStruct(
            id=error.log_id,
            vector=vector,
            payload={
                "log_id": error.log_id,
                "timestamp": error.timestamp,
                "job_key": error.job_key,
                "process_name": error.process_name,
                "workflow": error.workflow,
                "robot": error.robot,
                "environment": error.environment,
                "status": error.status,
                "error_code": error.error_code,
                "error_category": error.error_category,
                "severity": error.severity,
                "error_message": error.error_message,
                "retry_count": error.retry_count,
                "queue_item": error.queue_item,
            },
        )

        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

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

    def count_errors(self):

        collection_info = (
            self.client.get_collection(
                collection_name=self.collection_name
            )
        )

        return collection_info.points_count

    def close(self):

        if self._owns_client:
            self.client.close()