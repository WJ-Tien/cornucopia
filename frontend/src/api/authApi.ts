import axios from 'axios';
import settings from '../api_configs/configs'; // ✅ 從設定檔匯入

interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: 'bearer';
}

// 使用匯入的設定來建立 Axios 實例
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
      throw new Error(error.response.data?.detail || '登入時發生未知錯誤');
    }
    throw new Error('登入時發生網路或客戶端錯誤');
  }
};