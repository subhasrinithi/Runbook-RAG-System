from typing import List, Optional, Dict
import logging
import json
import re

from src.modules.vector_search.vector_store import VectorStore
from src.modules.vector_search.service import VectorSearchService
from src.modules.rag_engine.query_processor import QueryProcessor
from src.modules.rag_engine.context_builder import ContextBuilder
from src.modules.rag_engine.llm_client import LLMClient
from src.modules.playbook_generator.formatter import PlaybookFormatter

logger = logging.getLogger(__name__)


class PlaybookGeneratorService:
    """Service for generating remediation playbooks"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.search_service = VectorSearchService(vector_store)
        self.query_processor = QueryProcessor()
        self.context_builder = ContextBuilder()
        self.llm_client = LLMClient()
        self.formatter = PlaybookFormatter()
    
    async def generate_playbook(
        self,
        incident_description: str,
        context: Optional[List[str]] = None,
        include_verification: bool = True
    ) -> Dict:
        """Generate a complete remediation playbook"""
        logger.info(f"Generating playbook for: {incident_description[:100]}...")
        
        # Process query
        processed_query = self.query_processor.process(incident_description)
        
        # Retrieve context if not provided
        if context is None:
            search_results = await self.search_service.search(
                query=processed_query["enhanced_query"],
                top_k=5
            )
            context_str = self.context_builder.build_context(search_results)
        else:
            context_str = "\n\n".join(context)
        
        # Generate playbook using LLM
        playbook_text = await self._generate_playbook_with_llm(
            incident_description,
            context_str,
            include_verification
        )
        
        # Parse and format playbook
        playbook = self.formatter.parse_playbook(playbook_text)
        
        return playbook
    
    async def _generate_playbook_with_llm(
        self,
        incident_description: str,
        context: str,
        include_verification: bool
    ) -> str:
        """Generate playbook using LLM"""
        system_prompt = """You are an expert Site Reliability Engineer creating incident remediation playbooks.
Create clear, actionable, step-by-step playbooks that help resolve incidents quickly and safely."""
        
        verification_instruction = ""
        if include_verification:
            verification_instruction = "\nFor each step, include a verification method to confirm success."
        
        prompt = f"""Based on the following incident and relevant runbook sections, create a detailed remediation playbook.

INCIDENT: {incident_description}

RELEVANT RUNBOOK SECTIONS:
{context}

Create a playbook with:
1. A clear title
2. A brief summary (2-3 sentences)
3. Step-by-step instructions with:
   - Action to take
   - Command to execute (if applicable)
   - Expected outcome
   - Verification method{verification_instruction}
4. Estimated time to complete
5. Risk level (Low/Medium/High/Critical)

Format the playbook in markdown with clear sections."""
        
        response = await self.llm_client.generate(prompt, system_prompt)
        return response
