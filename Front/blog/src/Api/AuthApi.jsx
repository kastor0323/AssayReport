import axios from 'axios';
import { SPRING_SERVER_URL } from '../constants/config';

const API_URL = SPRING_SERVER_URL;

const authApi = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
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
        localStorage.removeItem('authToken');
        localStorage.removeItem('isLoggedIn');
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const signup = async (user_id, password, name) => {
  console.log(user_id, password, name);
  return authApi.post('/signup', { user_id, password, name });
};

export const login = async (user_id, password) => {
  console.log(user_id, password);
  return authApi.post('/login', { user_id, password });
};

export const postAssay = async (data) => {
  // JWT 토큰은 인터셉터에서 자동으로 추가됨
  return authApi.post('/assay/save', data);
};

export const getAssayList = async () => {
  return authApi.get('/assay/get');
};

export const getAssayDetail = async (record_id) => {
  return authApi.get(`/assay/record/detail/${record_id}`);
};
