import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getSessionsApi, revokeSessionApi } from '../api/authApi';

export function useSessionManagement(isOpen) {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['login-sessions'],
    queryFn: async () => {
      const res = await getSessionsApi();
      return res.data;
    },
    enabled: isOpen,
  });

  const revokeMutation = useMutation({
    mutationFn: (sessionId) => revokeSessionApi(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries(['login-sessions']);
    },
  });

  return { data, isLoading, isError, error, revokeMutation };
}
