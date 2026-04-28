import axios from 'axios';
import toast from 'react-hot-toast';

// Get API URL from environment or use current domain
const getApiUrl = () => {
  // In production, use the same domain
  if (import.meta.env.PROD) {
    return '/api';  // This will call the same domain's /api endpoint
  }
  // In development, use local backend
  return import.meta.env.VITE_API_URL || 'http://localhost:8000/api';
};

const API_URL = getApiUrl();

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor - add token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Handle 401 Unauthorized
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          const { access_token } = response.data;
          localStorage.setItem('access_token', access_token);
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      }
    }

    // Handle other errors
    if (error.response?.status === 403) {
      toast.error('You don\'t have permission to perform this action');
    } else if (error.response?.status === 404) {
      console.error('Endpoint not found:', error.config?.url);
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.');
    }

    return Promise.reject(error);
  }
);

// API Methods
export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
};

export const calendarAPI = {
  getEvents: (month, year) => api.get('/calendar/events', { params: { month, year } }),
  createEvent: (data) => api.post('/calendar/events', data),
  updateEvent: (id, data) => api.put(`/calendar/events/${id}`, data),
  deleteEvent: (id) => api.delete(`/calendar/events/${id}`),
};

export const feedAPI = {
  getPosts: (limit = 20) => api.get('/feed/posts', { params: { limit } }),
  getPost: (id) => api.get(`/feed/posts/${id}`),
  createPost: (data) => api.post('/feed/posts', data),
  likePost: (id) => api.post(`/feed/posts/${id}/like`),
  commentOnPost: (id, comment) => api.post(`/feed/posts/${id}/comment`, { comment }),
  sharePost: (id) => api.post(`/feed/posts/${id}/share`),
};

export const chatAPI = {
  getGroups: () => api.get('/chat/groups'),
  getMessages: (groupId, limit = 50) => api.get(`/chat/messages/${groupId}`, { params: { limit } }),
  sendMessage: (data) => api.post('/chat/messages', data),
  getConversations: () => api.get('/chat/conversations'),
  getPrivateMessages: (userId, limit = 50) => api.get(`/chat/messages/private/${userId}`, { params: { limit } }),
  sendPrivateMessage: (data) => api.post('/chat/messages/private', data),
};

export const quarterlyAPI = {
  getShares: () => api.get('/quarterly/shares'),
  forwardShare: (shareId) => api.post(`/quarterly/share/${shareId}/forward`),
};

export const profileAPI = {
  getProfile: () => api.get('/profile/me'),
  updateProfile: (data) => api.put('/profile/me', data),
  getParishMembers: () => api.get('/profile/parish-members'),
  uploadAvatar: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/profile/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const adminAPI = {
  getUsers: () => api.get('/admin/users'),
  assignRole: (userId, role) => api.put(`/admin/users/${userId}/role`, { role }),
  activateUser: (userId) => api.put(`/admin/users/${userId}/activate`),
};

export default api;
