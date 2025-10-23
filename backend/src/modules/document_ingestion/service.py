import os
import logging
from typing import Dict, List
from pathlib import Path

from src.modules.document_ingestion.loader import DocumentLoader
from src.modules.document_ingestion.parser import DocumentParser
from src.modules.document_ingestion.chunker import ChunkingEngine
from src.modules.document_ingestion.embeddings import EmbeddingGenerator
from src.modules.vector_search.vector_store import VectorStore

logger = logging.getLogger(__name__)


class DocumentIngestionService:
    """Service for ingesting and indexing runbook documents"""
    
    def __init__(self, vector_store: VectorStore):
        self.loader = DocumentLoader()
        self.parser = DocumentParser()
        self.chunker = ChunkingEngine()
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = vector_store
    
    async def ingest_directory(self, directory_path: str) -> Dict:
        """Ingest all markdown files from a directory"""
        logger.info(f"Starting ingestion from directory: {directory_path}")
        
        # Load documents
        documents = self.loader.load_directory(directory_path)
        logger.info(f"Loaded {len(documents)} documents")
        
        if not documents:
            return {
                "documents_processed": 0,
                "chunks_created": 0
            }
        
        # Parse and chunk documents
        all_chunks = []
        for doc in documents:
            parsed_doc = self.parser.parse(doc)
            chunks = self.chunker.chunk_document(parsed_doc)
            all_chunks.extend(chunks)
        
        logger.info(f"Created {len(all_chunks)} chunks")
        
        # Generate embeddings and store
        texts = [chunk["content"] for chunk in all_chunks]
        metadatas = [chunk["metadata"] for chunk in all_chunks]
        ids = [chunk["id"] for chunk in all_chunks]
        
        self.vector_store.add_documents(texts, metadatas, ids)
        
        return {
            "documents_processed": len(documents),
            "chunks_created": len(all_chunks)
        }