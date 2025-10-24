Runbook RAG System:
AI-powered incident remediation system that generates step-by-step playbooks using RAG (Retrieval-Augmented Generation).
What It Does
Upload your runbook documentation, describe an incident, and get an automated remediation playbook with relevant context from your documents.


```mermaid
graph TB
    subgraph Frontend["Frontend Layer - React + TypeScript + Tailwind"]
        A[Dashboard Page] --> D[API Client Axios]
        B[Incident Input Form] --> D
        C[Playbook Display] --> D
    end
    
    D -->|HTTP/REST| E[API GatewayFastAPI]
    
    subgraph Backend["Backend Services - Python"]
        E --> F[Document Ingestion]
        E --> G[Vector Search]
        E --> H[RAG Engine]
        
        F -->|Embeddings| I[(ChromaDBVector Store)]
        G -->|Query| I
        H -->|Retrieve Context| G
        H --> J[Playbook Generator]
    end
    
    H -->|LLM Request| K[External LLMOpenAI / Anthropic]
    
    style A fill:#60a5fa,stroke:#2563eb,color:#fff
    style B fill:#60a5fa,stroke:#2563eb,color:#fff
    style C fill:#60a5fa,stroke:#2563eb,color:#fff
    style D fill:#3b82f6,stroke:#1e40af,color:#fff
    style E fill:#fbbf24,stroke:#f59e0b,color:#000
    style F fill:#8b5cf6,stroke:#7c3aed,color:#fff
    style G fill:#10b981,stroke:#059669,color:#fff
    style H fill:#ec4899,stroke:#db2777,color:#fff
    style I fill:#0891b2,stroke:#0e7490,color:#fff
    style J fill:#f59e0b,stroke:#d97706,color:#fff
    style K fill:#7c3aed,stroke:#6d28d9,color:#fff
```
Features:
 1.Upload runbook documents (PDF, DOCX, TXT, MD)
 2.Semantic search through documentation
 3.AI-generated incident remediation steps
 4.Clean, modern web interface.


 Backend Setup:
 cd backend
 python -m venv venv
 .\venv\Scripts\activate 
 pip install -r requirements.txt
 uvicorn src.main:app --reload --port 8000
 Backend runs at: http://localhost:8000

 Frontend Setup:
 cd frontend
 npm install
 npm run dev
 Frontend runs at: http://localhost:3000

 Tech Stack:
Backend:

FastAPI
LangChain
ChromaDB
OpenAI/Anthropic

Frontend:

React 18
TypeScript
Tailwind CSS
Vite

PROJECT STRUCTURE:

incident-remediation/
├── backend/
│   ├── src/
│   │   ├── api/             
│   │   ├── modules/          
│   │   ├── config.py
│   │   └── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       
│   │   ├── pages/            
│   │   ├── services/         
│   │   └── App.tsx
│   └── package.json
│
└── README.md

Usage:

Start both backend and frontend servers
Open http://localhost:3000
Upload runbook documents
Enter incident description
Get AI-generated remediation playbook



