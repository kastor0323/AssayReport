import axios, { AxiosInstance } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Platform } from 'react-native';
import { SPRING_SERVER_URL } from '../constants/config';

const API_URL = SPRING_SERVER_URL;

const authApi: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Platform': Platform.OS,
  },
  timeout: 15000,
});

// 요청 인터셉터 설정
authApi.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('authToken');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터 설정
authApi.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (axios.isAxiosError(error)) {
      if (error.response && error.response.status === 401) {
        await AsyncStorage.removeItem('isLoggedIn');
        await AsyncStorage.removeItem('authToken');
      }
    }
    return Promise.reject(error);
  }
);

export const signup = async (user_id: string, password: string, name: string) => {
  return authApi.post('/signup', { user_id, password, name});
};

export const login = async (user_id: string, password: string) => {
  return authApi.post('/login', { user_id, password });
}; 