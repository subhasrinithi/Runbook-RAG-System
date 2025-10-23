import re
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class DocumentParser:
    """Parse markdown documents and extract metadata"""
    
    def parse(self, document: Dict) -> Dict:
        """Parse a document and extract structured information"""
        content = document["content"]
        
        # Extract metadata from content
        metadata = {
            "source": document["source"],
            "filename": document["filename"],
            "incident_type": self._extract_incident_type(content),
            "severity": self._extract_severity(content),
            "tags": self._extract_tags(content)
        }
        
        return {
            "content": content,
            "metadata": metadata
        }
    
    def _extract_incident_type(self, content: str) -> str:
        """Extract incident type from content"""
        patterns = [
            r"(?i)incident\s*type:\s*(.+)",
            r"(?i)type:\s*(.+)",
            r"(?i)category:\s*(.+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()
        
        return "unknown"
    
    def _extract_severity(self, content: str) -> str:
        """Extract severity level from content"""
        severity_pattern = r"(?i)severity:\s*(critical|high|medium|low)"
        match = re.search(severity_pattern, content)
        
        if match:
            return match.group(1).lower()
        
        return "medium"
    
    def _extract_tags(self, content: str) -> list:
        """Extract tags from content"""
        tags_pattern = r"(?i)tags?:\s*(.+)"
        match = re.search(tags_pattern, content)
        
        if match:
            tags_str = match.group(1)
            return [tag.strip() for tag in re.split(r'[,;]', tags_str)]
        
        return []