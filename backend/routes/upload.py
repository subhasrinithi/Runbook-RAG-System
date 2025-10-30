from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import os
import shutil
from datetime import datetime
import uuid

from models.database import SessionLocal, Document
from services.document_processor import DocumentProcessor
from services.embeddings import EmbeddingService
from src.modules.vector_search.vector_store import VectorStore
from src.config import settings

router = APIRouter()

# Initialize services
doc_processor = DocumentProcessor()

# Lazy load these (will be initialized on first use)
_embedding_service = None
_vector_store = None


def get_embedding_service():
    """Lazy load embedding service"""
    global _embedding_service
    if _embedding_service is None:
        _embedding_service = EmbeddingService()
    return _embedding_service


def get_vector_store():
    """Lazy load vector store"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    service: str = Form(...),
    severity: str = Form(...),
    owner: Optional[str] = Form(None),
    version: Optional[str] = Form("1.0"),
    tags: Optional[str] = Form(None)
):
    """Upload and process a document"""
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.allowed_extensions:
        raise HTTPException(400, f"File type {file_ext} not allowed")
    
    # Create upload directory
    os.makedirs(settings.upload_dir, exist_ok=True)
    
    # Save file temporarily
    file_path = os.path.join(settings.upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_size = os.path.getsize(file_path)
    
    if file_size > settings.max_file_size:
        os.remove(file_path)
        raise HTTPException(400, "File size exceeds 10MB limit")
    
    try:
        # Read and process document
        text = doc_processor.read_file(file_path, file_ext)
        chunks = doc_processor.chunk_text(text)
        
        # Generate embeddings (lazy load)
        embedding_service = get_embedding_service()
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings, embed_latency = embedding_service.generate_embeddings(chunk_texts)
        
        # Parse tags
        tag_list = [tag.strip() for tag in tags.split(',')] if tags else []
        
        # Prepare data for vector store (matching your VectorStore interface)
        vector_ids = []
        texts = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            doc_id = str(uuid.uuid4())
            vector_ids.append(doc_id)
            texts.append(chunk['text'])
            
            chunk_metadata = {
                'filename': file.filename,
                'service': service,
                'severity': severity,
                'owner': owner or '',
                'version': version,
                'tags': ','.join(tag_list),
                'chunk_id': str(chunk['chunk_id'])
            }
            metadatas.append(chunk_metadata)
        
        # Store in vector database (lazy load)
        vector_store = get_vector_store()
        vector_store.add_documents(
            texts=texts,
            metadatas=metadatas,
            ids=vector_ids
        )
        
        # Store metadata in relational DB
        db = SessionLocal()
        document = Document(
            filename=file.filename,
            service=service,
            severity=severity,
            owner=owner,
            version=version,
            tags=tag_list,
            file_size=file_size,
            chunk_count=len(chunks),
            embed_latency_ms=embed_latency,
            vector_ids=vector_ids
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        db.close()
        
        return {
            "success": True,
            "document_id": document.id,
            "ingestion_log": {
                "filename": file.filename,
                "file_size": f"{file_size / 1024:.2f} KB",
                "chunks": len(chunks),
                "vectors_stored": len(vector_ids),
                "embed_latency": f"{embed_latency}ms",
                "service": service,
                "severity": severity,
                "tags": tag_list,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    db = SessionLocal()
    documents = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    db.close()
    
    return {
        "documents": [
            {
                "id": doc.id,
                "name": doc.filename,
                "service": doc.service,
                "severity": doc.severity,
                "tags": doc.tags,
                "chunk_count": doc.chunk_count,
                "uploaded_at": doc.uploaded_at.isoformat()
            }
            for doc in documents
        ]
    }