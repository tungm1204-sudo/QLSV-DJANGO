import { useState } from 'react';
import { Plus, Search } from 'lucide-react';
import { useTrainingPrograms, useTrainingProgramMutations } from '../hooks/useTrainingPrograms';
import { 
  useMajorOptions, 
  useSpecializationOptions, 
  useCohortOptions 
} from '../../master_data/hooks/useMasterDataOptions';
import { usePermissions } from '@/hooks/usePermissions';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import ConfirmModal from '@/components/ui/ConfirmModal';
import TrainingProgramTable from '../components/TrainingProgramTable';
import TrainingProgramFormModal from '../components/TrainingProgramFormModal';
import { useDebounce } from '@/hooks/useDebounce';

export default function TrainingProgramsPage() {
  const { hasPermission } = usePermissions();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  const [majorId, setMajorId] = useState('all');
  const [cohortId, setCohortId] = useState('all');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });

  const { data: majorsData } = useMajorOptions();
  const { data: specializationsData } = useSpecializationOptions();
  const { data: cohortsData } = useCohortOptions();

  const majors = majorsData || [];
  const specializations = specializationsData || [];
  const cohorts = cohortsData || [];

  const filters = {
    page,
    search: debouncedSearch || undefined,
    major_id: majorId !== 'all' ? majorId : undefined,
    cohort_id: cohortId !== 'all' ? cohortId : undefined,
  };

  const { data, isLoading } = useTrainingPrograms(filters);
  const { createMutation, updateMutation, deleteMutation } = useTrainingProgramMutations(() => {
    setIsFormOpen(false);
    setSelectedProgram(null);
    setDeleteConfig({ isOpen: false, id: null });
  });

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleFilterChange = (type, val) => {
    if (type === 'major') setMajorId(val);
    if (type === 'cohort') setCohortId(val);
    setPage(1);
  };

  const handleOpenForm = (program = null) => {
    setSelectedProgram(program);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (formData) => {
    if (selectedProgram) {
      updateMutation.mutate({ id: selectedProgram.id, data: formData });
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
          <h1 className="text-2xl font-bold text-slate-900">Quản lý CTĐT</h1>
          <p className="text-slate-500 mt-1">Danh sách Khung chương trình đào tạo</p>
        </div>

        {hasPermission('curriculum.add_trainingprogram') && (
          <Button onClick={() => handleOpenForm()} className="bg-indigo-600 hover:bg-indigo-700">
            <Plus className="w-4 h-4 mr-2" /> Thêm CTĐT
          </Button>
        )}
      </div>

      <div className="flex flex-col lg:flex-row gap-4 items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Tìm kiếm CTĐT (Mã, Tên)..."
            className="pl-9 bg-slate-50 border-transparent focus-visible:bg-white"
            onChange={handleSearchChange}
          />
        </div>
        
        <div className="w-full lg:w-48">
          <Select value={majorId} onValueChange={(v) => handleFilterChange('major', v)}>
            <SelectTrigger className="bg-slate-50 border-transparent focus:bg-white">
              <SelectValue placeholder="Tất cả Ngành">
                {majorId === 'all' 
                  ? 'Tất cả Ngành' 
                  : majors.find(d => d.value === majorId)?.label || majorId}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả Ngành</SelectItem>
              {majors.map(m => (
                <SelectItem key={m.value} value={m.value}>{m.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="w-full lg:w-48">
          <Select value={cohortId} onValueChange={(v) => handleFilterChange('cohort', v)}>
            <SelectTrigger className="bg-slate-50 border-transparent focus:bg-white">
              <SelectValue placeholder="Tất cả Khóa">
                {cohortId === 'all' 
                  ? 'Tất cả Khóa' 
                  : cohorts.find(c => c.value === cohortId)?.label || cohortId}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả Khóa</SelectItem>
              {cohorts.map(c => (
                <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <TrainingProgramTable
        programs={data?.results || []}
        count={data?.count || 0}
        page={page}
        setPage={setPage}
        isLoading={isLoading}
        canUpdate={hasPermission('curriculum.change_trainingprogram')}
        canDelete={hasPermission('curriculum.delete_trainingprogram')}
        onEdit={handleOpenForm}
        setDeleteConfig={setDeleteConfig}
        majors={majors}
        specializations={specializations}
        cohorts={cohorts}
      />

      <TrainingProgramFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        initialData={selectedProgram}
        onSubmit={handleSubmitForm}
        majors={majors}
        specializations={specializations}
        cohorts={cohorts}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Xóa Chương trình đào tạo"
        description="Bạn có chắc chắn muốn xóa Chương trình đào tạo này? Hành động này sẽ vô hiệu hóa CTĐT khỏi hệ thống."
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
