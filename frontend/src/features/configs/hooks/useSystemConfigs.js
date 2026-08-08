import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { getSystemConfigsApi, updateSystemConfigApi, createSystemConfigApi } from '../api/configApi';

export function useSystemConfigs(canView) {
  const queryClient = useQueryClient();

  const { data: configsData, isLoading } = useQuery({
    queryKey: ['systemConfigs'],
    queryFn: getSystemConfigsApi,
    enabled: canView,
  });

  const updateMutation = useMutation({
    mutationFn: async (payloads) => {
      const promises = payloads.map(p => {
        if (p.id) {
          return updateSystemConfigApi(p.id, { key: p.key, value: p.value });
        } else {
          return createSystemConfigApi({ key: p.key, value: p.value, description: p.description });
        }
      });
      return Promise.all(promises);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['systemConfigs']);
      toast.success('Lưu cấu hình thành công!');
    },
    onError: () => toast.error('Lỗi khi lưu cấu hình.'),
  });

  return {
    configsData,
    isLoading,
    updateMutation,
  };
}
