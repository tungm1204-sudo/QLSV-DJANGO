import { useState, useRef, useEffect } from 'react';
import { Bell, Search, Menu, User, LogOut, Settings, MonitorSmartphone, CheckCircle2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import useAuthStore from '../../features/auth/store/useAuthStore';
import { logoutApi } from '../../api/auth';
import SessionManagement from '../../features/auth/SessionManagement';
import { cn } from '../../utils/index';

export default function Header() {
  const navigate = useNavigate();
  const { user, refreshToken, clearAuth } = useAuthStore();
  const [isNotifOpen, setIsNotifOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showSessions, setShowSessions] = useState(false);
  const [visibleCount, setVisibleCount] = useState(2);
  const notifRef = useRef(null);
  const userMenuRef = useRef(null);

  const logoutMutation = useMutation({
    mutationFn: () => logoutApi(refreshToken),
    onSettled: () => {
      clearAuth();
      navigate('/login', { replace: true });
    },
  });

  useEffect(() => {
    function handleClickOutside(event) {
      if (notifRef.current && !notifRef.current.contains(event.target)) {
        setIsNotifOpen(false);
      }
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setShowUserMenu(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // 5 thông báo giả lập để test tính năng "Xem thêm"
  const allNotifications = [
    { id: 1, title: 'Đăng nhập thành công', desc: 'Thiết bị mới vừa đăng nhập vào tài khoản của bạn.', time: 'Vừa xong', unread: true },
    { id: 2, title: 'Hệ thống cập nhật', desc: 'Bản vá bảo mật v1.0.2 đã được cài đặt tự động.', time: '2 giờ trước', unread: false },
    { id: 3, title: 'Sinh viên mới', desc: 'Có 5 sinh viên vừa được thêm vào lớp CNTT_01.', time: '5 giờ trước', unread: true },
    { id: 4, title: 'Cảnh báo hệ thống', desc: 'Tải CPU đang ở mức cao (85%).', time: '1 ngày trước', unread: false },
    { id: 5, title: 'Báo cáo tháng', desc: 'Báo cáo điểm danh tháng 6 đã sẵn sàng.', time: '2 ngày trước', unread: false },
  ];

  const displayedNotifications = allNotifications.slice(0, visibleCount);
  const hasMore = visibleCount < allNotifications.length;

  return (
    <header className="flex items-center justify-between px-6 py-4 bg-white border-b border-slate-200 shrink-0 sticky top-0 z-50">
      {/* Search Bar */}
      <div className="flex-1 max-w-md">
        <div className="relative group">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-4 w-4 text-slate-400 group-focus-within:text-blue-600 transition-colors" />
          </div>
          <input
            type="text"
            className="block w-full pl-10 pr-3 py-2 border border-slate-200 rounded-lg leading-5 bg-slate-50 placeholder-slate-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition-all sm:text-sm shadow-sm"
            placeholder="Tìm kiếm nhanh (Nhấn '/' để focus)..."
          />
        </div>
      </div>

      {/* Right Side Actions */}
      <div className="flex items-center gap-4 pl-4">
        {/* Notification Bell */}
        <div className="relative" ref={notifRef}>
          <button
            onClick={() => setIsNotifOpen(!isNotifOpen)}
            className="relative p-2 text-slate-500 hover:bg-slate-100 hover:text-slate-900 rounded-lg transition-colors focus:outline-none"
          >
            <Bell size={20} />
            <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-blue-600 rounded-full ring-2 ring-white"></span>
          </button>

          {/* Notification Dropdown */}
          {isNotifOpen && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-slate-200 overflow-hidden animate-in fade-in slide-in-from-top-2 duration-200 z-50">
              <div className="flex items-center justify-between px-4 py-3 border-b border-slate-100 bg-white/50 backdrop-blur-sm sticky top-0">
                <span className="font-semibold text-slate-900">Thông báo</span>
                <button className="text-xs font-medium text-blue-600 hover:text-blue-700 transition-colors">Đánh dấu đã đọc</button>
              </div>
              <div className="max-h-[28rem] overflow-y-auto">
                {displayedNotifications.map((n) => (
                  <div key={n.id} className={cn(
                    "px-4 py-3 cursor-pointer border-b border-slate-100 last:border-0 transition-colors hover:bg-slate-50 group",
                    n.unread ? "bg-blue-50/30" : "bg-white"
                  )}>
                    <div className="flex gap-3">
                      <div className="mt-0.5">
                        <CheckCircle2 size={16} className={cn("transition-colors", n.unread ? "text-blue-600" : "text-slate-300 group-hover:text-slate-400")} />
                      </div>
                      <div>
                        <p className={cn("text-sm transition-colors", n.unread ? "font-semibold text-slate-900" : "font-medium text-slate-600 group-hover:text-slate-900")}>{n.title}</p>
                        <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{n.desc}</p>
                        <span className="text-[10px] font-medium text-slate-400 mt-1 block">{n.time}</span>
                      </div>
                    </div>
                  </div>
                ))}
                
                {/* Nút Xem thêm không chuyển trang, chỉ mở rộng list */}
                {hasMore && (
                  <div className="px-4 py-3 text-center border-t border-slate-100 bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer"
                       onClick={() => setVisibleCount(prev => prev + 3)}>
                    <button className="text-xs font-semibold text-slate-600 hover:text-slate-900">
                      Xem thêm thông báo
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="w-px h-6 bg-slate-200 hidden sm:block"></div>

        {/* User Profile & Dropdown */}
        <div className="relative" ref={userMenuRef}>
          <button 
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center gap-3 hover:bg-slate-50 p-1.5 rounded-xl transition-colors text-left"
          >
            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-50 text-blue-600 border border-blue-100 shadow-sm shrink-0">
              <User size={16} />
            </div>
            <div className="hidden sm:block">
              <p className="text-sm font-semibold text-slate-900 leading-tight">{user?.full_name || 'Người dùng'}</p>
              <p className="text-xs font-medium text-slate-500">{user?.role?.name || 'Chưa phân quyền'}</p>
            </div>
          </button>

          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-100 overflow-hidden z-50 animate-in fade-in slide-in-from-top-2 duration-200">
              <div className="p-3 border-b border-slate-50">
                <p className="text-sm font-semibold text-slate-900">{user?.full_name}</p>
                <p className="text-xs text-slate-500 truncate max-w-[180px]">{user?.email}</p>
                <p className="text-xs font-medium text-blue-600 truncate max-w-[180px] mt-0.5">{user?.role?.name || 'Chưa phân quyền'}</p>
              </div>
              
              <div className="p-1.5">
                <button 
                  onClick={() => {
                    setShowUserMenu(false);
                    setShowSessions(true);
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-lg transition-colors"
                >
                  <MonitorSmartphone size={16} />
                  Thiết bị đăng nhập
                </button>
                <button 
                  className="w-full flex items-center gap-3 px-3 py-2 text-sm font-medium text-slate-600 hover:text-slate-900 hover:bg-slate-50 rounded-lg transition-colors"
                >
                  <Settings size={16} />
                  Cài đặt tài khoản
                </button>
              </div>

              <div className="p-1.5 border-t border-slate-50">
                <button 
                  onClick={() => {
                    setShowUserMenu(false);
                    logoutMutation.mutate();
                  }}
                  disabled={logoutMutation.isPending}
                  className="w-full flex items-center gap-3 px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                >
                  <LogOut size={16} />
                  Đăng xuất
                </button>
              </div>
            </div>
          )}
        </div>
      </div>

      <SessionManagement 
        isOpen={showSessions} 
        onClose={() => setShowSessions(false)} 
      />
    </header>
  );
}
