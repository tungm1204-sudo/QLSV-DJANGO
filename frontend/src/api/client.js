import axios from 'axios';
import useAuthStore from '../stores/useAuthStore';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || `http://${window.location.hostname}:8000/api/v1`;

/**
 * apiClient - Axios instance trung tâm của toàn bộ ứng dụng.
 *
 * Cấu hình:
 * - Request Interceptor: Tự động gắn Access Token vào header Authorization.
 * - Response Interceptor: Khi nhận lỗi 401 (Unauthorized), tự động dùng
 *   Refresh Token để lấy Access Token mới, sau đó thử lại request gốc.
 *   Nếu Refresh Token cũng hết hạn → clearAuth() và chuyển về /login.
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
});

// ─────────────────────────────────────────────
// REQUEST INTERCEPTOR: Gắn Access Token
// ─────────────────────────────────────────────
apiClient.interceptors.request.use(
  (config) => {
    const { accessToken } = useAuthStore.getState();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ─────────────────────────────────────────────
// RESPONSE INTERCEPTOR: Tự động Refresh Token
// ─────────────────────────────────────────────
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      // Fix: Bỏ qua interceptor (không redirect) nếu đang ở bước Đăng nhập
      if (originalRequest.url?.includes('/auth/login/')) {
        return Promise.reject(error);
      }

      if (isRefreshing) {
        // Nếu đang refresh, xếp hàng request này chờ
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      originalRequest._retry = true;
      isRefreshing = true;

      const { setTokens, clearAuth } = useAuthStore.getState();

      try {
        // Fix: Gọi API refresh không cần gửi body vì refresh_token đã nằm trong Cookie
        const response = await axios.post(`${API_BASE_URL}/identity/auth/refresh/`, {}, {
          withCredentials: true
        });

        const newAccessToken = response.data.access;
        setTokens(newAccessToken);
        processQueue(null, newAccessToken);
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        clearAuth();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
