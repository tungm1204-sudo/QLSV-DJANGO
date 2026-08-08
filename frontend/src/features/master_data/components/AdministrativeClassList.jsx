import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Plus, Search, Edit2, Trash2, X, Users, BookOpen, GraduationCap, Award } from 'lucide-react';
import { toast } from 'sonner';
import ConfirmModal from '../../../components/ui/ConfirmModal';
import { 
  administrativeClassApi, 
  majorApi, 
  cohortApi, 
  educationSystemApi 
} from '../api/masterDataApi';

export default function AdministrativeClassList() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, id: null });

  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  // Data fetching
  const { data: response, isLoading } = useQuery({
    queryKey: ['master-data', 'administrativeClasses', searchTerm],
    queryFn: () => administrativeClassApi.getAll({ search: searchTerm }),
  });
  const records = response?.data?.results || response?.data || [];

  const { data: majorsRes } = useQuery({
    queryKey: ['master-data', 'majors', 'all'],
    queryFn: () => majorApi.getAll({}),
  });
  const majors = majorsRes?.data?.results || majorsRes?.data || [];

  const { data: cohortsRes } = useQuery({
    queryKey: ['master-data', 'cohorts', 'all'],
    queryFn: () => cohortApi.getAll({}),
  });
  const cohorts = cohortsRes?.data?.results || cohortsRes?.data || [];

  const { data: eduSystemsRes } = useQuery({
    queryKey: ['master-data', 'educationSystems', 'all'],
    queryFn: () => educationSystemApi.getAll({}),
  });
  const educationSystems = eduSystemsRes?.data?.results || eduSystemsRes?.data || [];

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data) => administrativeClassApi.create(data),
    onSuccess: () => {
      toast.success('Thêm lớp hành chính thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'administrativeClasses'] });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi thêm lớp hành chính'),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => administrativeClassApi.update(id, data),
    onSuccess: () => {
      toast.success('Cập nhật lớp hành chính thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'administrativeClasses'] });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi cập nhật lớp hành chính'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => administrativeClassApi.delete(id),
    onSuccess: () => {
      toast.success('Xóa lớp hành chính thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'administrativeClasses'] });
      setDeleteModal({ isOpen: false, id: null });
    },
    onError: () => toast.error('Không thể xóa lớp hành chính này'),
  });

  const openModal = (data = null) => {
    if (data) {
      setEditingData(data);
      reset({
        code: data.code,
        name: data.name,
        major: data.major?.id || data.major,
        cohort: data.cohort?.id || data.cohort,
        education_system: data.education_system?.id || data.education_system,
        is_active: data.is_active,
      });
    } else {
      setEditingData(null);
      reset({ code: '', name: '', major: '', cohort: '', education_system: '', is_active: true });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingData(null);
    reset();
  };

  const onSubmit = (data) => {
    const payload = {
        ...data,
        major: data.major ? String(data.major) : null,
        cohort: data.cohort ? String(data.cohort) : null,
        education_system: data.education_system ? String(data.education_system) : null,
    };
    if (editingData) {
      updateMutation.mutate({ id: editingData.id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const confirmDelete = () => {
    if (deleteModal.id) {
      deleteMutation.mutate(deleteModal.id, { onSuccess: () => setDeleteModal({ isOpen: false, id: null }) });
    }
  };

  return (
    <div className="p-6 h-full flex flex-col relative">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Quản lý Lớp hành chính</h1>
        <button 
          onClick={() => openModal()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <Plus size={18} />
          <span>Thêm mới</span>
        </button>
      </div>

      <div className="flex gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
          <input
            type="text"
            placeholder="Tìm kiếm lớp..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex-1 overflow-hidden flex flex-col">
        <div className="overflow-x-auto flex-1">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-slate-700 font-medium border-b border-slate-200 sticky top-0">
              <tr>
                <th className="px-6 py-4">Mã lớp</th>
                <th className="px-6 py-4">Tên lớp</th>
                <th className="px-6 py-4">Ngành / Hệ</th>
                <th className="px-6 py-4">Khóa học</th>
                <th className="px-6 py-4">Trạng thái</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">Đang tải dữ liệu...</td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-slate-500">Không tìm thấy dữ liệu.</td>
                </tr>
              ) : (
                records.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-900">{item.code}</td>
                    <td className="px-6 py-4">{item.name}</td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col gap-1">
                        {item.major && (
                          <div className="flex items-center gap-1.5 text-blue-600">
                            <BookOpen size={14} />
                            <span>{item.major_details?.name || item.major}</span>
                          </div>
                        )}
                        {item.education_system && (
                          <div className="flex items-center gap-1.5 text-slate-500 text-xs">
                            <Award size={12} />
                            <span>{item.education_system_details?.name || item.education_system}</span>
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      {item.cohort ? (
                        <div className="flex items-center gap-1.5 text-slate-600">
                          <GraduationCap size={14} />
                          <span>{item.cohort_details?.name || item.cohort}</span>
                        </div>
                      ) : '-'}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        item.is_active ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-700'
                      }`}>
                        {item.is_active ? 'Hoạt động' : 'Tạm dừng'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button
                          onClick={() => openModal(item)}
                          className="p-1 text-slate-400 hover:text-blue-600 transition-colors"
                        >
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => setDeleteModal({ isOpen: true, id: item.id })}
                          className="p-1 text-slate-400 hover:text-red-600 transition-colors"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {isModalOpen && (
        <div className="absolute inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-slate-100">
              <h2 className="text-lg font-semibold text-slate-800">
                {editingData ? 'Cập nhật Lớp hành chính' : 'Thêm Lớp hành chính'}
              </h2>
              <button onClick={closeModal} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit(onSubmit)} className="p-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2 sm:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mã lớp <span className="text-red-500">*</span></label>
                  <input
                    {...register('code', { required: 'Mã không được để trống' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="VD: D19CQCN01-N"
                  />
                  {errors.code && <span className="text-xs text-red-500 mt-1">{errors.code.message}</span>}
                </div>

                <div className="col-span-2 sm:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Tên lớp <span className="text-red-500">*</span></label>
                  <input
                    {...register('name', { required: 'Tên không được để trống' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="VD: D19 Công nghệ thông tin 01"
                  />
                  {errors.name && <span className="text-xs text-red-500 mt-1">{errors.name.message}</span>}
                </div>

                <div className="col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Ngành học <span className="text-red-500">*</span></label>
                  <select
                    {...register('major', { required: 'Vui lòng chọn ngành học' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">-- Chọn ngành học --</option>
                    {majors.map(m => (
                      <option key={m.id} value={m.id}>{m.code} - {m.name}</option>
                    ))}
                  </select>
                  {errors.major && <span className="text-xs text-red-500 mt-1">{errors.major.message}</span>}
                </div>

                <div className="col-span-2 sm:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Hệ đào tạo <span className="text-red-500">*</span></label>
                  <select
                    {...register('education_system', { required: 'Vui lòng chọn hệ đào tạo' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">-- Chọn hệ đào tạo --</option>
                    {educationSystems.map(es => (
                      <option key={es.id} value={es.id}>{es.code} - {es.name}</option>
                    ))}
                  </select>
                  {errors.education_system && <span className="text-xs text-red-500 mt-1">{errors.education_system.message}</span>}
                </div>

                <div className="col-span-2 sm:col-span-1">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Khóa học <span className="text-red-500">*</span></label>
                  <select
                    {...register('cohort', { required: 'Vui lòng chọn khóa học' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">-- Chọn khóa học --</option>
                    {cohorts.map(c => (
                      <option key={c.id} value={c.id}>{c.code} - {c.name}</option>
                    ))}
                  </select>
                  {errors.cohort && <span className="text-xs text-red-500 mt-1">{errors.cohort.message}</span>}
                </div>

                <div className="col-span-2 flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    id="is_active"
                    {...register('is_active')}
                    className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                  />
                  <label htmlFor="is_active" className="text-sm text-slate-700">Trạng thái hoạt động</label>
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 mt-6 border-t border-slate-100">
                <button
                  type="button"
                  onClick={closeModal}
                  className="px-4 py-2 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isPending || updateMutation.isPending}
                  className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors disabled:opacity-50"
                >
                  {createMutation.isPending || updateMutation.isPending ? 'Đang lưu...' : 'Lưu thông tin'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <ConfirmModal
        isDanger={true}
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, id: null })}
        onConfirm={confirmDelete}
        title="Xóa lớp hành chính"
        message="Bạn có chắc chắn muốn xóa lớp hành chính này? Hành động này không thể hoàn tác."
        
      />
    </div>
  );
}
