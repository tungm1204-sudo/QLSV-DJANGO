import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getStudentsApi, 
  getStudentApi,
  createStudentApi, 
  updateStudentApi, 
  deleteStudentApi,
  importStudentsApi,
  exportStudentsApi,
  printIdCardApi
} from '../api/studentApi';

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

export const useStudents = (filters) => {
  return useQuery({
    queryKey: ['students', filters],
    queryFn: async () => {
      const res = await getStudentsApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useStudentDetail = (id) => {
  return useQuery({
    queryKey: ['students', id],
    queryFn: async () => {
      const res = await getStudentApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useStudentMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createStudentApi,
    onSuccess: () => {
      toast.success('Thêm sinh viên thành công');
      queryClient.invalidateQueries(['students']);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateStudentApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật sinh viên thành công');
      queryClient.invalidateQueries(['students']);
      queryClient.invalidateQueries(['students', variables.id]);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteStudentApi,
    onSuccess: () => {
      toast.success('Xóa sinh viên thành công');
      queryClient.invalidateQueries(['students']);
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

export const useStudentImport = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: importStudentsApi,
    onSuccess: (res) => {
      toast.success(res.data?.detail || 'Import thành công');
      queryClient.invalidateQueries(['students']);
    },
    onError: handleError
  });
};
