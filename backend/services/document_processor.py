import PyPDF2
from typing import List, Dict
import re
from src.config import settings



class DocumentProcessor:
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap
    
    def read_file(self, file_path: str, file_type: str) -> str:
        """Read content from file based on type"""
        if file_type == '.pdf':
            return self._read_pdf(file_path)
        elif file_type in ['.md', '.txt']:
            return self._read_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _read_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    
    def _read_text(self, file_path: str) -> str:
        """Read text/markdown file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def chunk_text(self, text: str) -> List[Dict[str, any]]:
        """Split text into chunks with overlap"""
        text = re.sub(r'\s+', ' ', text).strip()
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            if end < len(text):
                sentence_end = text.rfind('. ', start, end)
                if sentence_end == -1:
                    sentence_end = text.rfind('! ', start, end)
                if sentence_end == -1:
                    sentence_end = text.rfind('? ', start, end)
                if sentence_end != -1:
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append({
                    'chunk_id': chunk_id,
                    'text': chunk_text,
                    'start_idx': start,
                    'end_idx': end
                })
                chunk_id += 1
            
            start = end - self.chunk_overlap if end < len(text) else end
        
        return chunks