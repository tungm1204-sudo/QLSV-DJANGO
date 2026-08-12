import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getLecturersApi, 
  getLecturerApi,
  createLecturerApi, 
  updateLecturerApi, 
  deleteLecturerApi,
  importLecturersApi,
  exportLecturersApi
} from '../api/lecturerApi';

const handleError = (err) => {
  if (err.response?.data) {
    const data = err.response.data;
    if (data.detail) return toast.error(data.detail);
    const firstErrorKey = Object.keys(data)[0];
    if (firstErrorKey && Array.isArray(data[firstErrorKey])) {
      return toast.error(`${firstErrorKey}: ${data[firstErrorKey][0]}`);
    }
  }
  toast.error('Có lỗi xảy ra');
};

export const useLecturers = (filters) => {
  return useQuery({
    queryKey: ['lecturers', filters],
    queryFn: async () => {
      const res = await getLecturersApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useLecturerDetail = (id) => {
  return useQuery({
    queryKey: ['lecturers', id],
    queryFn: async () => {
      const res = await getLecturerApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useLecturerMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createLecturerApi,
    onSuccess: () => {
      toast.success('Thêm giảng viên thành công');
      queryClient.invalidateQueries({ queryKey: ['lecturers'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateLecturerApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật giảng viên thành công');
      queryClient.invalidateQueries({ queryKey: ['lecturers'] });
      queryClient.invalidateQueries({ queryKey: ['lecturers', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteLecturerApi,
    onSuccess: () => {
      toast.success('Xóa giảng viên thành công');
      queryClient.invalidateQueries({ queryKey: ['lecturers'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  return {
    createMutation,
    updateMutation,
    deleteMutation
  };
};

export const useLecturerImport = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: importLecturersApi,
    onSuccess: (res) => {
      toast.success(res.data?.detail || 'Import thành công');
      queryClient.invalidateQueries({ queryKey: ['lecturers'] });
    },
    onError: handleError
  });
};
