import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

/**
 * DashboardLayout - Khung bố cục chung cho toàn bộ ứng dụng sau khi đăng nhập.
 * Bao gồm: Sidebar (menu trái) + Header (trên cùng) + Outlet (nội dung trang hiện tại).
 */
export default function DashboardLayout() {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50 font-sans">
      <Sidebar />

      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />

        {/* Vùng nội dung chính */}
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
