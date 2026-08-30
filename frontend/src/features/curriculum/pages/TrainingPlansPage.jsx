import { useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { useTrainingPlans, useTrainingPlanMutations } from '../hooks/useTrainingPlans';
import { useDepartmentOptions, useSemesterOptions } from '../../master_data/hooks/useMasterDataOptions';
import { usePermissions } from '@/hooks/usePermissions';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import ConfirmModal from '@/components/ui/ConfirmModal';
import TrainingPlanTable from '../components/TrainingPlanTable';
import TrainingPlanFormModal from '../components/TrainingPlanFormModal';
import { useDebounce } from '@/hooks/useDebounce';

export default function TrainingPlansPage() {
  const { hasPermission } = usePermissions();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  const [departmentId, setDepartmentId] = useState('all');
  const [semesterId, setSemesterId] = useState('all');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });

  const { data: departmentsData } = useDepartmentOptions();
  const { data: semestersData } = useSemesterOptions();

  const departments = departmentsData || [];
  const semesters = semestersData || [];

  const filters = {
    page,
    search: debouncedSearch || undefined,
    department_id: departmentId !== 'all' ? departmentId : undefined,
    semester_id: semesterId !== 'all' ? semesterId : undefined,
  };

  const { data, isLoading } = useTrainingPlans(filters);
  const { createMutation, updateMutation, deleteMutation } = useTrainingPlanMutations(() => {
    setIsFormOpen(false);
    setSelectedPlan(null);
    setDeleteConfig({ isOpen: false, id: null });
  });

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleDepartmentChange = (val) => {
    setDepartmentId(val);
    setPage(1);
  };

  const handleSemesterChange = (val) => {
    setSemesterId(val);
    setPage(1);
  };

  const handleOpenForm = (plan = null) => {
    setSelectedPlan(plan);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (formData) => {
    if (selectedPlan) {
      updateMutation.mutate({ id: selectedPlan.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleDelete = () => {
    if (deleteConfig.id) {
      deleteMutation.mutate(deleteConfig.id);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Kế hoạch Đào tạo</h1>
          <p className="text-slate-500 mt-1">Quản lý danh sách kế hoạch đào tạo theo học kỳ</p>
        </div>

        {hasPermission('curriculum.add_trainingplan') && (
          <Button onClick={() => handleOpenForm()} className="bg-indigo-600 hover:bg-indigo-700">
            <Plus className="w-4 h-4 mr-2" /> Thêm Kế hoạch
          </Button>
        )}
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Tìm kiếm theo tên..."
            className="pl-9 bg-slate-50 border-transparent focus-visible:bg-white"
            onChange={handleSearchChange}
          />
        </div>
        
        <div className="w-full sm:w-48">
          <Select value={semesterId} onValueChange={handleSemesterChange}>
            <SelectTrigger className="bg-slate-50 border-transparent focus:bg-white">
              <SelectValue placeholder="Tất cả Học kỳ">
                {semesterId === 'all' 
                  ? 'Tất cả Học kỳ' 
                  : semesters.find(s => s.value === semesterId)?.label || semesterId}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả Học kỳ</SelectItem>
              {semesters.map(sem => (
                <SelectItem key={sem.value} value={sem.value}>{sem.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="w-full sm:w-64">
          <Select value={departmentId} onValueChange={handleDepartmentChange}>
            <SelectTrigger className="bg-slate-50 border-transparent focus:bg-white">
              <SelectValue placeholder="Tất cả Khoa">
                {departmentId === 'all' 
                  ? 'Tất cả Khoa' 
                  : departments.find(d => d.value === departmentId)?.label || departmentId}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả Khoa</SelectItem>
              {departments.map(dept => (
                <SelectItem key={dept.value} value={dept.value}>{dept.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <TrainingPlanTable
        plans={data?.results || []}
        count={data?.count || 0}
        page={page}
        setPage={setPage}
        isLoading={isLoading}
        canUpdate={hasPermission('curriculum.change_trainingplan')}
        canDelete={hasPermission('curriculum.delete_trainingplan')}
        onEdit={handleOpenForm}
        setDeleteConfig={setDeleteConfig}
      />

      <TrainingPlanFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        initialData={selectedPlan}
        onSubmit={handleSubmitForm}
        departments={departments}
        semesters={semesters}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Xóa Kế hoạch Đào tạo"
        description="Bạn có chắc chắn muốn xóa kế hoạch này? Các dữ liệu liên quan sẽ bị ảnh hưởng."
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
