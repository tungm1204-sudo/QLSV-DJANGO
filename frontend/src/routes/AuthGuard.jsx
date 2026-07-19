import { Navigate, Outlet } from 'react-router-dom';
import { useEffect, useState } from 'react';
import useAuthStore from '../features/auth/store/useAuthStore';
import { getMeApi } from '../api/auth';
import { toast } from 'sonner';

/**
 * AuthGuard - Bảo vệ các route yêu cầu đăng nhập.
 * Nếu chưa có accessToken, tự động chuyển hướng về /login.
 * Tự động fetch lại thông tin user nếu accessToken có nhưng user đang rỗng (do F5).
 */
export default function AuthGuard() {
  const { isAuthenticated, user, setUser, clearAuth } = useAuthStore();
  const [isFetching, setIsFetching] = useState(isAuthenticated && !user);

  useEffect(() => {
    if (isAuthenticated && !user) {
      getMeApi()
        .then((res) => {
          setUser(res.data);
        })
        .catch(() => {
          toast.error('Phiên đăng nhập hết hạn hoặc lỗi xác thực');
          clearAuth();
        })
        .finally(() => {
          setIsFetching(false);
        });
    } else {
      setIsFetching(false);
    }
  }, [isAuthenticated, user, setUser, clearAuth]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (isFetching) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  return <Outlet />;
}
