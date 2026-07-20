import { useState } from 'react';
import { Building2, BookOpen, MapPin, Award, FileSpreadsheet, Layers, Clock, CalendarDays, Key, Settings } from 'lucide-react';
import DepartmentList from './components/DepartmentList';
import MajorList from './components/MajorList';
import SpecializationList from './components/SpecializationList';
import SemesterList from './components/SemesterList';
import RoomList from './components/RoomList';
import PriorityCategoryList from './components/PriorityCategoryList';
import CohortList from './components/CohortList';
import AcademicYearList from './components/AcademicYearList';
import GenericDataList from './components/GenericDataList';
import {
  examTypeApi,
  educationSystemApi,
} from '../../api/masterData';

const TABS = [
  { id: 'departments', label: 'Đơn vị đào tạo', icon: Building2 },
  { id: 'majors', label: 'Ngành học', icon: BookOpen },
  { id: 'specializations', label: 'Chuyên ngành', icon: Layers },
  { id: 'educationSystems', label: 'Hệ đào tạo', icon: Award },
  { id: 'cohorts', label: 'Khóa học', icon: Key },
  { id: 'academicYears', label: 'Năm học', icon: CalendarDays },
  { id: 'semesters', label: 'Học kỳ', icon: Clock },
  { id: 'rooms', label: 'Phòng học', icon: MapPin },
  { id: 'examTypes', label: 'Hình thức thi', icon: FileSpreadsheet },
  { id: 'priorityCategories', label: 'Đối tượng ưu tiên', icon: Settings },
];

export default function MasterDataPage() {
  const [activeTab, setActiveTab] = useState(TABS[0].id);

  const renderContent = () => {
    switch (activeTab) {
      case 'departments':
        return <DepartmentList />;
      case 'majors':
        return <MajorList />;
      case 'rooms':
        return <RoomList />;
      case 'priorityCategories':
        return <PriorityCategoryList />;
      case 'examTypes':
        return <GenericDataList api={examTypeApi} title="Hình thức thi" />;
      case 'cohorts':
        return <CohortList />;
      case 'semesters':
        return <SemesterList />;
      case 'specializations':
        return <SpecializationList />;
      case 'educationSystems':
        return <GenericDataList api={educationSystemApi} title="Hệ đào tạo" />;
      case 'academicYears':
        return <AcademicYearList />;
      default:
        return <div>Chưa khả dụng</div>;
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Secondary Sidebar cho Tabs */}
      <div className="w-64 bg-white border-r border-slate-200 overflow-y-auto">
        <div className="p-4 border-b border-slate-200">
          <h2 className="text-lg font-semibold text-slate-800">Danh mục gốc</h2>
        </div>
        <nav className="p-2 space-y-1">
          {TABS.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                }`}
              >
                <tab.icon size={18} className={isActive ? 'text-blue-700' : 'text-slate-400'} />
                {tab.label}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-slate-50 overflow-hidden">
        {renderContent()}
      </div>
    </div>
  );
}
