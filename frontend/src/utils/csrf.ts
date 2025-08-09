// CSRF Token Management for frontend
import settings from '../api_configs/configs';

export class CSRFTokenManager {
  private static token: string | null = null;
  
  /**
   * Fetch CSRF token from server
   */
  static async fetchCSRFToken(): Promise<string> {
    try {
      // Use the configured API base URL instead of relative path
      const csrfUrl = `${settings.apiBaseUrl}/cornucopia/security/csrf-token`;
      
      const response = await fetch(csrfUrl, {
        method: 'GET',
        credentials: 'include', // Include cookies
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error('CSRF token fetch failed:', {
          status: response.status,
          statusText: response.statusText,
          url: response.url,
          errorText: errorText.substring(0, 200)
        });
        
        if (response.status === 404) {
          throw new Error('CSRF endpoint not found. Please check if the backend server is running on the correct port.');
        }
        
        throw new Error(`Failed to fetch CSRF token: ${response.status} ${response.statusText}`);
      }
      
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const responseText = await response.text();
        console.error('CSRF token endpoint returned non-JSON:', responseText.substring(0, 200));
        throw new Error('CSRF token endpoint returned non-JSON response');
      }
      
      const data = await response.json();
      this.token = data.csrf_token;
      
      if (!this.token) {
        throw new Error('CSRF token is empty');
      }
      
      console.log('CSRF token fetched successfully');
      return this.token;
    } catch (error) {
      if (error instanceof Error) {
        console.error('Error fetching CSRF token:', error.message);
      } else {
        console.error('Error fetching CSRF token:', error);
      }
      throw error;
    }
  }
  
  /**
   * Get current CSRF token, fetch if not available
   */
  static async getToken(): Promise<string> {
    if (!this.token) {
      await this.fetchCSRFToken();
    }
    
    if (!this.token) {
      throw new Error('Failed to obtain CSRF token');
    }
    
    return this.token;
  }
  
  /**
   * Create headers with CSRF token
   */
  static async getHeaders(): Promise<Record<string, string>> {
    const token = await this.getToken();
    return {
      'Content-Type': 'application/json',
      'X-CSRF-Token': token,
    };
  }
  
  /**
   * Refresh CSRF token (call this if you get 403 CSRF errors)
   */
  static async refreshToken(): Promise<string> {
    this.token = null;
    return await this.fetchCSRFToken();
  }
}
