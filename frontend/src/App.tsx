import { useState } from 'react'
import UploadPage from './components/UploadPage'
import SearchPage from './components/SearchPage'

function App() {
  const [currentPage, setCurrentPage] = useState('upload')

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md border-b-2 border-gray-200">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between items-center h-16">
            <div className="flex space-x-8">
              <button
                onClick={() => setCurrentPage('search')}
                style={{
                  padding: '8px 12px',
                  borderBottom: currentPage === 'search' ? '2px solid blue' : '2px solid transparent',
                  color: currentPage === 'search' ? 'blue' : 'gray',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                Search Runbooks
              </button>
              
              <button
                onClick={() => setCurrentPage('upload')}
                style={{
                  padding: '8px 12px',
                  borderBottom: currentPage === 'upload' ? '2px solid blue' : '2px solid transparent',
                  color: currentPage === 'upload' ? 'blue' : 'gray',
                  background: 'transparent',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '16px'
                }}
              >
                Upload Documents
              </button>
            </div>
            
            <h1 style={{ fontSize: '20px', fontWeight: 'bold' }}>
              Runbook RAG System
            </h1>
          </div>
        </div>
      </nav>

      <main>
        {currentPage === 'upload' ? <UploadPage /> : <SearchPage />}
      </main>
    </div>
  )
}

export default App