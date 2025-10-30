import React, { useState, useEffect } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle, Loader, X, Plus } from 'lucide-react';
import axios from 'axios';

interface IngestionLog {
  filename: string;
  file_size: string;
  chunks: number;
  embed_latency: string;
  vectors_stored: number;
  service: string;
  severity: string;
  tags: string[];
  timestamp: string;
}

interface Document {
  id: number;
  name: string;
  service: string;
  severity: string;
  tags: string[];
  chunk_count: number;
  uploaded_at: string;
}

const API_BASE_URL = 'http://localhost:8000/api/v1';

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState({
    service: '',
    severity: 'medium',
    tags: [] as string[],
    owner: '',
    version: '1.0'
  });
  const [tagInput, setTagInput] = useState('');
  const [uploading, setUploading] = useState(false);
  const [ingestionLog, setIngestionLog] = useState<IngestionLog | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`);
      setDocuments(response.data.documents);
    } catch (err) {
      console.error('Failed to fetch documents:', err);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      const validTypes = ['.md', '.txt', '.pdf'];
      const fileExt = '.' + selectedFile.name.split('.').pop()?.toLowerCase();
      const isValid = validTypes.includes(fileExt);
      
      if (isValid) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError('Please upload a markdown (.md), text (.txt), or PDF file');
        setFile(null);
      }
    }
  };

  const handleAddTag = () => {
    if (tagInput.trim() && !metadata.tags.includes(tagInput.trim())) {
      setMetadata({
        ...metadata,
        tags: [...metadata.tags, tagInput.trim()]
      });
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setMetadata({
      ...metadata,
      tags: metadata.tags.filter(tag => tag !== tagToRemove)
    });
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }
    if (!metadata.service) {
      setError('Please specify a service name');
      return;
    }

    setUploading(true);
    setError(null);
    setIngestionLog(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('service', metadata.service);
    formData.append('severity', metadata.severity);
    if (metadata.owner) formData.append('owner', metadata.owner);
    formData.append('version', metadata.version);
    if (metadata.tags.length > 0) formData.append('tags', metadata.tags.join(','));

    try {
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setIngestionLog(response.data.ingestion_log);
      
      // Reset form
      setFile(null);
      setMetadata({
        service: '',
        severity: 'medium',
        tags: [],
        owner: '',
        version: '1.0'
      });
      
      // Clear file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
      
      // Refresh documents list
      fetchDocuments();
      
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-slate-800">Runbook Document Upload</h1>
          </div>
          <p className="text-slate-600">Upload runbooks and documentation to the RAG system</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Upload Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-slate-800 mb-4">Upload Document</h2>
              
              {/* File Upload */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Document File
                </label>
                <div className="border-2 border-dashed border-slate-300 rounded-lg p-8 text-center hover:border-blue-400 transition-colors">
                  <input
                    id="file-input"
                    type="file"
                    accept=".md,.txt,.pdf"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                  <label htmlFor="file-input" className="cursor-pointer">
                    <Upload className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                    <p className="text-slate-600 mb-1">
                      {file ? file.name : 'Click to upload or drag and drop'}
                    </p>
                    <p className="text-sm text-slate-400">
                      Markdown, Text, or PDF (max 10MB)
                    </p>
                  </label>
                </div>
              </div>

              {/* Metadata Fields */}
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Service Name *
                    </label>
                    <input
                      type="text"
                      value={metadata.service}
                      onChange={(e) => setMetadata({...metadata, service: e.target.value})}
                      placeholder="e.g., payment-service"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Severity
                    </label>
                    <select
                      value={metadata.severity}
                      onChange={(e) => setMetadata({...metadata, severity: e.target.value})}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Owner
                    </label>
                    <input
                      type="text"
                      value={metadata.owner}
                      onChange={(e) => setMetadata({...metadata, owner: e.target.value})}
                      placeholder="e.g., platform-team"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-2">
                      Version
                    </label>
                    <input
                      type="text"
                      value={metadata.version}
                      onChange={(e) => setMetadata({...metadata, version: e.target.value})}
                      placeholder="e.g., 1.0"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Tags
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      value={tagInput}
                      onChange={(e) => setTagInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddTag())}
                      placeholder="Add tags (press Enter)"
                      className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      onClick={handleAddTag}
                      type="button"
                      className="px-4 py-2 bg-slate-200 text-slate-700 rounded-lg hover:bg-slate-300 transition-colors"
                    >
                      <Plus className="w-5 h-5" />
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {metadata.tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm flex items-center gap-2"
                      >
                        {tag}
                        <X
                          className="w-4 h-4 cursor-pointer hover:text-blue-900"
                          onClick={() => handleRemoveTag(tag)}
                        />
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Error Display */}
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                  <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
                  <p className="text-red-700">{error}</p>
                </div>
              )}

              {/* Upload Button */}
              <button
                onClick={handleUpload}
                disabled={uploading || !file}
                type="button"
                className="mt-6 w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
              >
                {uploading ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="w-5 h-5" />
                    Upload & Process Document
                  </>
                )}
              </button>
            </div>

            {/* Ingestion Log */}
            {ingestionLog && (
              <div className="mt-6 bg-white rounded-lg shadow-sm p-6">
                <div className="flex items-center gap-3 mb-4">
                  <CheckCircle className="w-6 h-6 text-green-600" />
                  <h3 className="text-lg font-semibold text-slate-800">Ingestion Complete</h3>
                </div>
                
                <div className="space-y-3 text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-50 p-3 rounded-lg">
                      <p className="text-slate-600 mb-1">File Name</p>
                      <p className="font-medium text-slate-800">{ingestionLog.filename}</p>
                    </div>
                    <div className="bg-slate-50 p-3 rounded-lg">
                      <p className="text-slate-600 mb-1">File Size</p>
                      <p className="font-medium text-slate-800">{ingestionLog.file_size}</p>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-3 gap-4">
                    <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
                      <p className="text-blue-600 mb-1">Chunks Created</p>
                      <p className="text-2xl font-bold text-blue-700">{ingestionLog.chunks}</p>
                    </div>
                    <div className="bg-green-50 p-3 rounded-lg border border-green-200">
                      <p className="text-green-600 mb-1">Vectors Stored</p>
                      <p className="text-2xl font-bold text-green-700">{ingestionLog.vectors_stored}</p>
                    </div>
                    <div className="bg-purple-50 p-3 rounded-lg border border-purple-200">
                      <p className="text-purple-600 mb-1">Embed Latency</p>
                      <p className="text-2xl font-bold text-purple-700">{ingestionLog.embed_latency}</p>
                    </div>
                  </div>

                  <div className="bg-slate-50 p-3 rounded-lg">
                    <p className="text-slate-600 mb-2">Metadata Stored</p>
                    <div className="flex flex-wrap gap-2">
                      <span className="px-2 py-1 bg-white border border-slate-300 rounded text-slate-700">
                        Service: {ingestionLog.service}
                      </span>
                      <span className="px-2 py-1 bg-white border border-slate-300 rounded text-slate-700">
                        Severity: {ingestionLog.severity}
                      </span>
                      {ingestionLog.tags.map((tag, idx) => (
                        <span key={idx} className="px-2 py-1 bg-white border border-slate-300 rounded text-slate-700">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Uploaded Documents List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-6">
              <h3 className="text-lg font-semibold text-slate-800 mb-4">Recent Uploads</h3>
              
              {documents.length === 0 ? (
                <div className="text-center py-8 text-slate-400">
                  <FileText className="w-12 h-12 mx-auto mb-3 opacity-50" />
                  <p>No documents uploaded yet</p>
                </div>
              ) : (
                <div className="space-y-3 max-h-[600px] overflow-y-auto">
                  {documents.map((doc) => (
                    <div key={doc.id} className="border border-slate-200 rounded-lg p-3 hover:border-blue-300 transition-colors">
                      <div className="flex items-start gap-2 mb-2">
                        <FileText className="w-4 h-4 text-blue-600 mt-1 flex-shrink-0" />
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-slate-800 text-sm truncate">{doc.name}</p>
                          <p className="text-xs text-slate-500">{new Date(doc.uploaded_at).toLocaleString()}</p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1 mt-2">
                        <span className="px-2 py-0.5 bg-slate-100 text-slate-700 rounded text-xs">
                          {doc.service}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-xs ${
                          doc.severity === 'critical' ? 'bg-red-100 text-red-700' :
                          doc.severity === 'high' ? 'bg-orange-100 text-orange-700' :
                          doc.severity === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                          'bg-green-100 text-green-700'
                        }`}>
                          {doc.severity}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;