import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getSchedulesApi, 
  getScheduleApi,
  createScheduleApi, 
  updateScheduleApi, 
  deleteScheduleApi,
  validateScheduleApi
} from '../api/scheduleApi';

const handleError = (err) => {
  if (err.response?.data) {
    const data = err.response.data;
    if (data.detail) {
      if (Array.isArray(data.detail)) {
        return toast.error(data.detail[0]);
      }
      return toast.error(data.detail);
    }
    const firstErrorKey = Object.keys(data)[0];
    if (firstErrorKey && Array.isArray(data[firstErrorKey])) {
      return toast.error(`${firstErrorKey}: ${data[firstErrorKey][0]}`);
    }
  }
  toast.error('Có lỗi xảy ra');
};

export const useSchedules = (filters) => {
  return useQuery({
    queryKey: ['schedules', filters],
    queryFn: async () => {
      const res = await getSchedulesApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useScheduleDetail = (id) => {
  return useQuery({
    queryKey: ['schedules', id],
    queryFn: async () => {
      const res = await getScheduleApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useScheduleMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createScheduleApi,
    onSuccess: () => {
      toast.success('Xếp lịch thành công');
      queryClient.invalidateQueries({ queryKey: ['schedules'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateScheduleApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật lịch thành công');
      queryClient.invalidateQueries({ queryKey: ['schedules'] });
      queryClient.invalidateQueries({ queryKey: ['schedules', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteScheduleApi,
    onSuccess: () => {
      toast.success('Xóa lịch thành công');
      queryClient.invalidateQueries({ queryKey: ['schedules'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });
  
  const validateMutation = useMutation({
    mutationFn: validateScheduleApi,
  });

  return {
    createMutation,
    updateMutation,
    deleteMutation,
    validateMutation
  };
};
