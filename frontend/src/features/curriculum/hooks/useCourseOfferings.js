import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getCourseOfferingsApi, 
  getCourseOfferingApi,
  createCourseOfferingApi, 
  updateCourseOfferingApi, 
  deleteCourseOfferingApi
} from '../api/courseOfferingApi';

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

export const useCourseOfferings = (filters) => {
  return useQuery({
    queryKey: ['course-offerings', filters],
    queryFn: async () => {
      const res = await getCourseOfferingsApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useCourseOfferingDetail = (id) => {
  return useQuery({
    queryKey: ['course-offerings', id],
    queryFn: async () => {
      const res = await getCourseOfferingApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useCourseOfferingMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createCourseOfferingApi,
    onSuccess: () => {
      toast.success('Thêm lớp học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['course-offerings'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateCourseOfferingApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật lớp học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['course-offerings'] });
      queryClient.invalidateQueries({ queryKey: ['course-offerings', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCourseOfferingApi,
    onSuccess: () => {
      toast.success('Xóa lớp học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['course-offerings'] });
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
