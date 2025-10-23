import React from 'react';
import { FileText, Star } from 'lucide-react';

interface SearchResult {
  content: string;
  metadata: Record<string, any>;
  chunk_id: string;
  relevance_score: number;
}

interface SearchResultsProps {
  results: SearchResult[];
}

const SearchResults: React.FC<SearchResultsProps> = ({ results }) => {
  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <FileText className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No relevant runbooks found</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Retrieved Runbook Sections
      </h3>
      
      {results.map((result, index) => (
        <div
          key={result.chunk_id}
          className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-semibold text-sm">
                {index + 1}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-900">
                  {result.metadata.filename || 'Unknown Source'}
                </p>
                {result.metadata.section_title && (
                  <p className="text-xs text-gray-500">
                    {result.metadata.section_title}
                  </p>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-1 text-yellow-500">
              <Star className="h-4 w-4 fill-current" />
              <span className="text-sm font-medium">
                {(result.relevance_score * 100).toFixed(0)}%
              </span>
            </div>
          </div>
          
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-700 whitespace-pre-wrap">
              {result.content}
            </p>
          </div>
          
          {result.metadata.tags && result.metadata.tags.length > 0 && (
            <div className="mt-3 flex flex-wrap gap-2">
              {result.metadata.tags.map((tag: string, i: number) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default SearchResults;
