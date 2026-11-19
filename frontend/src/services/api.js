import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

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
