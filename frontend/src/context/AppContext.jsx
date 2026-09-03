import React, { createContext, useContext, useState, useEffect } from 'react';
import { fetchHealth } from '../services/api';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [systemHealth, setSystemHealth] = useState({
    status: 'checking',
    ai_mode: 'demo',
    model_loaded: false
  });
  const [activeSession, setActiveSession] = useState(null);

  const checkHealth = async () => {
    try {
      const data = await fetchHealth();
      setSystemHealth(data);
    } catch (err) {
      setSystemHealth({
        status: 'offline',
        ai_mode: 'demo',
        model_loaded: false,
        error: err.message
      });
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <AppContext.Provider value={{ systemHealth, checkHealth, activeSession, setActiveSession }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  return useContext(AppContext);
}
