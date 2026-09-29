from pydantic import BaseModel, Field


class ErrorAnalysis(BaseModel):
    root_cause: str
    explanation: str
    recommended_solution: str
    prevention: str
    confidence: float = Field( ge=0.0, le=1.0)