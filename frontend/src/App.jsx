import { Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'sonner';

// Configs
import { queryClient } from './lib/queryClient';
import { routes } from './routes';

// Layout & Guards
import DashboardLayout from './components/layout/DashboardLayout';
import AuthGuard from './routes/AuthGuard';

const GlobalLoading = () => (
  <div className="flex h-screen w-screen items-center justify-center">
    <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
  </div>
);

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Suspense fallback={<GlobalLoading />}>
          <Routes>
            {/* Public Routes */}
            {routes.public.map((route) => (
              <Route key={route.path} path={route.path} element={<route.component />} />
            ))}

            {/* Protected Routes */}
            <Route element={<AuthGuard />}>
              <Route element={<DashboardLayout />}>
                {routes.protected.map((route) => (
                  <Route key={route.path} path={route.path} element={<route.component />} />
                ))}
                
                {/* Fallbacks in protected layout */}
                <Route path="/notifications" element={<div className="p-6">Đang phát triển: Thông báo</div>} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Route>
            </Route>

            {/* Global Fallback */}
            <Route path="*" element={<Navigate to="/login" replace />} />
          </Routes>
        </Suspense>
        <Toaster position="top-right" richColors />
      </BrowserRouter>
    </QueryClientProvider>
  );
}
