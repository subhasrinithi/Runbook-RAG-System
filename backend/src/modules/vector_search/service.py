from typing import List, Dict, Optional
import logging

from src.modules.vector_search.vector_store import VectorStore

logger = logging.getLogger(__name__)


class VectorSearchService:
    """Service for semantic search over runbooks"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    async def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for relevant runbook sections"""
        logger.info(f"Searching for: {query[:100]}...")
        
        results = self.vector_store.search(
            query=query,
            top_k=top_k,
            filter_metadata=filter_metadata
        )
        
        logger.info(f"Found {len(results)} results")
        return results