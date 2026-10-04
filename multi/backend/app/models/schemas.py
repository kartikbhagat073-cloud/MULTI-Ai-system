from pydantic import BaseModel, Field
from typing import List, Optional


class CompareRequest(BaseModel):
    prompt: str = Field(min_length=1)
    models: List[str] = Field(min_length=2)


class ModelResponse(BaseModel):
    model: str
    output: Optional[str] = None
    latency_ms: Optional[int] = None
    error: Optional[str] = None


class CompareResponse(BaseModel):
    prompt: str
    responses: List[ModelResponse]
