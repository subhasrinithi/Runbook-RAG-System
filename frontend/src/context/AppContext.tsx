import React, { createContext, useContext, useState, ReactNode } from 'react';

interface Playbook {
  title: string;
  summary: string;
  steps: PlaybookStep[];
  estimated_time: string;
  risk_level: string;
}

interface PlaybookStep {
  step_number: number;
  action: string;
  command: string | null;
  expected_outcome: string;
  verification: string | null;
}

interface SearchResult {
  content: string;
  metadata: Record<string, any>;
  chunk_id: string;
  relevance_score: number;
}

interface AppContextType {
  playbook: Playbook | null;
  setPlaybook: (playbook: Playbook | null) => void;
  searchResults: SearchResult[];
  setSearchResults: (results: SearchResult[]) => void;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [playbook, setPlaybook] = useState<Playbook | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  return (
    <AppContext.Provider
      value={{
        playbook,
        setPlaybook,
        searchResults,
        setSearchResults,
        isLoading,
        setIsLoading,
        error,
        setError,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};