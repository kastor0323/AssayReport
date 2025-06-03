import axios from 'axios';
import { SPRING_SERVER_URL } from '../constants/config';

const API_URL = SPRING_SERVER_URL;

const authApi = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Platform': 'web', // 또는 navigator.userAgent 등
  },
  timeout: 15000,
});

authApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

authApi.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 401) {
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('authToken');
      }
    }
    return Promise.reject(error);
  }
);

export const signup = async (user_id, password, name) => {
  return authApi.post('/signup', { user_id, password, name });
};

export const login = async (user_id, password) => {
  return authApi.post('/login', { user_id, password });
};
