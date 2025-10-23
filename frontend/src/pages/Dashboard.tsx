import React, { useState } from 'react';
import { BookOpen } from 'lucide-react'; // ✅ Added missing import
import { useAppContext } from '../context/AppContext';
import IncidentInput from '../components/Incident Input';
import PlaybookDisplay from '../components/PlaybookDisplay';
import SearchResults from '../components/SearchResults';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';

const Dashboard: React.FC = () => {
  const { playbook, searchResults, isLoading, error } = useAppContext();
  const [activeTab, setActiveTab] = useState<'playbook' | 'search'>('playbook');

  return (
    <div className="space-y-6">
      <IncidentInput />
      
      {error && <ErrorMessage message={error} />}
      
      {isLoading && <LoadingSpinner />}
      
      {!isLoading && (playbook || searchResults.length > 0) && (
        <div className="bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('playbook')}
                className={`px-6 py-3 text-sm font-medium border-b-2 ${
                  activeTab === 'playbook'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Remediation Playbook
              </button>
              <button
                onClick={() => setActiveTab('search')}
                className={`px-6 py-3 text-sm font-medium border-b-2 ${
                  activeTab === 'search'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Retrieved Runbooks ({searchResults.length})
              </button>
            </nav>
          </div>
          
          <div className="p-6">
            {activeTab === 'playbook' && playbook && (
              <PlaybookDisplay playbook={playbook} />
            )}
            
            {activeTab === 'search' && (
              <SearchResults results={searchResults} />
            )}
          </div>
        </div>
      )}
      
      {!isLoading && !playbook && !searchResults.length && !error && (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            No Incident Analyzed Yet
          </h3>
          <p className="text-gray-600">
            Enter an incident description above to generate a remediation playbook
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
