from sentence_transformers import SentenceTransformer
from typing import List
import time
from src.config import settings


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
    
    def generate_embeddings(self, texts: List[str]) -> tuple:
        """Generate embeddings for texts and return embeddings with latency"""
        start_time = time.time()
        embeddings = self.model.encode(texts, show_progress_bar=False)
        latency_ms = int((time.time() - start_time) * 1000)
        
        return embeddings, latency_ms