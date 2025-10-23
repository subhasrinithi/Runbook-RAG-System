import React from 'react';
import { CheckCircle, AlertTriangle, Clock, Shield } from 'lucide-react';

interface PlaybookStep {
  step_number: number;
  action: string;
  command: string | null;
  expected_outcome: string;
  verification: string | null;
}

interface Playbook {
  title: string;
  summary: string;
  steps: PlaybookStep[];
  estimated_time: string;
  risk_level: string;
}

interface PlaybookDisplayProps {
  playbook: Playbook;
}

const PlaybookDisplay: React.FC<PlaybookDisplayProps> = ({ playbook }) => {
  const getRiskColor = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'critical':
        return 'text-red-600 bg-red-100';
      case 'high':
        return 'text-orange-600 bg-orange-100';
      case 'medium':
        return 'text-yellow-600 bg-yellow-100';
      case 'low':
        return 'text-green-600 bg-green-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          {playbook.title}
        </h2>
        <p className="text-gray-600">{playbook.summary}</p>
      </div>

      <div className="flex items-center space-x-6 text-sm">
        <div className="flex items-center space-x-2">
          <Clock className="h-5 w-5 text-gray-400" />
          <span className="text-gray-700">
            <span className="font-medium">Estimated Time:</span> {playbook.estimated_time}
          </span>
        </div>
        
        <div className="flex items-center space-x-2">
          <Shield className="h-5 w-5 text-gray-400" />
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getRiskColor(playbook.risk_level)}`}>
            {playbook.risk_level} Risk
          </span>
        </div>
      </div>

      <div className="space-y-4">
        {playbook.steps.map((step) => (
          <div
            key={step.step_number}
            className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0">
                <div className="h-8 w-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center font-semibold">
                  {step.step_number}
                </div>
              </div>
              
              <div className="flex-1 space-y-3">
                <h3 className="text-lg font-semibold text-gray-900">
                  {step.action}
                </h3>
                
                {step.command && (
                  <div className="bg-gray-900 rounded-lg p-3">
                    <code className="text-sm text-green-400 font-mono">
                      {step.command}
                    </code>
                  </div>
                )}
                
                <div className="space-y-2">
                  <div className="flex items-start space-x-2">
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-gray-700">Expected Outcome:</p>
                      <p className="text-sm text-gray-600">{step.expected_outcome}</p>
                    </div>
                  </div>
                  
                  {step.verification && (
                    <div className="flex items-start space-x-2">
                      <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-gray-700">Verification:</p>
                        <p className="text-sm text-gray-600">{step.verification}</p>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PlaybookDisplay;