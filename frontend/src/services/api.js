import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
const TOKEN_KEY = 'kisanmitra_auth_token';

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const setToken = (token) => {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
};
export const removeToken = () => localStorage.removeItem(TOKEN_KEY);

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
});

// Automatically inject Authorization Bearer token if present
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authAPI = {
  signup: async (data) => {
    const response = await apiClient.post('/auth/signup', data);
    if (response.data?.token) {
      setToken(response.data.token);
    }
    return response.data;
  },

  login: async (data) => {
    const response = await apiClient.post('/auth/login', data);
    if (response.data?.token) {
      setToken(response.data.token);
    }
    return response.data;
  },

  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } catch (e) {
      // Continue cleanup even if server network error
    } finally {
      removeToken();
    }
  },

  updateProfile: async (data) => {
    const response = await apiClient.put('/auth/profile', data);
    return response.data;
  },

  forgotPassword: async (channel, identifier) => {
    const response = await apiClient.post('/auth/forgot-password', {
      channel,
      identifier,
    });
    return response.data;
  },

  verifyOtp: async (identifier, otp_code) => {
    const response = await apiClient.post('/auth/verify-otp', {
      identifier,
      otp_code,
    });
    return response.data;
  },

  resetPassword: async (reset_token, new_password) => {
    const response = await apiClient.post('/auth/reset-password', {
      reset_token,
      new_password,
    });
    return response.data;
  },
};

export const chatAPI = {
  sendMessage: async (message, language, district, crop, conversationId) => {
    const response = await apiClient.post('/chat', {
      message,
      language,
      district,
      crop,
      conversation_id: conversationId,
    });
    return response.data;
  },

  getConversations: async () => {
    const response = await apiClient.get('/conversations');
    return response.data;
  },

  getConversationMessages: async (conversationId) => {
    const response = await apiClient.get(`/conversations/${conversationId}`);
    return response.data;
  },

  deleteConversation: async (conversationId) => {
    const response = await apiClient.delete(`/conversations/${conversationId}`);
    return response.data;
  },

  getCrops: async () => {
    const response = await apiClient.get('/crops');
    return response.data;
  },

  getDistricts: async () => {
    const response = await apiClient.get('/districts');
    return response.data;
  },

  getSchemes: async (language = 'en') => {
    const response = await apiClient.get('/schemes', { params: { language } });
    return response.data;
  },

  getWeather: async (district) => {
    const response = await apiClient.get('/weather', { params: { district } });
    return response.data;
  },

  getHealth: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },
};

export default apiClient;
