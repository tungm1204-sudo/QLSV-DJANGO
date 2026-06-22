import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { tuitionApi } from '../api/tuition';

export const useTuitionFees = () => {
  return useQuery({
    queryKey: ['tuitionFees'],
    queryFn: () => tuitionApi.getTuitionFees().then(res => res.data.results || res.data),
  });
};

export const usePayTuitionFee = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: tuitionApi.payTuitionFee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tuitionFees'] });
    },
  });
};
