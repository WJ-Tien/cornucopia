import axios from 'axios';
import settings from '../../../api_configs/configs';
import * as tokenService from './tokenService';
import { CSRFTokenManager } from '../../../utils/csrf';

interface LoginResponse {
  access_token: string;
  token_type: 'bearer';
  username?: string;
}

interface RefreshResponse {
  access_token: string;
  token_type: 'bearer';
}

// Create axios instance with secure defaults
const apiClient = axios.create({
  baseURL: settings.apiBaseUrl,
  timeout: 10000,
  withCredentials: true,  // Allow cookies for refresh token
});

// Request interceptor to add Authorization header and CSRF token
apiClient.interceptors.request.use(
  async (config) => {
    const token = tokenService.getAccessToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // Add CSRF token for state-changing requests
    if (['post', 'put', 'patch', 'delete'].includes(config.method?.toLowerCase() || '')) {
      try {
        const csrfToken = await CSRFTokenManager.getToken();
        config.headers['X-CSRF-Token'] = csrfToken;
      } catch (error) {
        console.error('Failed to get CSRF token:', error);
        // For critical operations like login, we should fail if we can't get CSRF token
        if (config.url?.includes('/login') || config.url?.includes('/register')) {
          throw new Error('Unable to obtain CSRF token for security. Please refresh the page and try again.');
        }
        // For other requests, try to fetch a new CSRF token
        try {
          const csrfToken = await CSRFTokenManager.refreshToken();
          config.headers['X-CSRF-Token'] = csrfToken;
        } catch (csrfError) {
          console.error('Failed to refresh CSRF token:', csrfError);
          throw new Error('Security token unavailable. Please refresh the page and try again.');
        }
      }
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for automatic token refresh and CSRF retry
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized (token expired)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // Try to refresh token using HttpOnly cookie
        const refreshResponse = await axios.post<RefreshResponse>(
          `${settings.apiBaseUrl}/cornucopia/user/refresh`,
          {},  // Empty body
          {
            withCredentials: true,  // Send HttpOnly refresh token cookie
            timeout: 10000
          }
        );
        
        // Store new access token in memory
        tokenService.setTokens(refreshResponse.data.access_token);
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access_token}`;
        return apiClient(originalRequest);
        
      } catch (refreshError) {
        // Refresh failed, user needs to login again
        tokenService.clearTokens();
        window.location.href = '/login';  // Redirect to login
        return Promise.reject(refreshError);
      }
    }
    
    // Handle 403 Forbidden (CSRF token invalid/missing)
    if (error.response?.status === 403 && !originalRequest._csrfRetry) {
      const errorMessage = error.response?.data?.detail || '';
      if (errorMessage.toLowerCase().includes('csrf')) {
        originalRequest._csrfRetry = true;
        
        try {
          console.log('CSRF token validation failed, refreshing...');
          // Refresh CSRF token and retry
          const newCsrfToken = await CSRFTokenManager.refreshToken();
          originalRequest.headers['X-CSRF-Token'] = newCsrfToken;
          console.log('CSRF token refreshed, retrying request...');
          return apiClient(originalRequest);
        } catch (csrfError) {
          console.error('Failed to refresh CSRF token after 403:', csrfError);
          // Don't throw the CSRF error, throw the original 403 error
          return Promise.reject(error);
        }
      }
    }
    
    return Promise.reject(error);
  }
);

export const loginUser = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  try {
    const response = await apiClient.post<LoginResponse>('/cornucopia/user/login', {
      username,
      password,
    });
    
    // Store access token in memory
    tokenService.setTokens(response.data.access_token);
    
    // Store username for UI display
    if (response.data.username) {
      tokenService.setUsername(response.data.username);
    } else {
      tokenService.setUsername(username);
    }
    
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data?.detail || 'Login failed');
    }
    throw new Error('Network or client error occurred');
  }
};

export const logoutUser = async (): Promise<void> => {
  try {
    // Call server logout to clear HttpOnly cookie
    await apiClient.post('/cornucopia/user/logout');
  } catch (error) {
    // Even if server logout fails, clear client tokens
    console.warn('Server logout failed, clearing client tokens anyway');
  } finally {
    // Clear client-side tokens
    tokenService.clearTokens();
  }
};

export const refreshToken = async (): Promise<RefreshResponse> => {
  const response = await axios.post<RefreshResponse>(
    `${settings.apiBaseUrl}/cornucopia/user/refresh`,
    {},
    { withCredentials: true, timeout: 10000 }
  );
  
  tokenService.setTokens(response.data.access_token);
  return response.data;
};

// Export the configured axios instance for other API calls
export { apiClient };
