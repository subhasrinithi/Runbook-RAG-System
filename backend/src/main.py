from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from src.api.routes import router
from src.config import settings
from src.modules.vector_search.vector_store import VectorStore

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting Runbook RAG API...")
    
    
    vector_store = VectorStore()
    app.state.vector_store = vector_store
    
    logger.info("Application startup complete")
    yield
    

    logger.info("Shutting down application...")


app = FastAPI(
    title="Runbook RAG API",
    description="API for retrieving runbook steps and generating remediation playbooks",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Runbook RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }