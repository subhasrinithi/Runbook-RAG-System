import React, { useState } from 'react';
import { Search, Wand2 } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { apiService } from '../services/api';

const IncidentInput: React.FC = () => {
  const [incidentDescription, setIncidentDescription] = useState('');
  const [actionType, setActionType] = useState<'query' | 'generate'>('generate');
  const { setPlaybook, setSearchResults, setIsLoading, setError } = useAppContext();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!incidentDescription.trim()) {
      setError('Please enter an incident description');
      return;
    }

    setIsLoading(true);
    setError(null);
    setPlaybook(null);
    setSearchResults([]);

    try {
      if (actionType === 'query') {
        // Just search for relevant runbooks
        const response = await apiService.queryRunbooks({
          incident_description: incidentDescription,
          top_k: 5,
        });
        setSearchResults(response.results);
      } else {
        // Generate full playbook
        const response = await apiService.generatePlaybook({
          incident_description: incidentDescription,
          include_verification: true,
        });
        setPlaybook(response.playbook);
        
        // Also fetch search results for reference
        const searchResponse = await apiService.queryRunbooks({
          incident_description: incidentDescription,
          top_k: 5,
        });
        setSearchResults(searchResponse.results);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Describe Your Incident
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="incident" className="block text-sm font-medium text-gray-700 mb-2">
            Incident Description
          </label>
          <textarea
            id="incident"
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="e.g., Database connection timeouts on production server, high CPU usage causing application slowdowns..."
            value={incidentDescription}
            onChange={(e) => setIncidentDescription(e.target.value)}
          />
        </div>

        <div className="flex items-center space-x-4">
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              name="action"
              value="generate"
              checked={actionType === 'generate'}
              onChange={() => setActionType('generate')}
              className="text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Generate Complete Playbook</span>
          </label>
          
          <label className="flex items-center space-x-2">
            <input
              type="radio"
              name="action"
              value="query"
              checked={actionType === 'query'}
              onChange={() => setActionType('query')}
              className="text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700">Search Runbooks Only</span>
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2 font-medium"
        >
          {actionType === 'generate' ? (
            <>
              <Wand2 className="h-5 w-5" />
              <span>Generate Remediation Playbook</span>
            </>
          ) : (
            <>
              <Search className="h-5 w-5" />
              <span>Search Runbooks</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default IncidentInput;