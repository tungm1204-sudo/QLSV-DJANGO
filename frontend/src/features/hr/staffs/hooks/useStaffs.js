import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { staffApi } from '../api/staffApi';
import { toast } from 'sonner';

// 1. Hook lấy danh sách nhân viên (có phân trang, filter)
export const useStaffs = (params) => {
  return useQuery({
    queryKey: ['staffs', params],
    queryFn: async () => {
      const response = await staffApi.getAll(params);
      return response.data; // DRF trả về { count, next, previous, results }
    },
    keepPreviousData: true,
  });
};

// 2. Hook lấy chi tiết nhân viên theo ID
export const useStaffDetail = (id) => {
  return useQuery({
    queryKey: ['staff', id],
    queryFn: async () => {
      const response = await staffApi.getById(id);
      return response.data;
    },
    enabled: !!id, // Chỉ gọi API khi có id hợp lệ
  });
};

// 3. Hook chứa các mutation (Create, Update, Delete)
export const useStaffMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: staffApi.create,
    onSuccess: () => {
      toast.success('Thêm nhân viên thành công!');
      queryClient.invalidateQueries({ queryKey: ['staffs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: (error) => {
      const msg = error.response?.data?.message || 'Có lỗi xảy ra khi thêm nhân viên.';
      toast.error(msg);
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => staffApi.update(id, data),
    onSuccess: (data, variables) => {
      toast.success('Cập nhật nhân viên thành công!');
      queryClient.invalidateQueries({ queryKey: ['staffs'] });
      queryClient.invalidateQueries({ queryKey: ['staff', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: (error) => {
      const msg = error.response?.data?.message || 'Có lỗi xảy ra khi cập nhật.';
      toast.error(msg);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: staffApi.delete,
    onSuccess: () => {
      toast.success('Xóa nhân viên thành công!');
      queryClient.invalidateQueries({ queryKey: ['staffs'] });
    },
    onError: (error) => {
      const msg = error.response?.data?.message || 'Không thể xóa nhân viên này.';
      toast.error(msg);
    },
  });

  return {
    createMutation,
    updateMutation,
    deleteMutation,
  };
};

// 4. Hook import Excel
export const useImportStaffs = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: staffApi.importExcel,
    onSuccess: (response) => {
      toast.success(response.data?.message || 'Import danh sách nhân viên thành công!');
      queryClient.invalidateQueries({ queryKey: ['staffs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: (error) => {
      const msg = error.response?.data?.error || 'Lỗi khi import file Excel.';
      toast.error(msg);
    },
  });
};
