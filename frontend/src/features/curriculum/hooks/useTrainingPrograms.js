import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getTrainingProgramsApi, 
  getTrainingProgramApi,
  createTrainingProgramApi, 
  updateTrainingProgramApi, 
  deleteTrainingProgramApi
} from '../api/trainingProgramApi';

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

export const useTrainingPrograms = (filters) => {
  return useQuery({
    queryKey: ['training-programs', filters],
    queryFn: async () => {
      const res = await getTrainingProgramsApi(filters);
      return res.data;
    },
    keepPreviousData: true,
  });
};

export const useTrainingProgramDetail = (id) => {
  return useQuery({
    queryKey: ['training-programs', id],
    queryFn: async () => {
      const res = await getTrainingProgramApi(id);
      return res.data;
    },
    enabled: !!id,
  });
};

export const useTrainingProgramMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createTrainingProgramApi,
    onSuccess: () => {
      toast.success('Thêm khung chương trình thành công');
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateTrainingProgramApi,
    onSuccess: (data, variables) => {
      toast.success('Cập nhật khung chương trình thành công');
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
      queryClient.invalidateQueries({ queryKey: ['training-programs', variables.id] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTrainingProgramApi,
    onSuccess: () => {
      toast.success('Xóa khung chương trình thành công');
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
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
