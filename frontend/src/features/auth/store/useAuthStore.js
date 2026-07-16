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
      refreshToken: null,
      user: null,

      // Gọi sau khi đăng nhập thành công
      setTokens: (accessToken, refreshToken) =>
        set({ accessToken, refreshToken }),

      // Gọi sau khi lấy được thông tin user
      setUser: (user) => set({ user }),

      // Gọi khi đăng xuất hoặc token hết hạn không thể refresh
      clearAuth: () =>
        set({ accessToken: null, refreshToken: null, user: null }),
    }),
    {
      name: 'qlsv-auth-storage',
      storage: createJSONStorage(() => localStorage),
      // Chỉ persist token, không persist user để re-fetch mỗi lần
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
      }),
    }
  )
);

export default useAuthStore;
