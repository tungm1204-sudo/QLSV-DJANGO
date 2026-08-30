import { useState, useCallback } from 'react';
import { Plus, Search } from 'lucide-react';
import { useCourses, useCourseMutations } from '../hooks/useCourses';
import { useDepartmentOptions, useCourseTypeOptions } from '../../master_data/hooks/useMasterDataOptions';
import { usePermissions } from '@/hooks/usePermissions';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import ConfirmModal from '@/components/ui/ConfirmModal';
import CourseTable from '../components/CourseTable';
import CourseFormModal from '../components/CourseFormModal';
import { useDebounce } from '@/hooks/useDebounce';

export default function CoursesPage() {
  const { hasPermission } = usePermissions();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebounce(search, 500);
  const [departmentId, setDepartmentId] = useState('all');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });

  const { data: departmentsData } = useDepartmentOptions();
  const { data: courseTypesData } = useCourseTypeOptions();

  const departments = departmentsData || [];
  const courseTypes = courseTypesData || [];

  const filters = {
    page,
    search: debouncedSearch || undefined,
    department_id: departmentId !== 'all' ? departmentId : undefined
  };

  const { data, isLoading } = useCourses(filters);
  const { createMutation, updateMutation, deleteMutation } = useCourseMutations(() => {
    setIsFormOpen(false);
    setSelectedCourse(null);
    setDeleteConfig({ isOpen: false, id: null });
  });

  const handleSearchChange = (e) => {
    setSearch(e.target.value);
    setPage(1);
  };

  const handleFilterChange = (val) => {
    setDepartmentId(val);
    setPage(1);
  };

  const handleOpenForm = (course = null) => {
    setSelectedCourse(course);
    setIsFormOpen(true);
  };

  const handleSubmitForm = (formData) => {
    if (selectedCourse) {
      updateMutation.mutate({ id: selectedCourse.id, data: formData });
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
          <h1 className="text-2xl font-bold text-slate-900">Quản lý Môn học</h1>
          <p className="text-slate-500 mt-1">Danh sách môn học và thiết lập tín chỉ</p>
        </div>

        {hasPermission('curriculum.add_course') && (
          <Button onClick={() => handleOpenForm()} className="bg-indigo-600 hover:bg-indigo-700">
            <Plus className="w-4 h-4 mr-2" /> Thêm Môn học
          </Button>
        )}
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <Input
            placeholder="Tìm kiếm môn học (Mã, Tên)..."
            className="pl-9 bg-slate-50 border-transparent focus-visible:bg-white"
            onChange={handleSearchChange}
          />
        </div>
        <div className="w-full sm:w-64">
          <Select value={departmentId} onValueChange={handleFilterChange}>
            <SelectTrigger className="bg-slate-50 border-transparent focus:bg-white">
              <SelectValue placeholder="Tất cả Bộ môn">
                {departmentId === 'all' 
                  ? 'Tất cả Bộ môn' 
                  : departments.find(d => d.value === departmentId)?.label || departmentId}
              </SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Tất cả Bộ môn</SelectItem>
              {departments.map(dept => (
                <SelectItem key={dept.value} value={dept.value}>{dept.label}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <CourseTable
        courses={data?.results || []}
        count={data?.count || 0}
        page={page}
        setPage={setPage}
        isLoading={isLoading}
        canUpdate={hasPermission('curriculum.change_course')}
        canDelete={hasPermission('curriculum.delete_course')}
        onEdit={handleOpenForm}
        setDeleteConfig={setDeleteConfig}
        departments={departments}
        courseTypes={courseTypes}
      />

      <CourseFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        initialData={selectedCourse}
        onSubmit={handleSubmitForm}
        departments={departments}
        courseTypes={courseTypes}
        isLoading={createMutation.isLoading || updateMutation.isLoading}
      />

      <ConfirmModal
        isOpen={deleteConfig.isOpen}
        onClose={() => setDeleteConfig({ isOpen: false, id: null })}
        onConfirm={handleDelete}
        title="Xóa môn học"
        description="Bạn có chắc chắn muốn xóa môn học này? Hành động này có thể ẩn môn học khỏi hệ thống."
        isLoading={deleteMutation.isLoading}
      />
    </div>
  );
}
