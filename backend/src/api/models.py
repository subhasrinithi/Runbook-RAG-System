from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class IngestRequest(BaseModel):
    directory_path: str = Field(..., description="Path to directory containing runbook MD files")


class IngestResponse(BaseModel):
    status: str
    documents_processed: int
    chunks_created: int
    message: str


class QueryRequest(BaseModel):
    incident_description: str = Field(..., description="Description of the incident")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of results to return")


class SearchResult(BaseModel):
    content: str
    metadata: Dict[str, Any]
    chunk_id: str
    relevance_score: float


class QueryResponse(BaseModel):
    results: List[SearchResult]


class PlaybookStep(BaseModel):
    step_number: int
    action: str
    command: Optional[str] = None
    expected_outcome: str
    verification: Optional[str] = None


class Playbook(BaseModel):
    title: str
    summary: str
    steps: List[PlaybookStep]
    estimated_time: str
    risk_level: str


class GeneratePlaybookRequest(BaseModel):
    incident_description: str = Field(..., description="Description of the incident")
    context: Optional[List[str]] = Field(default=None, description="Pre-retrieved context")
    include_verification: bool = Field(default=True, description="Include verification steps")


class GeneratePlaybookResponse(BaseModel):
    playbook: Playbook


class HealthResponse(BaseModel):
    status: str
    timestamp: str