from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.config import settings

Base = declarative_base()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    service = Column(String, index=True)
    severity = Column(String, index=True)
    owner = Column(String)
    version = Column(String)
    tags = Column(JSON)
    file_size = Column(Integer)
    chunk_count = Column(Integer)
    embed_latency_ms = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    vector_ids = Column(JSON)


# Create tables on import
Base.metadata.create_all(bind=engine)