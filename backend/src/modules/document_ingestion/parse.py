import os
from pathlib import Path
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Load markdown documents from filesystem"""
    
    def load_directory(self, directory_path: str) -> List[Dict]:
        """Load all .md files from a directory"""
        documents = []
        path = Path(directory_path)
        
        if not path.exists():
            logger.warning(f"Directory does not exist: {directory_path}")
            return documents
        
        for file_path in path.glob("**/*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        "content": content,
                        "source": str(file_path),
                        "filename": file_path.name
                    })
                logger.debug(f"Loaded document: {file_path}")
            except Exception as e:
                logger.error(f"Error loading {file_path}: {str(e)}")
        
        return documents