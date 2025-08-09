// Store both access token and username in memory (more secure against XSS)
let accessToken: string | null = null;
let username: string | null = null;

export const setTokens = (accessTokenValue: string): void => {
  // Access token stored in memory
  accessToken = accessTokenValue;
  
  // Refresh token is now handled via HttpOnly cookies by the server
  // No need to store it in localStorage anymore
};

export const getAccessToken = (): string | null => {
  return accessToken;
};

export const setUsername = (usernameValue: string): void => {
  // Store username in memory instead of localStorage to prevent XSS attacks
  username = usernameValue;
};

export const getUsername = (): string | null => {
  return username;
};

export const parseJwt = (token: string | null): any => {
  if (!token) return null;
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

export const isTokenValid = (token: string | null): boolean => {
  const decodedToken = parseJwt(token);
  return decodedToken && decodedToken.exp * 1000 > Date.now();
};

export const clearTokens = (): void => {
  // Clear access token from memory
  accessToken = null;
  
  // Clear username from memory
  username = null;
  
  // Note: Refresh token in HttpOnly cookie will be cleared by server logout endpoint
};
