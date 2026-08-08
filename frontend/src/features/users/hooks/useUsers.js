import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getUsersApi, 
  createUserApi, 
  updateUserApi, 
  lockUserApi, 
  unlockUserApi, 
  resetPasswordApi, 
  deleteUserApi 
} from '../api/userApi';
import { getRolesApi } from '../../roles/api/roleApi';

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

export const useUsers = (searchQuery) => {
  return useQuery({
    queryKey: ['users', searchQuery],
    queryFn: async () => {
      const res = await getUsersApi({ search: searchQuery });
      return res.data;
    }
  });
};

export const useRolesOptions = () => {
  return useQuery({
    queryKey: ['roles', 'all'],
    queryFn: async () => {
      const res = await getRolesApi(); // Need to import getRolesApi
      return res.data;
    }
  });
};

export const useUserMutations = (onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createUserApi,
    onSuccess: () => {
      toast.success('Thêm người dùng thành công');
      queryClient.invalidateQueries(['users']);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateUserApi,
    onSuccess: () => {
      toast.success('Cập nhật người dùng thành công');
      queryClient.invalidateQueries(['users']);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const lockUnlockMutation = useMutation({
    mutationFn: ({ id, isLocked }) => isLocked ? unlockUserApi(id) : lockUserApi(id),
    onSuccess: (_, variables) => {
      toast.success(variables.isLocked ? 'Đã mở khóa tài khoản' : 'Đã khóa tài khoản');
      queryClient.invalidateQueries(['users']);
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi cập nhật trạng thái');
    }
  });

  const resetPasswordMutation = useMutation({
    mutationFn: resetPasswordApi,
    onSuccess: () => {
      toast.success('Đổi mật khẩu thành công');
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi đổi mật khẩu');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: deleteUserApi,
    onSuccess: () => {
      toast.success('Xóa người dùng thành công');
      queryClient.invalidateQueries(['users']);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: (err) => {
      toast.error(err.response?.data?.detail || 'Lỗi khi xóa người dùng');
    }
  });

  return {
    createMutation,
    updateMutation,
    lockUnlockMutation,
    resetPasswordMutation,
    deleteMutation
  };
};
