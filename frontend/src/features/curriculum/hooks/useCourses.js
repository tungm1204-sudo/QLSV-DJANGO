import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getCoursesApi, 
  getCourseApi,
  createCourseApi, 
  updateCourseApi, 
  deleteCourseApi
} from '../api/courseApi';

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

export const useCourses = (filters) => {
  return useQuery({
    queryKey: ['courses', filters],
    queryFn: async () => {
      const res = await getCoursesApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useCourseDetail = (id) => {
  return useQuery({
    queryKey: ['courses', id],
    queryFn: async () => {
      const res = await getCourseApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useCourseMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createCourseApi,
    onSuccess: () => {
      toast.success('Thêm môn học thành công');
      queryClient.invalidateQueries({ queryKey: ['courses'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateCourseApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật môn học thành công');
      queryClient.invalidateQueries({ queryKey: ['courses'] });
      queryClient.invalidateQueries({ queryKey: ['courses', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCourseApi,
    onSuccess: () => {
      toast.success('Xóa môn học thành công');
      queryClient.invalidateQueries({ queryKey: ['courses'] });
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
