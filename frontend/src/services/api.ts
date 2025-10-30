import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API service methods
export const apiService = {
  queryRunbooks: async (query: any) => {
    const response = await api.post('/api/v1/query', query)
    return response.data
  },
  
  generatePlaybook: async (data: any) => {
    const response = await api.post('/api/v1/generate-playbook', data)
    return response.data
  },
  
  uploadDocument: async (formData: FormData) => {
    const response = await api.post('/api/v1/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  
  getDocuments: async () => {
    const response = await api.get('/api/v1/documents')
    return response.data
  }
}

export default api
