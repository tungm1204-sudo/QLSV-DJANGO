import { create } from 'zustand';
import api from '../api/axiosClient';
import { jwtDecode } from 'jwt-decode';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true, // initial load check

  login: async (username, password) => {
    try {
      const response = await api.post('/auth/login/', { username, password });
      const { access, refresh } = response.data;
      
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      
      // Decode JWT for basic user info, then optionally fetch full profile
      const decoded = jwtDecode(access);
      set({ 
        user: { 
          id: decoded.user_id, 
          role: decoded.role, 
          fullName: decoded.full_name,
          email: decoded.email
        }, 
        isAuthenticated: true 
      });
      return true;
    } catch (error) {
      console.error("Login failed", error);
      throw error;
    }
  },

  logout: async () => {
    try {
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        await api.post('/auth/logout/', { refresh });
      }
    } catch(e) {
      // ignore
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      set({ user: null, isAuthenticated: false });
    }
  },

  checkAuth: () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ user: null, isAuthenticated: false, isLoading: false });
      return;
    }
    
    try {
      const decoded = jwtDecode(token);
      // Check if expired
      if (decoded.exp * 1000 < Date.now()) {
        // Will refresh natively via interceptor on next call, or we could proactively refresh here
        set({ user: null, isAuthenticated: false, isLoading: false });
        return;
      }
      
      set({ 
        user: { 
          id: decoded.user_id, 
          role: decoded.role, 
          fullName: decoded.full_name,
          email: decoded.email
        }, 
        isAuthenticated: true,
        isLoading: false
      });
    } catch (e) {
      set({ user: null, isAuthenticated: false, isLoading: false });
    }
  }
}));

// Setup global listener to handle token refresh failures
window.addEventListener('auth:logout', () => {
  useAuthStore.getState().logout();
});
