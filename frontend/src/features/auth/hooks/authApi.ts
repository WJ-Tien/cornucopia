import axios from 'axios';
import settings from '../../../api_configs/configs';

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

const apiClient = axios.create({
  baseURL: settings.apiBaseUrl, 
  timeout: 10000,
});

export const loginUser = async (
  username: string,
  password: string
): Promise<LoginResponse> => {
  try {
    const response = await apiClient.post<LoginResponse>('/cornucopia/user/login', {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data?.detail || 'Unknown error');
    }
    throw new Error('Network or client error occurred');
  }
};