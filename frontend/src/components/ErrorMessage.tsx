import React from 'react';
import { AlertCircle, X } from 'lucide-react';
import { useAppContext } from '../context/AppContext';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  const { setError } = useAppContext();

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start justify-between">
      <div className="flex items-start space-x-3">
        <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
        <div>
          <h3 className="text-sm font-medium text-red-800">Error</h3>
          <p className="text-sm text-red-700 mt-1">{message}</p>
        </div>
      </div>
      <button
        onClick={() => setError(null)}
        className="text-red-600 hover:text-red-800"
      >
        <X className="h-5 w-5" />
      </button>
    </div>
  );
};

export default ErrorMessage;