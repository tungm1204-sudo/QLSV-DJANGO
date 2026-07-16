import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';

// Layout & Guards
import DashboardLayout from './components/layout/DashboardLayout';
import AuthGuard from './routes/AuthGuard';

// Pages
import LoginPage from './features/auth/LoginPage';
import DashboardPage from './features/dashboard/DashboardPage';
import RolesPage from './features/roles/RolesPage';
import UsersPage from './features/users/UsersPage';

// QueryClient: cấu hình mặc định cho toàn bộ ứng dụng
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Data "tươi" trong 5 phút
      retry: 1,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          {/* Route công khai (không cần đăng nhập) */}
          <Route path="/login" element={<LoginPage />} />

          {/* Route được bảo vệ - phải đăng nhập mới vào được */}
          <Route element={<AuthGuard />}>
            <Route element={<DashboardLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/users" element={<UsersPage />} />
              <Route path="/roles" element={<RolesPage />} />
              <Route path="/audit-logs" element={<div className="p-6">Đang phát triển: Nhật ký</div>} />
              <Route path="/notifications" element={<div className="p-6">Đang phát triển: Thông báo</div>} />
              <Route path="/system-config" element={<div className="p-6">Đang phát triển: Cấu hình</div>} />
              
              {/* Nếu nhập sai URL khi đã đăng nhập -> về dashboard */}
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Route>
          </Route>

          {/* Mọi đường dẫn không khớp ở ngoài (chưa đăng nhập) -> về /login */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
