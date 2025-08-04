const ACCESS_TOKEN_KEY = 'cornucopia_access_token';
const REFRESH_TOKEN_KEY = 'cornucopia_refresh_token';
const USERNAME_KEY = 'cornucopia_username';

export const setTokens = (accessToken: string, refreshToken: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  }
};

export const getAccessToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

export const setUsername = (username: string): void => {
    localStorage.setItem(USERNAME_KEY, username);
};

export const getUsername = (): string | null => {
    return localStorage.getItem(USERNAME_KEY);
};

export const clearTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USERNAME_KEY);
};