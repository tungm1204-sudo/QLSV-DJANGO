import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

/**
 * useAuthStore - Global state cho xác thực (Authentication).
 * Lưu trữ: Access Token, Refresh Token, User Profile.
 * Dùng middleware `persist` để lưu vào localStorage, giúp user
 * không bị đăng xuất khi refresh trang.
 */
const useAuthStore = create(
  persist(
    (set) => ({
      accessToken: null,
      user: null,
      isAuthenticated: false,

      // Gọi sau khi đăng nhập thành công
      setTokens: (accessToken) =>
        set({ accessToken, isAuthenticated: true }),

      // Gọi sau khi lấy được thông tin user
      setUser: (user) => set({ user }),

      // Gọi khi đăng xuất hoặc token hết hạn không thể refresh
      clearAuth: () =>
        set({ accessToken: null, user: null, isAuthenticated: false }),
    }),
    {
      name: 'qlsv-auth-storage',
      storage: createJSONStorage(() => localStorage),
      // Fix: Chỉ persist cờ isAuthenticated để biết user đã đăng nhập, không persist accessToken để tránh XSS.
      // Dùng hàm trung gian tạo cờ thay vì lưu trực tiếp.
      partialize: (state) => ({
        isAuthenticated: state.isAuthenticated,
      }),
      merge: (persistedState, currentState) => {
        // Merge state: Nếu có cờ isAuthenticated = true thì đánh dấu là có thể đang login.
        // Nhưng access_token vẫn = null cho đến khi gọi refresh_token.
        return {
          ...currentState,
          ...persistedState,
        }
      }
    }
  )
);

export default useAuthStore;
