import requests

from uipath_agent.models.analysis import ErrorAnalysis


class ErrorAnalyzer:

    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-5.6-luna",
    ):
        self.api_key = api_key
        self.model = model

    def analyze(
        self,
        context: str,
    ) -> ErrorAnalysis:

        system_prompt = """
You are a UiPath error analysis assistant.

Analyze the provided UiPath job error using:
1. The current error information.
2. Similar historical errors.
3. Relevant UiPath knowledge.

Do not invent facts that are not supported by the provided context.

Identify the most likely root cause, explain the reasoning, provide a practical solution, and suggest prevention steps.

Return the result using the required JSON schema.
"""

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": (
                    f"Bearer {self.api_key}"
                ),
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": context,
                    },
                ],
                "reasoning": {
                    "enabled": True,
                },
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "error_analysis",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "root_cause": {
                                    "type": "string"
                                },
                                "explanation": {
                                    "type": "string"
                                },
                                "recommended_solution": {
                                    "type": "string"
                                },
                                "prevention": {
                                    "type": "string"
                                },
                                "confidence": {
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1,
                                },
                            },
                            "required": [
                                "root_cause",
                                "explanation",
                                "recommended_solution",
                                "prevention",
                                "confidence",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "temperature": 0,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        content = data[
            "choices"
        ][0]["message"]["content"]

        return ErrorAnalysis.model_validate_json(
            content
        )