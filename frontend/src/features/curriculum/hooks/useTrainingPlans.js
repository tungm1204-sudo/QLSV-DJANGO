import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getTrainingPlansApi, 
  getTrainingPlanApi,
  createTrainingPlanApi, 
  updateTrainingPlanApi, 
  deleteTrainingPlanApi,
  approveTrainingPlanApi,
  duplicateTrainingPlanApi
} from '../api/trainingPlanApi';

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

export const useTrainingPlans = (filters) => {
  return useQuery({
    queryKey: ['training-plans', filters],
    queryFn: async () => {
      const res = await getTrainingPlansApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useTrainingPlanDetail = (id) => {
  return useQuery({
    queryKey: ['training-plans', id],
    queryFn: async () => {
      const res = await getTrainingPlanApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useTrainingPlanMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createTrainingPlanApi,
    onSuccess: () => {
      toast.success('Thêm kế hoạch thành công');
      queryClient.invalidateQueries({ queryKey: ['training-plans'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateTrainingPlanApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật kế hoạch thành công');
      queryClient.invalidateQueries({ queryKey: ['training-plans'] });
      queryClient.invalidateQueries({ queryKey: ['training-plans', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTrainingPlanApi,
    onSuccess: () => {
      toast.success('Xóa kế hoạch thành công');
      queryClient.invalidateQueries({ queryKey: ['training-plans'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const approveMutation = useMutation({
    mutationFn: approveTrainingPlanApi,
    onSuccess: (data, variables) => {
      toast.success('Phê duyệt kế hoạch thành công');
      queryClient.invalidateQueries({ queryKey: ['training-plans'] });
      queryClient.invalidateQueries({ queryKey: ['training-plans', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const duplicateMutation = useMutation({
    mutationFn: duplicateTrainingPlanApi,
    onSuccess: () => {
      toast.success('Sao chép kế hoạch thành công');
      queryClient.invalidateQueries({ queryKey: ['training-plans'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  return {
    createMutation,
    updateMutation,
    deleteMutation,
    approveMutation,
    duplicateMutation
  };
};
