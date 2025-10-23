from typing import Optional, Dict
import logging
import os

from src.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Interface to LLM API"""
    
    def __init__(self):
        self.provider = settings.llm_provider
        self.model = settings.llm_model
        self.api_key = settings.llm_api_key or os.getenv("LLM_API_KEY")
        
        if not self.api_key:
            logger.warning("No LLM API key configured - using mock mode")
            self.mock_mode = True
        else:
            self.mock_mode = False
            self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate completion from LLM"""
        if self.mock_mode:
            return self._mock_generate(prompt)
        
        try:
            if self.provider == "openai":
                return await self._generate_openai(prompt, system_prompt)
            elif self.provider == "anthropic":
                return await self._generate_anthropic(prompt, system_prompt)
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            return self._mock_generate(prompt)
    
    async def _generate_openai(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate using OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    async def _generate_anthropic(self, prompt: str, system_prompt: Optional[str]) -> str:
        """Generate using Anthropic"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt or "",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
    
    def _mock_generate(self, prompt: str) -> str:
        """Mock LLM generation for testing"""
        return """# Database Connection Failure Remediation Playbook"""