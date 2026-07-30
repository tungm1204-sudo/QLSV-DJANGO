import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Plus, Search, Edit2, Trash2, X, Building } from 'lucide-react';
import { toast } from 'sonner';
import ConfirmDeleteModal from '../../../components/ui/ConfirmDeleteModal';
import { buildingApi, campusApi } from '../../../api/masterData';

export default function BuildingList() {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, id: null });

  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  // Data fetching
  const { data: response, isLoading } = useQuery({
    queryKey: ['master-data', 'buildings', searchTerm],
    queryFn: () => buildingApi.getAll({ search: searchTerm }),
  });
  const records = response?.data?.results || response?.data || [];

  const { data: campusRes } = useQuery({
    queryKey: ['master-data', 'campuses', 'all'],
    queryFn: () => campusApi.getAll({}),
  });
  const campuses = campusRes?.data?.results || campusRes?.data || [];

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data) => buildingApi.create(data),
    onSuccess: () => {
      toast.success('Thêm tòa nhà thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'buildings'] });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi thêm tòa nhà'),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => buildingApi.update(id, data),
    onSuccess: () => {
      toast.success('Cập nhật tòa nhà thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'buildings'] });
      closeModal();
    },
    onError: () => toast.error('Có lỗi xảy ra khi cập nhật tòa nhà'),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => buildingApi.delete(id),
    onSuccess: () => {
      toast.success('Xóa tòa nhà thành công');
      queryClient.invalidateQueries({ queryKey: ['master-data', 'buildings'] });
      setDeleteModal({ isOpen: false, id: null });
    },
    onError: () => toast.error('Không thể xóa vì tòa nhà đang chứa phòng học'),
  });

  const openModal = (data = null) => {
    if (data) {
      setEditingData(data);
      reset({
        code: data.code,
        name: data.name,
        campus: data.campus?.id || data.campus,
        floor_count: data.floor_count || 1,
        is_active: data.is_active,
      });
    } else {
      setEditingData(null);
      reset({ code: '', name: '', campus: '', floor_count: 1, is_active: true });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingData(null);
    reset();
  };

  const onSubmit = (data) => {
    // Convert to numbers where needed
    const payload = {
        ...data,
        campus: data.campus ? String(data.campus) : null,
    };
    if (editingData) {
      updateMutation.mutate({ id: editingData.id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const confirmDelete = () => {
    if (deleteModal.id) {
      deleteMutation.mutate(deleteModal.id);
    }
  };

  return (
    <div className="p-6 h-full flex flex-col relative">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Quản lý Tòa nhà</h1>
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
            placeholder="Tìm kiếm tòa nhà..."
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
                <th className="px-6 py-4">Mã</th>
                <th className="px-6 py-4">Tên tòa nhà</th>
                <th className="px-6 py-4">Thuộc Cơ sở</th>
                <th className="px-6 py-4">Số tầng</th>
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
                      {item.campus ? (
                        <div className="flex items-center gap-1.5 text-blue-600">
                          <Building size={14} />
                          <span>{item.campus_details?.name || item.campus}</span>
                        </div>
                      ) : <span className="text-slate-400 italic">Chưa xác định</span>}
                    </td>
                    <td className="px-6 py-4">{item.floor_count}</td>
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
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
            <div className="flex justify-between items-center p-4 border-b border-slate-100">
              <h2 className="text-lg font-semibold text-slate-800">
                {editingData ? 'Cập nhật Tòa nhà' : 'Thêm Tòa nhà mới'}
              </h2>
              <button onClick={closeModal} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>
            
            <form onSubmit={handleSubmit(onSubmit)} className="p-4 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Cơ sở trực thuộc <span className="text-red-500">*</span></label>
                <select
                  {...register('campus', { required: 'Vui lòng chọn cơ sở' })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">-- Chọn cơ sở --</option>
                  {campuses.map(c => (
                    <option key={c.id} value={c.id}>{c.code} - {c.name}</option>
                  ))}
                </select>
                {errors.campus && <span className="text-xs text-red-500 mt-1">{errors.campus.message}</span>}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Mã Tòa nhà <span className="text-red-500">*</span></label>
                <input
                  {...register('code', { required: 'Mã không được để trống' })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="VD: TA"
                />
                {errors.code && <span className="text-xs text-red-500 mt-1">{errors.code.message}</span>}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Tên Tòa nhà <span className="text-red-500">*</span></label>
                <input
                  {...register('name', { required: 'Tên không được để trống' })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="VD: Tòa nhà A"
                />
                {errors.name && <span className="text-xs text-red-500 mt-1">{errors.name.message}</span>}
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Số tầng</label>
                <input
                  type="number"
                  {...register('floor_count', { valueAsNumber: true })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex items-center gap-2 mt-4">
                <input
                  type="checkbox"
                  id="is_active"
                  {...register('is_active')}
                  className="rounded border-slate-300 text-blue-600 focus:ring-blue-500"
                />
                <label htmlFor="is_active" className="text-sm text-slate-700">Trạng thái hoạt động</label>
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

      <ConfirmDeleteModal
        isOpen={deleteModal.isOpen}
        onClose={() => setDeleteModal({ isOpen: false, id: null })}
        onConfirm={confirmDelete}
        title="Xóa tòa nhà"
        message="Bạn có chắc chắn muốn xóa tòa nhà này? Hành động này không thể hoàn tác."
        isDeleting={deleteMutation.isPending}
      />
    </div>
  );
}
