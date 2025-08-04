import { useState, useEffect } from 'react';
import * as tokenService from './tokenService';
import { loginUser } from './authApi';

export const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [username, setUsername] = useState<string | null>(null);

  const handleLogout = () => {
    tokenService.clearTokens();
    setUsername(null);
    setIsLoggedIn(false);
    setError('');
  };
  
  useEffect(() => {
    const token = tokenService.getAccessToken();

    if (token && tokenService.isTokenValid(token)) {
      const decodedToken = tokenService.parseJwt(token);
      setIsLoggedIn(true);
      setUsername(decodedToken.username || decodedToken.sub || 'User');
    } else {
      handleLogout();
    }
  }, []);

  const handleLogin = async (usernameInput: string, passwordInput: string) => {
    setLoading(true);
    setError('');
    try {
      const data = await loginUser(usernameInput, passwordInput);
      tokenService.setTokens(data.access_token, data.refresh_token);
      tokenService.setUsername(usernameInput);
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
