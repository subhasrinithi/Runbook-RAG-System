import re
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class QueryProcessor:
    """Process and enhance user queries"""
    
    def process(self, query: str) -> Dict:
        """Process a query and extract key information"""
        
        # Extract keywords
        keywords = self._extract_keywords(query)
        
        # Detect incident type
        incident_type = self._detect_incident_type(query)
        
        # Detect urgency
        urgency = self._detect_urgency(query)
        
        return {
            "original_query": query,
            "keywords": keywords,
            "incident_type": incident_type,
            "urgency": urgency,
            "enhanced_query": self._enhance_query(query, keywords, incident_type)
        }
    
    def _extract_keywords(self, query: str) -> list:
        """Extract important keywords from query"""
        # Remove common words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being'}
        
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        
        return keywords
    
    def _detect_incident_type(self, query: str) -> str:
        """Detect the type of incident from query"""
        incident_patterns = {
            "database": r"(?i)(database|db|mysql|postgres|sql|connection)",
            "network": r"(?i)(network|connectivity|timeout|dns|firewall)",
            "application": r"(?i)(application|app|service|api|crash|error)",
            "performance": r"(?i)(slow|performance|latency|cpu|memory|disk)",
            "security": r"(?i)(security|breach|unauthorized|hack|vulnerability)"
        }
        
        for incident_type, pattern in incident_patterns.items():
            if re.search(pattern, query):
                return incident_type
        
        return "general"
    
    def _detect_urgency(self, query: str) -> str:
        """Detect urgency level from query"""
        urgent_keywords = r"(?i)(urgent|critical|emergency|down|outage|production)"
        
        if re.search(urgent_keywords, query):
            return "high"
        
        return "normal"
    
    def _enhance_query(self, query: str, keywords: list, incident_type: str) -> str:
        """Enhance query with additional context"""
        enhanced = query
        
        if incident_type != "general":
            enhanced += f" {incident_type} incident"
        
        return enhanced