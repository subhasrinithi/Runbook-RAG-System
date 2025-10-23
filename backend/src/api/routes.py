from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
import logging

from src.api.models import (
    IngestRequest, IngestResponse,
    QueryRequest, QueryResponse,
    GeneratePlaybookRequest, GeneratePlaybookResponse,
    HealthResponse
)
from src.modules.document_ingestion.service import DocumentIngestionService
from src.modules.vector_search.service import VectorSearchService
from src.modules.playbook_generator.service import PlaybookGeneratorService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat()
    )


@router.post("/ingest", response_model=IngestResponse)
async def ingest_documents(
    request: IngestRequest,
    api_request: Request
):
    """Ingest and index runbook documents"""
    try:
        vector_store = api_request.app.state.vector_store
        service = DocumentIngestionService(vector_store)
        
        result = await service.ingest_directory(request.directory_path)
        
        return IngestResponse(
            status="success",
            documents_processed=result["documents_processed"],
            chunks_created=result["chunks_created"],
            message=f"Successfully processed {result['documents_processed']} documents"
        )
    except Exception as e:
        logger.error(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query", response_model=QueryResponse)
async def query_runbooks(
    request: QueryRequest,
    api_request: Request
):
    """Query for relevant runbook steps"""
    try:
        vector_store = api_request.app.state.vector_store
        service = VectorSearchService(vector_store)
        
        results = await service.search(
            query=request.incident_description,
            top_k=request.top_k
        )
        
        return QueryResponse(results=results)
    except Exception as e:
        logger.error(f"Error querying runbooks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-playbook", response_model=GeneratePlaybookResponse)
async def generate_playbook(
    request: GeneratePlaybookRequest,
    api_request: Request
):
    """Generate complete remediation playbook"""
    try:
        vector_store = api_request.app.state.vector_store
        service = PlaybookGeneratorService(vector_store)
        
        playbook = await service.generate_playbook(
            incident_description=request.incident_description,
            context=request.context,
            include_verification=request.include_verification
        )
        
        return GeneratePlaybookResponse(playbook=playbook)
    except Exception as e:
        logger.error(f"Error generating playbook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))