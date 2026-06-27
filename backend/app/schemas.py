from typing import List, Optional
from pydantic import BaseModel, Field


class Citation(BaseModel):
    chunk_id: str
    content: str
    page: Optional[int] = None
    source: Optional[str] = None
    score: float


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    document_id: Optional[str] = None
    top_k: Optional[int] = None


class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    usage: dict
    estimated_cost_usd: float


class IngestResponse(BaseModel):
    document_id: str
    chunks_created: int
    filename: str
