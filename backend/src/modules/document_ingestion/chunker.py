from typing import List, Dict
import re
import uuid
import logging

logger = logging.getLogger(__name__)


class ChunkingEngine:
    """Split documents into semantic chunks"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """Chunk a document into smaller pieces"""
        content = document["content"]
        metadata = document["metadata"]
        
        # Split by sections (headers) first
        sections = self._split_by_headers(content)
        
        chunks = []
        for section in sections:
            # If section is small enough, keep as is
            if len(section["content"]) <= self.chunk_size:
                chunks.append({
                    "id": str(uuid.uuid4()),
                    "content": section["content"],
                    "metadata": {
                        **metadata,
                        "section_title": section["title"],
                        "chunk_type": "section"
                    }
                })
            else:
                # Split large sections into smaller chunks
                section_chunks = self._split_text(section["content"])
                for i, chunk_text in enumerate(section_chunks):
                    chunks.append({
                        "id": str(uuid.uuid4()),
                        "content": chunk_text,
                        "metadata": {
                            **metadata,
                            "section_title": section["title"],
                            "chunk_index": i,
                            "chunk_type": "subsection"
                        }
                    })
        
        return chunks
    
    def _split_by_headers(self, content: str) -> List[Dict]:
        """Split content by markdown headers"""
        sections = []
        
        # Split by headers (##, ###, etc.)
        header_pattern = r'^(#{1,6})\s+(.+)$'
        lines = content.split('\n')
        
        current_section = {"title": "Introduction", "content": ""}
        
        for line in lines:
            match = re.match(header_pattern, line)
            if match:
                # Save previous section
                if current_section["content"].strip():
                    sections.append(current_section)
                
                # Start new section
                current_section = {
                    "title": match.group(2).strip(),
                    "content": ""
                }
            else:
                current_section["content"] += line + "\n"
        
        # Add last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        return sections
    
    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(' '.join(chunk_words))
        
        return chunks

