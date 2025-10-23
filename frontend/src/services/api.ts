import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface IngestRequest {
  directory_path: string;
}

export interface QueryRequest {
  incident_description: string;
  top_k?: number;
}

export interface GeneratePlaybookRequest {
  incident_description: string;
  context?: string[];
  include_verification?: boolean;
}

export const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await api.get('/health');
    return response.data;
  },

  // Ingest documents
  ingestDocuments: async (request: IngestRequest) => {
    const response = await api.post('/ingest', request);
    return response.data;
  },

  // Query runbooks
  queryRunbooks: async (request: QueryRequest) => {
    const response = await api.post('/query', request);
    return response.data;
  },

  // Generate playbook
  generatePlaybook: async (request: GeneratePlaybookRequest) => {
    const response = await api.post('/generate-playbook', request);
    return response.data;
  },
};

export default api;