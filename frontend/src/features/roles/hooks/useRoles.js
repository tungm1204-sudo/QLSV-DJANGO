import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { getRolesApi, createRoleApi, updateRoleApi, deleteRoleApi, getAvailablePermissionsApi } from '../api/roleApi';

export function useRoles() {
  const queryClient = useQueryClient();

  const { data: rolesResponse, isLoading: isLoadingRoles } = useQuery({
    queryKey: ['roles'],
    queryFn: async () => {
      const res = await getRolesApi();
      return res.data;
    }
  });

  const { data: availablePermissions = [] } = useQuery({
    queryKey: ['permissions'],
    queryFn: async () => {
      const res = await getAvailablePermissionsApi();
      return res.data;
    }
  });

  const roles = Array.isArray(rolesResponse) ? rolesResponse : rolesResponse?.results || [];

  return { roles, availablePermissions, isLoadingRoles };
}

export function useRoleMutations(onSuccessCallback) {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createRoleApi,
    onSuccess: (res) => {
      queryClient.invalidateQueries(['roles']);
      toast.success('Thêm vai trò mới thành công!');
      if (onSuccessCallback) onSuccessCallback(res.data, 'create');
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi tạo vai trò');
    }
  });

  const updateMutation = useMutation({
    mutationFn: updateRoleApi,
    onSuccess: (res) => {
      queryClient.invalidateQueries(['roles']);
      toast.success('Cập nhật vai trò thành công!');
      if (onSuccessCallback) onSuccessCallback(res.data, 'update');
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi cập nhật vai trò');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: deleteRoleApi,
    onSuccess: () => {
      queryClient.invalidateQueries(['roles']);
      toast.success('Đã xóa vai trò!');
      if (onSuccessCallback) onSuccessCallback(null, 'delete');
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi xóa vai trò');
    }
  });

  return { createMutation, updateMutation, deleteMutation };
}
