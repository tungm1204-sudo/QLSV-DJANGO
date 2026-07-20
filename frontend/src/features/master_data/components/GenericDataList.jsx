import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { Plus, Search, Edit2, Trash2, X } from 'lucide-react';
import { toast } from 'sonner';
import ConfirmDeleteModal from '../../../components/ui/ConfirmDeleteModal';

export default function GenericDataList({ api, title }) {
  const queryClient = useQueryClient();
  const [searchTerm, setSearchTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingData, setEditingData] = useState(null);
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, id: null });

  // Lấy dữ liệu
  const { data: response, isLoading } = useQuery({
    queryKey: ['master-data', title, searchTerm],
    queryFn: () => api.getAll({ search: searchTerm }),
  });

  const records = response?.data?.results || response?.data || [];

  // Mutations
  const createMutation = useMutation({
    mutationFn: (data) => api.create(data),
    onSuccess: () => {
      toast.success(`Thêm ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', title] });
      closeModal();
    },
    onError: () => toast.error(`Có lỗi xảy ra khi thêm ${title.toLowerCase()}`),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => api.update(id, data),
    onSuccess: () => {
      toast.success(`Cập nhật ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', title] });
      closeModal();
    },
    onError: () => toast.error(`Có lỗi xảy ra khi cập nhật ${title.toLowerCase()}`),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(id),
    onSuccess: () => {
      toast.success(`Xóa ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', title] });
      setDeleteModal({ isOpen: false, id: null });
    },
    onError: () => toast.error(`Không thể xóa ${title.toLowerCase()} vì dữ liệu đang được sử dụng`),
  });

  // Modal State
  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  const openModal = (data = null) => {
    if (data) {
      setEditingData(data);
      reset({
        code: data.code,
        name: data.name,
        is_active: data.is_active,
      });
    } else {
      setEditingData(null);
      reset({ code: '', name: '', is_active: true });
    }
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingData(null);
    reset();
  };

  const onSubmit = (data) => {
    if (editingData) {
      updateMutation.mutate({ id: editingData.id, data });
    } else {
      createMutation.mutate(data);
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
        <h1 className="text-2xl font-bold text-slate-800">Quản lý {title}</h1>
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
            placeholder={`Tìm kiếm ${title.toLowerCase()}...`}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 flex-1 overflow-hidden flex flex-col">
        <div className="overflow-x-auto flex-1">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-slate-700 font-medium border-b border-slate-200 sticky top-0">
              <tr>
                <th className="px-6 py-4">Mã</th>
                <th className="px-6 py-4">Tên {title.toLowerCase()}</th>
                <th className="px-6 py-4">Trạng thái</th>
                <th className="px-6 py-4 text-right">Thao tác</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {isLoading ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                    Đang tải dữ liệu...
                  </td>
                </tr>
              ) : records.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-8 text-center text-slate-500">
                    Không tìm thấy dữ liệu.
                  </td>
                </tr>
              ) : (
                records.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="px-6 py-4 font-medium text-slate-900">{item.code}</td>
                    <td className="px-6 py-4">{item.name}</td>
                    <td className="px-6 py-4">
                      {item.is_active !== false ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          Hoạt động
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
                          Ngừng hoạt động
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-2">
                        <button onClick={() => openModal(item)} className="p-1.5 text-slate-400 hover:text-blue-600 transition-colors" title="Sửa">
                          <Edit2 size={16} />
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          className="p-1.5 text-slate-400 hover:text-red-600 transition-colors"
                          title="Xóa"
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

      {/* Modal Form */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <div className="flex justify-between items-center px-6 py-4 border-b border-slate-100">
              <h2 className="text-lg font-semibold text-slate-800">
                {editingData ? `Sửa ${title}` : `Thêm ${title} mới`}
              </h2>
              <button onClick={closeModal} className="text-slate-400 hover:text-slate-600">
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Mã *</label>
                  <input
                    {...register('code', { required: 'Vui lòng nhập mã' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Nhập mã..."
                  />
                  {errors.code && <span className="text-xs text-red-500">{errors.code.message}</span>}
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Tên {title.toLowerCase()} *</label>
                  <input
                    {...register('name', { required: 'Vui lòng nhập tên' })}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder={`Nhập tên ${title.toLowerCase()}...`}
                  />
                  {errors.name && <span className="text-xs text-red-500">{errors.name.message}</span>}
                </div>

                <div className="flex items-center gap-2 mt-2">
                  <input
                    type="checkbox"
                    id="is_active"
                    {...register('is_active')}
                    className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500"
                  />
                  <label htmlFor="is_active" className="text-sm text-slate-700">Trạng thái Hoạt động</label>
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
        message={`Bạn có chắc chắn muốn xóa ${title.toLowerCase()} này không?`}
      />
    </div>
  );
}
