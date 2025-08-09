import { useEffect } from 'react';
import LoginPage from './pages/LoginPage';
import { CSRFTokenManager } from './utils/csrf';
import './styles/App.css'

function App() {
  useEffect(() => {
    // Pre-fetch CSRF token when app starts
    const initializeCSRF = async () => {
      try {
        await CSRFTokenManager.fetchCSRFToken();
        console.log('CSRF token initialized successfully');
      } catch (error) {
        console.warn('Failed to initialize CSRF token:', error);
        // Don't block the app if CSRF token fetch fails initially
        // It will be retried when needed
      }
    };
    
    initializeCSRF();
  }, []);

  return (
    <LoginPage />
  )
}

export default App
