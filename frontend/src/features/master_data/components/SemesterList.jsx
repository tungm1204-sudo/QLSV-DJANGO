import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Plus, Search, Edit2, Trash2, X } from 'lucide-react';
import { toast } from 'sonner';
import ConfirmDeleteModal from '../../../components/ui/ConfirmDeleteModal';
import { semesterApi, academicYearApi } from '../../../api/masterData';

export default function SemesterList() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, id: null });

  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  // Fetch Semesters
  const { data: response, isLoading } = useQuery({
    queryKey: ['master-data', 'semesters', searchTerm],
    queryFn: () => semesterApi.getAll({ search: searchTerm }),
  });

  // Fetch Academic Years for Dropdown
  const { data: parentResponse } = useQuery({
    queryKey: ['master-data', 'academic-years', 'all'],
    queryFn: () => academicYearApi.getAll({}), 
  });

  const records = response?.data?.results || response?.data || [];
  const parentOptions = parentResponse?.data?.results || parentResponse?.data || [];

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data) => semesterApi.create(data),
    onSuccess: () => {
      toast.success('Thêm học kỳ thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'semesters'] });
      setDeleteModal({ isOpen: false, id: null });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi thêm học kỳ'),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => semesterApi.update(id, data),
    onSuccess: () => {
      toast.success('Cập nhật học kỳ thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'semesters'] });
      setDeleteModal({ isOpen: false, id: null });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi cập nhật học kỳ'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => semesterApi.delete(id),
    onSuccess: () => {
      toast.success('Xóa học kỳ thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'semesters'] });
      setDeleteModal({ isOpen: false, id: null });
    },
    onError: () => toast.error('Không thể xóa vì học kỳ này đang chứa dữ liệu khác'),
  });

  const openModal = (data = null) => {
    if (data) {
      setEditingData(data);
      reset({
        code: data.code,
        academic_year: data.academic_year || '',
        season: data.season || 'HK1',
        start_date: data.start_date || '',
        end_date: data.end_date || '',
        is_current: data.is_current || false,
      });
    } else {
      setEditingData(null);
      reset({ code: '', academic_year: '', season: 'HK1', start_date: '', end_date: '', is_current: false });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingData(null);
    reset();
  };

  const onSubmit = (data) => {
    // nullify empty strings for dates
    const payload = { ...data };
    if (!payload.start_date) payload.start_date = null;
    if (!payload.end_date) payload.end_date = null;

    if (editingData) {
      updateMutation.mutate({ id: editingData.id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const handleDelete = (id) => {
    setDeleteModal({ isOpen: true, id });
  };

  const confirmDelete = () => {
    if (deleteModal.id) {
      deleteMutation.mutate(deleteModal.id);
    }
  };

  return (
    <div className="p-6 h-full flex flex-col relative">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Quản lý Học kỳ</h1>
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
            placeholder="Tìm kiếm theo mã, tên..."
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
                <th className="px-6 py-4">Mã học kỳ</th>
                <th className="px-6 py-4">Năm học</th>
                <th className="px-6 py-4">Mùa</th>
                <th className="px-6 py-4">Ngày bắt đầu</th>
                <th className="px-6 py-4">Ngày kết thúc</th>
                <th className="px-6 py-4">Hiện tại</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {isLoading ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-slate-500">Đang tải dữ liệu...</td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={7} className="px-6 py-8 text-center text-slate-500">Không tìm thấy dữ liệu.</td>
                </tr>
              ) : (
                records.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-900">{item.code}</td>
                    <td className="px-6 py-4">{item.academic_year_name || '-'}</td>
                    <td className="px-6 py-4">
                      {item.season === 'HK1' ? 'Học kỳ 1' : 
                       item.season === 'HK2' ? 'Học kỳ 2' : 
                       item.season === 'HE' ? 'Học kỳ Hè' : item.season}
                    </td>
                    <td className="px-6 py-4">{item.start_date || '-'}</td>
                    <td className="px-6 py-4">{item.end_date || '-'}</td>
                    <td className="px-6 py-4">
                      {item.is_current ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">Hiện tại</span>
                      ) : (
                        <span className="text-slate-400">-</span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button onClick={() => openModal(item)} className="p-1.5 text-slate-400 hover:text-blue-600 transition-colors" title="Sửa">
                          <Edit2 size={16} />
                        </button>
                        <button onClick={() => handleDelete(item.id)} className="p-1.5 text-slate-400 hover:text-red-600 transition-colors" title="Xóa">
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

      {/* Modal Form */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200 h-max max-h-screen overflow-y-auto">
            <div className="flex justify-between items-center px-6 py-4 border-b border-slate-100 sticky top-0 bg-white z-10">
              <h2 className="text-lg font-semibold text-slate-800">
                {editingData ? 'Sửa Học kỳ' : 'Thêm Học kỳ mới'}
              </h2>
              <button onClick={closeModal} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit(onSubmit)} className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mã học kỳ *</label>
                  <input
                    {...register('code', { required: 'Vui lòng nhập mã' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="VD: HK1-2024"
                  />
                  {errors.code && <span className="text-xs text-red-500">{errors.code.message}</span>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Năm học trực thuộc *</label>
                  <select
                    {...register('academic_year', { required: 'Vui lòng chọn năm học' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">-- Chọn năm học --</option>
                    {parentOptions.map(parent => (
                      <option key={parent.id} value={parent.id}>{parent.name}</option>
                    ))}
                  </select>
                  {errors.academic_year && <span className="text-xs text-red-500">{errors.academic_year.message}</span>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mùa học kỳ *</label>
                  <select
                    {...register('season', { required: 'Vui lòng chọn mùa' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="HK1">Học kỳ 1</option>
                    <option value="HK2">Học kỳ 2</option>
                    <option value="HE">Học kỳ Hè</option>
                  </select>
                  {errors.season && <span className="text-xs text-red-500">{errors.season.message}</span>}
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Ngày bắt đầu *</label>
                    <input
                      type="date"
                      {...register('start_date', { required: 'Bắt buộc' })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {errors.start_date && <span className="text-xs text-red-500">{errors.start_date.message}</span>}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-slate-700 mb-1">Ngày kết thúc *</label>
                    <input
                      type="date"
                      {...register('end_date', { required: 'Bắt buộc' })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {errors.end_date && <span className="text-xs text-red-500">{errors.end_date.message}</span>}
                  </div>
                </div>

                <div className="flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    id="is_current"
                    {...register('is_current')}
                    className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"
                  />
                  <label htmlFor="is_current" className="text-sm text-slate-700 font-medium">Là học kỳ hiện tại</label>
                </div>
              </div>

              <div className="mt-8 flex justify-end gap-3">
                <button type="button" onClick={closeModal} className="px-4 py-2 text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors">
                  Hủy
                </button>
                <button 
                  type="submit" 
                  disabled={createMutation.isPending || updateMutation.isPending}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {(createMutation.isPending || updateMutation.isPending) ? 'Đang lưu...' : 'Lưu thông tin'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <ConfirmDeleteModal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, id: null })}
        onConfirm={confirmDelete}
        isDeleting={deleteMutation.isPending}
        message="Bạn có chắc chắn muốn xóa bản ghi này không? Hành động này không thể hoàn tác."
      />
    </div>
  );
}
