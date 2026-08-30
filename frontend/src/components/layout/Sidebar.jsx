import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Shield, FileText, Settings, Bell, ChevronLeft, ChevronRight, GraduationCap, Database, BookOpen, CalendarDays } from 'lucide-react';
import { useState } from 'react';
import { usePermissions } from '../../hooks/usePermissions';
import { cn } from '../../utils/index';

const menuItems = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'Tổng quan' },
  { path: '/master-data', icon: Database, label: 'Danh mục gốc', requiredPerm: null }, // Mọi người đều có thể xem tạm thời
  { path: '/curriculum/courses', icon: BookOpen, label: 'Quản lý Môn học', requiredPerm: null }, // Tạm thời để null
  { path: '/curriculum/training-programs', icon: FileText, label: 'Quản lý Khung ĐT', requiredPerm: null },
  { path: '/curriculum/training-plans', icon: CalendarDays, label: 'Kế hoạch Đào tạo', requiredPerm: null },
  { path: '/hr', icon: Users, label: 'Nhân sự', requiredPerm: 'HR_VIEW' },
  { path: '/users', icon: Shield, label: 'Người dùng', requiredPerm: 'USERS_VIEW' },
  { path: '/roles', icon: Shield, label: 'Phân quyền', requiredPerm: 'ROLES_VIEW' },
  { path: '/audit-logs', icon: FileText, label: 'Nhật ký', requiredPerm: 'AUDIT_VIEW' },
  { path: '/notifications', icon: Bell, label: 'Thông báo', requiredPerm: 'NOTIF_VIEW' },
  { path: '/system-config', icon: Settings, label: 'Cấu hình', requiredPerm: 'SYSTEM_VIEW' },
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const { hasPermission } = usePermissions();

  const visibleMenuItems = menuItems.filter(item => {
    if (!item.requiredPerm) return true;
    return hasPermission(item.requiredPerm);
  });

  return (
    <aside
      className={cn(
        'relative flex flex-col h-screen bg-slate-900 text-slate-100 transition-all duration-300 ease-in-out shrink-0 border-r border-slate-800',
        collapsed ? 'w-16' : 'w-60'
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-slate-800/50">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-slate-800 border border-slate-700 shrink-0 shadow-sm">
          <GraduationCap size={18} className="text-slate-100" />
        </div>
        {!collapsed && (
          <span className="font-bold text-lg tracking-tight whitespace-nowrap animate-in fade-in">
            QLSV Admin
          </span>
        )}
      </div>

      {/* Menu Links */}
      <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
        {visibleMenuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            title={collapsed ? item.label : undefined}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-blue-600 text-white shadow-sm shadow-blue-900/20'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-100'
              )
            }
          >
            <item.icon size={18} className={cn("shrink-0")} />
            {!collapsed && <span className="whitespace-nowrap animate-in fade-in">{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      {/* Collapse Button */}
      <button
        onClick={() => setCollapsed((prev) => !prev)}
        className="absolute -right-3 top-20 z-10 flex items-center justify-center w-6 h-6 rounded-full bg-slate-900 border border-slate-700 text-slate-400 hover:bg-blue-600 hover:text-white transition-colors shadow-sm ring-2 ring-slate-50"
      >
        {collapsed ? <ChevronRight size={12} strokeWidth={3} /> : <ChevronLeft size={12} strokeWidth={3} />}
      </button>

      {/* Footer Info */}
      {!collapsed && (
        <div className="p-4 border-t border-slate-800/50">
          <p className="text-xs font-medium text-slate-500 truncate">v1.0.0-beta</p>
        </div>
      )}
    </aside>
  );
}
