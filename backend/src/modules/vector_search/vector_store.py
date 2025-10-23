import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging

from src.config import settings as app_settings

logger = logging.getLogger(__name__)


class VectorStore:
    """Interface to vector database (ChromaDB)"""
    
    def __init__(self):
        logger.info("Initializing vector store...")
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path=app_settings.vector_db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=app_settings.chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        logger.info(f"Vector store initialized with collection: {app_settings.chroma_collection_name}")
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ):
        """Add documents to vector store"""
        try:
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"Added {len(texts)} documents to vector store")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and len(results['documents'][0]) > 0:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "chunk_id": results['ids'][0][i],
                        "relevance_score": 1 - results['distances'][0][i]  # Convert distance to similarity
                    })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            raise
    
    def count(self) -> int:
        """Get count of documents in collection"""
        return self.collection.count()
    
    def clear(self):
        """Clear all documents from collection"""
        self.client.delete_collection(app_settings.chroma_collection_name)
        self.collection = self.client.get_or_create_collection(
            name=app_settings.chroma_collection_name
        )
        logger.info("Vector store cleared")