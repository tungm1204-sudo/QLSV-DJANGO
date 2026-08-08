import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';

export function useMasterDataCrud({ api, queryKey, title, searchTerm }) {
  const queryClient = useQueryClient();

  const { data: response, isLoading } = useQuery({
    queryKey: ['master-data', queryKey, searchTerm],
    queryFn: () => api.getAll({ search: searchTerm }),
    keepPreviousData: true,
  });

  const records = response?.data?.results || response?.data || [];

  const createMutation = useMutation({
    mutationFn: (data) => api.create(data),
    onSuccess: () => {
      toast.success(`Thêm ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', queryKey] });
    },
    onError: () => toast.error(`Có lỗi xảy ra khi thêm ${title.toLowerCase()}`),
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => api.update(id, data),
    onSuccess: () => {
      toast.success(`Cập nhật ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', queryKey] });
    },
    onError: () => toast.error(`Có lỗi xảy ra khi cập nhật ${title.toLowerCase()}`),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(id),
    onSuccess: () => {
      toast.success(`Xóa ${title.toLowerCase()} thành công`);
      queryClient.invalidateQueries({ queryKey: ['master-data', queryKey] });
    },
    onError: (error) => toast.error(error.response?.data?.detail || `Không thể xóa ${title.toLowerCase()} vì dữ liệu đang được sử dụng`),
  });

  return {
    records,
    isLoading,
    createMutation,
    updateMutation,
    deleteMutation,
  };
}
