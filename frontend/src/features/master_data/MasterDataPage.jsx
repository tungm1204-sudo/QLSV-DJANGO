import { useState } from 'react';
import { 
  Building2, BookOpen, CalendarDays, GraduationCap, 
  Users, Globe, ChevronDown, ChevronRight 
} from 'lucide-react';

import DepartmentList from './components/DepartmentList';
import MajorList from './components/MajorList';
import SpecializationList from './components/SpecializationList';
import SemesterList from './components/SemesterList';
import RoomList from './components/RoomList';
import PriorityCategoryList from './components/PriorityCategoryList';
import CohortList from './components/CohortList';
import AcademicYearList from './components/AcademicYearList';
import GenericDataList from './components/GenericDataList';
import CampusList from './components/CampusList';
import BuildingList from './components/BuildingList';
import AdministrativeClassList from './components/AdministrativeClassList';

import {
  examTypeApi,
  educationSystemApi,
  degreeApi,
  academicTitleApi,
  admissionTypeApi,
  courseTypeApi,
  positionApi,
  ethnicityApi,
  religionApi,
  nationalityApi
} from '../../api/masterData';

const GROUPS = [
  {
    id: 'organization',
    label: 'Tổ chức & CSVC',
    icon: Building2,
    items: [
      { id: 'departments', label: 'Đơn vị đào tạo' },
      { id: 'campuses', label: 'Cơ sở' },
      { id: 'buildings', label: 'Tòa nhà' },
      { id: 'rooms', label: 'Phòng học' },
    ]
  },
  {
    id: 'training_structure',
    label: 'Cấu trúc đào tạo',
    icon: GraduationCap,
    items: [
      { id: 'educationSystems', label: 'Hệ đào tạo' },
      { id: 'majors', label: 'Ngành học' },
      { id: 'specializations', label: 'Chuyên ngành' },
      { id: 'administrativeClasses', label: 'Lớp hành chính' },
      { id: 'cohorts', label: 'Khóa học' },
    ]
  },
  {
    id: 'time',
    label: 'Thời gian đào tạo',
    icon: CalendarDays,
    items: [
      { id: 'academicYears', label: 'Năm học' },
      { id: 'semesters', label: 'Học kỳ' },
    ]
  },
  {
    id: 'hr_admission',
    label: 'Nhân sự & Tuyển sinh',
    icon: Users,
    items: [
      { id: 'positions', label: 'Chức vụ' },
      { id: 'degrees', label: 'Học vị' },
      { id: 'academicTitles', label: 'Học hàm' },
      { id: 'admissionTypes', label: 'Hình thức tuyển sinh' },
    ]
  },
  {
    id: 'exams_others',
    label: 'Khảo thí & Khác',
    icon: BookOpen,
    items: [
      { id: 'courseTypes', label: 'Loại học phần' },
      { id: 'examTypes', label: 'Hình thức thi' },
      { id: 'priorityCategories', label: 'Đối tượng ưu tiên' },
    ]
  },
  {
    id: 'demographics',
    label: 'Nhân khẩu học',
    icon: Globe,
    items: [
      { id: 'ethnicities', label: 'Dân tộc' },
      { id: 'religions', label: 'Tôn giáo' },
      { id: 'nationalities', label: 'Quốc tịch' },
    ]
  }
];

export default function MasterDataPage() {
  const [activeGroup, setActiveGroup] = useState('organization');
  const [activeTab, setActiveTab] = useState('departments');

  const renderContent = () => {
    switch (activeTab) {
      // Organization
      case 'departments': return <DepartmentList />;
      case 'campuses': return <CampusList />;
      case 'buildings': return <BuildingList />;
      case 'rooms': return <RoomList />;
      
      // Training Structure
      case 'educationSystems': return <GenericDataList api={educationSystemApi} title="Hệ đào tạo" />;
      case 'majors': return <MajorList />;
      case 'specializations': return <SpecializationList />;
      case 'administrativeClasses': return <AdministrativeClassList />;
      case 'cohorts': return <CohortList />;
      
      // Time
      case 'academicYears': return <AcademicYearList />;
      case 'semesters': return <SemesterList />;
      
      // HR & Admission
      case 'positions': return <GenericDataList api={positionApi} title="Chức vụ" />;
      case 'degrees': return <GenericDataList api={degreeApi} title="Học vị" />;
      case 'academicTitles': return <GenericDataList api={academicTitleApi} title="Học hàm" />;
      case 'admissionTypes': return <GenericDataList api={admissionTypeApi} title="Hình thức tuyển sinh" />;
      
      // Exams & Others
      case 'courseTypes': return <GenericDataList api={courseTypeApi} title="Loại học phần" />;
      case 'examTypes': return <GenericDataList api={examTypeApi} title="Hình thức thi" />;
      case 'priorityCategories': return <PriorityCategoryList />;
      
      // Demographics
      case 'ethnicities': return <GenericDataList api={ethnicityApi} title="Dân tộc" />;
      case 'religions': return <GenericDataList api={religionApi} title="Tôn giáo" />;
      case 'nationalities': return <GenericDataList api={nationalityApi} title="Quốc tịch" />;
      
      default: return <div>Chưa khả dụng</div>;
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Sidebar Navigation */}
      <div className="w-72 bg-white border-r border-slate-200 overflow-y-auto flex flex-col custom-scrollbar">
        <div className="p-4 border-b border-slate-200 bg-slate-50/50 sticky top-0 z-10">
          <h2 className="text-lg font-semibold text-slate-800">Danh mục hệ thống</h2>
          <p className="text-xs text-slate-500 mt-1">Quản lý 21 danh mục cốt lõi</p>
        </div>
        
        <nav className="p-3 space-y-2 flex-1">
          {GROUPS.map((group) => {
            const isGroupOpen = activeGroup === group.id;
            return (
              <div key={group.id} className="rounded-xl overflow-hidden bg-slate-50 border border-slate-100">
                <button
                  onClick={() => setActiveGroup(isGroupOpen ? '' : group.id)}
                  className={`w-full flex items-center justify-between p-3 transition-colors ${
                    isGroupOpen ? 'bg-slate-100/80 text-slate-900' : 'text-slate-700 hover:bg-slate-100/50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`p-1.5 rounded-lg ${isGroupOpen ? 'bg-blue-100 text-blue-700' : 'bg-white text-slate-500 shadow-sm border border-slate-200'}`}>
                      <group.icon size={16} />
                    </div>
                    <span className="text-sm font-medium">{group.label}</span>
                  </div>
                  {isGroupOpen ? (
                    <ChevronDown size={16} className="text-slate-400" />
                  ) : (
                    <ChevronRight size={16} className="text-slate-400" />
                  )}
                </button>
                
                {isGroupOpen && (
                  <div className="px-3 pb-3 space-y-1 bg-slate-50 border-t border-slate-100/50">
                    <div className="pt-2" />
                    {group.items.map((item) => {
                      const isActive = activeTab === item.id;
                      return (
                        <button
                          key={item.id}
                          onClick={() => setActiveTab(item.id)}
                          className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all ${
                            isActive
                              ? 'bg-blue-600 text-white font-medium shadow-sm shadow-blue-600/20'
                              : 'text-slate-600 hover:bg-slate-200/50'
                          }`}
                        >
                          {/* Dot indicator for active state */}
                          <div className={`w-1.5 h-1.5 rounded-full ${isActive ? 'bg-white' : 'bg-slate-300'}`} />
                          {item.label}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 bg-slate-50 overflow-hidden">
        {renderContent()}
      </div>
      
      {/* Custom Scrollbar CSS scoped to this page */}
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #cbd5e1;
          border-radius: 4px;
        }
        .custom-scrollbar:hover::-webkit-scrollbar-thumb {
          background: #94a3b8;
        }
      `}} />
    </div>
  );
}
