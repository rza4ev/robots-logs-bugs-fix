from pydantic import BaseModel


class UiPathError(BaseModel):
    log_id: int
    timestamp: str
    job_key: str
    process_name: str
    workflow: str
    robot: str
    environment: str
    status: str
    error_code: str
    error_category: str
    severity: str
    error_message: str
    retry_count: int
    queue_item: str | None = None