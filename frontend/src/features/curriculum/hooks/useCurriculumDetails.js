import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getKnowledgeBlocksApi,
  createKnowledgeBlockApi,
  updateKnowledgeBlockApi,
  deleteKnowledgeBlockApi,
  getTrainingProgramCoursesApi,
  createTrainingProgramCourseApi,
  updateTrainingProgramCourseApi,
  deleteTrainingProgramCourseApi
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

export const useKnowledgeBlocks = (filters) => {
  return useQuery({
    queryKey: ['knowledge-blocks', filters],
    queryFn: async () => {
      const res = await getKnowledgeBlocksApi(filters);
      return res.data;
    },
    enabled: !!filters?.training_program,
  });
};

export const useKnowledgeBlockMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createKnowledgeBlockApi,
    onSuccess: () => {
      toast.success('Thêm Khối kiến thức thành công');
      queryClient.invalidateQueries({ queryKey: ['knowledge-blocks'] });
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateKnowledgeBlockApi,
    onSuccess: () => {
      toast.success('Cập nhật Khối kiến thức thành công');
      queryClient.invalidateQueries({ queryKey: ['knowledge-blocks'] });
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteKnowledgeBlockApi,
    onSuccess: () => {
      toast.success('Xóa Khối kiến thức thành công');
      queryClient.invalidateQueries({ queryKey: ['knowledge-blocks'] });
      queryClient.invalidateQueries({ queryKey: ['training-programs'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  return { createMutation, updateMutation, deleteMutation };
};

export const useTrainingProgramCourses = (filters) => {
  return useQuery({
    queryKey: ['training-program-courses', filters],
    queryFn: async () => {
      const res = await getTrainingProgramCoursesApi(filters);
      return res.data;
    },
    enabled: !!filters?.training_program || !!filters?.knowledge_block,
  });
};

export const useTrainingProgramCourseMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createTrainingProgramCourseApi,
    onSuccess: () => {
      toast.success('Thêm Học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['training-program-courses'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateTrainingProgramCourseApi,
    onSuccess: () => {
      toast.success('Cập nhật Học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['training-program-courses'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteTrainingProgramCourseApi,
    onSuccess: () => {
      toast.success('Gỡ bỏ Học phần thành công');
      queryClient.invalidateQueries({ queryKey: ['training-program-courses'] });
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  return { createMutation, updateMutation, deleteMutation };
};
