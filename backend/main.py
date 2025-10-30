from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

from src.api.routes import router
from src.config import settings
from src.modules.vector_search.vector_store import VectorStore

# Import the new upload router
from routes.upload import router as upload_router

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting Runbook RAG API...")
    
    # Initialize vector store
    vector_store = VectorStore()
    app.state.vector_store = vector_store
    
    # Create necessary directories
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.vector_db_path, exist_ok=True)
    os.makedirs(os.path.dirname(settings.database_url.replace('sqlite:///', '')), exist_ok=True)
    
    logger.info("Application startup complete")
    yield
    
    # Shutdown
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

# Include existing router
app.include_router(router, prefix="/api/v1")

# Include new upload router
app.include_router(upload_router, prefix="/api/v1", tags=["upload"])


@app.get("/")
async def root():
    return {
        "message": "Runbook RAG API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )