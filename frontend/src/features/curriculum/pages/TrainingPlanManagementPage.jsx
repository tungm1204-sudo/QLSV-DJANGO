import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Plus, ArrowLeft, Search } from 'lucide-react';
import { useTrainingPlanDetail } from '../hooks/useTrainingPlans';
import { useCourseOfferings, useCourseOfferingMutations } from '../hooks/useCourseOfferings';
import { usePermissions } from '@/hooks/usePermissions';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import ConfirmModal from '@/components/ui/ConfirmModal';
import CourseOfferingTable from '../components/CourseOfferingTable';
import CourseOfferingFormModal from '../components/CourseOfferingFormModal';
import ScheduleConfigModal from '../components/ScheduleConfigModal';
import TrainingPlanCalendarTab from '../components/TrainingPlanCalendarTab';
import { useDebounce } from '@/hooks/useDebounce';

const statusMap = {
  'DRAFT': { label: 'Nháp', color: 'bg-slate-100 text-slate-700' },
  'PENDING': { label: 'Chờ duyệt', color: 'bg-yellow-100 text-yellow-700' },
  'APPROVED': { label: 'Đã duyệt', color: 'bg-green-100 text-green-700' },
  'REJECTED': { label: 'Từ chối', color: 'bg-red-100 text-red-700' },
};

export default function TrainingPlanManagementPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { hasPermission } = usePermissions();
  
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedOffering, setSelectedOffering] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });

  // State cho Tab
  const [activeTab, setActiveTab] = useState('list');

  // State cho Schedule Modal
  const [isScheduleModalOpen, setIsScheduleModalOpen] = useState(false);
  const [scheduleOffering, setScheduleOffering] = useState(null);

  // 1. Lấy thông tin Kế hoạch
  const { data: plan, isLoading: isPlanLoading } = useTrainingPlanDetail(id);

  // 2. Lấy danh sách Lớp học phần thuộc Kế hoạch này
  const filters = {
    training_plan_id: id,
    page,
    search: debouncedSearch || undefined,
  };
  const { data: offeringsData, isLoading: isOfferingsLoading } = useCourseOfferings(filters);
  
  // 3. Mutations
  const { createMutation, updateMutation, deleteMutation } = useCourseOfferingMutations(() => {
    setIsFormOpen(false);
    setSelectedOffering(null);
    setDeleteConfig({ isOpen: false, id: null });
  });

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleOpenForm = (offering = null) => {
    setSelectedOffering(offering);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (formData) => {
    // Inject training_plan and semester automatically
    const payload = {
      ...formData,
      training_plan: id,
      semester: plan?.semester?.id || plan?.semester
    };

    if (selectedOffering) {
      updateMutation.mutate({ id: selectedOffering.id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const handleDelete = () => {
    if (deleteConfig.id) {
      deleteMutation.mutate(deleteConfig.id);
    }
  };

  const handleConfigSchedule = (offering) => {
    setScheduleOffering(offering);
    setIsScheduleModalOpen(true);
  };

  if (isPlanLoading) return <div className="p-8 text-center">Đang tải thông tin kế hoạch...</div>;
  if (!plan) return <div className="p-8 text-center text-red-500">Không tìm thấy kế hoạch đào tạo</div>;

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      {/* Header (Kế hoạch) */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => navigate('/curriculum/training-plans')}>
            <ArrowLeft className="w-5 h-5" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold text-slate-900">{plan.name}</h1>
            <p className="text-slate-500 mt-1">
              Học kỳ: <span className="font-medium text-slate-700">{plan.semester?.name}</span> | 
              Khoa: <span className="font-medium text-slate-700">{plan.department?.name}</span>
            </p>
          </div>
          <div className="ml-auto">
            <Badge variant="outline" className={statusMap[plan.status]?.color}>
              {statusMap[plan.status]?.label || plan.status}
            </Badge>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-200">
        <button
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${activeTab === 'list' ? 'text-indigo-600' : 'text-slate-500 hover:text-slate-700'}`}
          onClick={() => setActiveTab('list')}
        >
          Danh sách Lớp học phần
          {activeTab === 'list' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600" />}
        </button>
        <button
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${activeTab === 'calendar' ? 'text-indigo-600' : 'text-slate-500 hover:text-slate-700'}`}
          onClick={() => setActiveTab('calendar')}
        >
          Lịch tuần (Grid)
          {activeTab === 'calendar' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600" />}
        </button>
      </div>

      {/* Body */}
      {activeTab === 'list' ? (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <h2 className="text-lg font-semibold text-slate-900">Danh sách Lớp học phần</h2>
            {hasPermission('curriculum.add_courseoffering') && plan.status !== 'APPROVED' && (
              <Button onClick={() => handleOpenForm()} className="bg-indigo-600 hover:bg-indigo-700">
                <Plus className="w-4 h-4 mr-2" /> Thêm Lớp học phần
              </Button>
            )}
          </div>

        <div className="flex flex-col sm:flex-row gap-4 items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
          <div className="relative flex-1 w-full max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <Input
              placeholder="Tìm kiếm theo mã môn, tên môn..."
              className="pl-9 bg-slate-50 border-transparent focus-visible:bg-white"
              onChange={handleSearchChange}
            />
          </div>
        </div>

        <CourseOfferingTable
          offerings={offeringsData?.results || []}
          count={offeringsData?.count || 0}
          page={page}
          setPage={setPage}
          isLoading={isOfferingsLoading}
          canUpdate={hasPermission('curriculum.change_courseoffering') && plan.status !== 'APPROVED'}
          canDelete={hasPermission('curriculum.delete_courseoffering') && plan.status !== 'APPROVED'}
          onEdit={handleOpenForm}
          onConfigSchedule={handleConfigSchedule}
          setDeleteConfig={setDeleteConfig}
        />
      </div>
      ) : (
        <div className="space-y-4">
          <TrainingPlanCalendarTab trainingPlanId={id} />
        </div>
      )}

      <CourseOfferingFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        initialData={selectedOffering}
        onSubmit={handleSubmitForm}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ScheduleConfigModal
        isOpen={isScheduleModalOpen}
        onClose={() => setIsScheduleModalOpen(false)}
        offering={scheduleOffering}
      />

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Xóa Lớp học phần"
        description="Bạn có chắc chắn muốn xóa lớp học phần này khỏi kế hoạch? Việc xóa lớp học phần sẽ xóa luôn các lịch học đã xếp."
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
