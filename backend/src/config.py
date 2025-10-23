from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # LLM Configuration
    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "openai/gpt-4o"
    
    # Vector DB
    vector_db_path: str = "./data/vectordb"
    chroma_collection_name: str = "runbooks"
    
    # Document Storage
    runbooks_path: str = "./data/runbooks"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()