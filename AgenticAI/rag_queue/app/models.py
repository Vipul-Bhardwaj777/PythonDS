from pydantic import BaseModel, Field, field_validator

MAX_QUERY_LENGTH = 1000


class ChatRequest(BaseModel):
    query: str = Field(..., description="User question.")

    @field_validator("query")
    @classmethod
    def normalize_query(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Query must not be empty.")
        if len(value) > MAX_QUERY_LENGTH:
            raise ValueError(f"Query must be at most {MAX_QUERY_LENGTH} characters.")
        return value
