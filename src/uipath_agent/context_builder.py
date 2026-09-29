class ContextBuilder:

    def build(
        self,
        query: str,
        historical_errors,
        knowledge_chunks,
    ) -> str:

        context = (
            "New UiPath Error:\n"
            f"{query}\n\n"
        )

        context += (
            "Similar Historical Errors:\n"
        )

        for index, result in enumerate(
            historical_errors,
            start=1,
        ):
            payload = result.payload

            context += (
                f"\nHistorical Error {index}\n"
                f"Similarity Score: "
                f"{result.score:.3f}\n"
                f"Log ID: "
                f"{payload.get('log_id')}\n"
                f"Timestamp: "
                f"{payload.get('timestamp')}\n"
                f"Job Key: "
                f"{payload.get('job_key')}\n"
                f"Process: "
                f"{payload.get('process_name')}\n"
                f"Workflow: "
                f"{payload.get('workflow')}\n"
                f"Robot: "
                f"{payload.get('robot')}\n"
                f"Environment: "
                f"{payload.get('environment')}\n"
                f"Status: "
                f"{payload.get('status')}\n"
                f"Error Code: "
                f"{payload.get('error_code')}\n"
                f"Category: "
                f"{payload.get('error_category')}\n"
                f"Severity: "
                f"{payload.get('severity')}\n"
                f"Error Message: "
                f"{payload.get('error_message')}\n"
                f"Retry Count: "
                f"{payload.get('retry_count')}\n"
                f"Queue Item: "
                f"{payload.get('queue_item')}\n"
            )

        context += (
            "\n\nRelevant UiPath Knowledge:\n"
        )

        for index, result in enumerate(
            knowledge_chunks,
            start=1,
        ):
            payload = result.payload

            context += (
                f"\nKnowledge Chunk {index}\n"
                f"Similarity Score: "
                f"{result.score:.3f}\n"
                f"Source: "
                f"{payload.get('source')}\n"
                f"Section: "
                f"{payload.get('heading')}\n"
                f"Content:\n"
                f"{payload.get('content')}\n"
            )

        return context