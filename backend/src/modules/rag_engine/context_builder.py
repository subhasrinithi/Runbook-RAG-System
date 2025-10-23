from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class ContextBuilder:
    """Build context from retrieved documents"""
    
    def build_context(self, search_results: List[Dict], max_context_length: int = 3000) -> str:
        """Build context string from search results"""
        context_parts = []
        current_length = 0
        
        for i, result in enumerate(search_results, 1):
            content = result["content"]
            source = result["metadata"].get("filename", "unknown")
            section = result["metadata"].get("section_title", "")
            
            part = f"\n--- Runbook {i} (from {source}) ---\n"
            if section:
                part += f"Section: {section}\n"
            part += f"{content}\n"
            
            if current_length + len(part) > max_context_length:
                break
            
            context_parts.append(part)
            current_length += len(part)
        
        return "\n".join(context_parts)

