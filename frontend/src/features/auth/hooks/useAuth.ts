import { useState, useEffect } from 'react';
import * as tokenService from './tokenService';
import { loginUser, logoutUser } from './secureAuthApi';

export const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [username, setUsername] = useState<string | null>(null);

  const handleLogout = async () => {
    try {
      await logoutUser();
    } catch (error) {
      console.warn('Logout error:', error);
    }
    setUsername(null);
    setIsLoggedIn(false);
    setError('');
  };
  
  useEffect(() => {
    const token = tokenService.getAccessToken();

    if (token && tokenService.isTokenValid(token)) {
      const decodedToken = tokenService.parseJwt(token);
      setIsLoggedIn(true);
      
      // Get username from memory first, if not available, get from token
      const storedUsername = tokenService.getUsername();
      const tokenUsername = decodedToken.username || decodedToken.sub || 'User';
      
      if (!storedUsername) {
        // If username not in memory (e.g., after page refresh), set it from token
        tokenService.setUsername(tokenUsername);
      }
      
      setUsername(storedUsername || tokenUsername);
    } else {
      handleLogout();
    }
  }, []);

  const handleLogin = async (usernameInput: string, passwordInput: string) => {
    setLoading(true);
    setError('');
    try {
      await loginUser(usernameInput, passwordInput);
      // Access token is already stored in memory by loginUser
      // Refresh token is stored in HttpOnly cookie by server
      // Username is also stored in memory by loginUser
      setUsername(usernameInput);
      setIsLoggedIn(true);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('Unknown error occurred during login');
      }
    } finally {
      setLoading(false);
    }
  };

  return { isLoggedIn, loading, error, username, handleLogin, handleLogout };
};
