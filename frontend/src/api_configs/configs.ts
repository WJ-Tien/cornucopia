// src/core/config.ts

// 從 Vite 的特殊環境變數中讀取 API 的基礎 URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

if (!API_BASE_URL) {
  throw new Error("VITE_API_BASE_URL is not defined. Please set it in your .env file.");
}

const settings = {
  apiBaseUrl: API_BASE_URL,
};

export default settings;
