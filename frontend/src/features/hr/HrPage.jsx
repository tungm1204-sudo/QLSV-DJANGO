import { Routes, Route, Navigate, NavLink, Outlet, useLocation } from 'react-router-dom';
import { Users, GraduationCap, Briefcase, Contact } from 'lucide-react';
import { cn } from '../../utils';
import HrPageHeader from './components/HrPageHeader';
import StudentListPage from './students/pages/StudentListPage';
import StudentFormPage from './students/pages/StudentFormPage';
import StudentDetailPage from './students/pages/StudentDetailPage';
import LecturerListPage from './lecturers/pages/LecturerListPage';
import LecturerFormPage from './lecturers/pages/LecturerFormPage';
import LecturerDetailPage from './lecturers/pages/LecturerDetailPage';

// Tạm thời các Page chưa implement, ta sẽ dùng placeholder
const Placeholder = ({ title }) => (
  <div className="flex h-64 items-center justify-center text-slate-500 bg-white rounded-xl border border-slate-200 mt-6 shadow-sm">
    <div className="text-center">
      <h3 className="text-lg font-medium text-slate-900 mb-2">{title}</h3>
      <p>Đang phát triển module này...</p>
    </div>
  </div>
);

// Tab Navigation Component
function HrTabs() {
  const tabs = [
    { name: 'Sinh viên', path: '/hr/students', icon: GraduationCap },
    { name: 'Giảng viên', path: '/hr/lecturers', icon: Briefcase },
    { name: 'Cán bộ / Nhân viên', path: '/hr/staffs', icon: Contact },
  ];

  return (
    <div className="border-b border-slate-200 mb-6 mt-2">
      <nav className="-mb-px flex space-x-8">
        {tabs.map((tab) => (
          <NavLink
            key={tab.name}
            to={tab.path}
            className={({ isActive }) =>
              cn(
                'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors',
                isActive
                  ? 'border-blue-600 text-blue-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
              )
            }
          >
            <tab.icon size={16} />
            {tab.name}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}

// Layout chính
export default function HrPage() {
  const location = useLocation();
  // Nếu url là dạng /hr/students/xxx (và không phải /new) thì coi như là trang Detail
  // Trang detail sẽ không hiển thị Header chung và Tabs
  const isDetailPage = location.pathname.split('/').length > 3 && !location.pathname.endsWith('/new');

  return (
    <div className="p-6 h-full flex flex-col bg-slate-50/50">
      {!isDetailPage && (
        <>
          <HrPageHeader 
            title="Quản lý Nhân sự" 
            description="Quản lý hồ sơ sinh viên, giảng viên và cán bộ nhân viên"
            icon={Users}
          />
          <HrTabs />
        </>
      )}

      {/* Main Content Area */}
      <div className="flex-1">
        <Routes>
          <Route path="/" element={<Navigate to="/hr/students" replace />} />
          
          <Route path="students" element={<StudentListPage />} />
          <Route path="students/new" element={<StudentFormPage />} />
          <Route path="students/:id/edit" element={<StudentFormPage />} />
          <Route path="students/:id" element={<StudentDetailPage />} />
          
          <Route path="lecturers" element={<LecturerListPage />} />
          <Route path="lecturers/new" element={<LecturerFormPage />} />
          <Route path="lecturers/:id/edit" element={<LecturerFormPage />} />
          <Route path="lecturers/:id" element={<LecturerDetailPage />} />
          
          <Route path="staffs" element={<Placeholder title="Danh sách Cán bộ" />} />
          <Route path="staffs/:id" element={<Placeholder title="Chi tiết Cán bộ" />} />
          
          <Route path="*" element={<Navigate to="/hr/students" replace />} />
        </Routes>
      </div>
    </div>
  );
}
