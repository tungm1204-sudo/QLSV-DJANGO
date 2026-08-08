import { QueryClient } from '@tanstack/react-query';

// Cấu hình mặc định cho toàn bộ ứng dụng
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data "tươi" trong 5 phút
      retry: 1,
    },
  },
});
