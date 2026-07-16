import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { toast } from 'sonner';
import { 
  Users, Search, Plus, MoreVertical, ShieldAlert, ShieldCheck, 
  Edit2, Trash2, KeyRound, Loader2 
} from 'lucide-react';

import { getUsersApi, createUserApi, updateUserApi, lockUserApi, unlockUserApi, resetPasswordApi } from '../../api/users';
import { getRolesApi } from '../../api/roles';
import { usePermissions } from '../../hooks/usePermissions';
import { cn } from '../../utils';

const userSchema = z.object({
  email: z.string().email('Email không hợp lệ'),
  full_name: z.string().min(2, 'Tên phải từ 2 ký tự').max(100),
  password: z.string().min(6, 'Mật khẩu phải từ 6 ký tự').optional().or(z.literal('')),
  // FIX: field phải là role_id (UUID) để Backend xử lý qua UserCreateUpdateSerializer
  role_id: z.string().uuid('Vai trò không hợp lệ').optional().nullable(),
});

export default function UsersPage() {
  const queryClient = useQueryClient();
  const { hasPermission } = usePermissions();
  const canCreate = hasPermission('USERS_CREATE');
  const canUpdate = hasPermission('USERS_UPDATE');
  const canDelete = hasPermission('USERS_DELETE');

  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);

  // Fetch Users
  const { data: usersData, isLoading: isLoadingUsers } = useQuery({
    queryKey: ['users', searchQuery],
    queryFn: async () => {
      const res = await getUsersApi({ search: searchQuery });
      return res.data;
    }
  });

  // Fetch Roles for the Select Dropdown
  const { data: rolesData } = useQuery({
    queryKey: ['roles'],
    queryFn: async () => {
      const res = await getRolesApi();
      return res.data;
    }
  });

  const users = Array.isArray(usersData) ? usersData : usersData?.results || [];
  const roles = Array.isArray(rolesData) ? rolesData : rolesData?.results || [];

  const form = useForm({
    resolver: zodResolver(userSchema),
    defaultValues: { email: '', full_name: '', password: '', role_id: null }
  });

  const handleOpenModal = (user = null) => {
    if (user) {
      setSelectedUser(user);
      form.reset({
        email: user.email,
        full_name: user.full_name,
        password: '',
        role_id: user.role?.id || null
      });
    } else {
      setSelectedUser(null);
      form.reset({ email: '', full_name: '', password: '', role_id: null });
    }
    setIsModalOpen(true);
  };

  const handleError = (err) => {
    if (err.response?.data) {
      const data = err.response.data;
      if (data.detail) return toast.error(data.detail);
      // DRF validation errors usually come as an object mapping field names to arrays of messages
      const firstErrorKey = Object.keys(data)[0];
      if (firstErrorKey && Array.isArray(data[firstErrorKey])) {
        return toast.error(`${firstErrorKey}: ${data[firstErrorKey][0]}`);
      }
    }
    toast.error('Có lỗi xảy ra');
  };

  const createMutation = useMutation({
    mutationFn: createUserApi,
    onSuccess: () => {
      toast.success('Thêm người dùng thành công');
      queryClient.invalidateQueries(['users']);
      setIsModalOpen(false);
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateUserApi,
    onSuccess: () => {
      toast.success('Cập nhật người dùng thành công');
      queryClient.invalidateQueries(['users']);
      setIsModalOpen(false);
    },
    onError: handleError
  });

  const lockUnlockMutation = useMutation({
    mutationFn: ({ id, isLocked }) => isLocked ? unlockUserApi(id) : lockUserApi(id),
    onSuccess: (_, variables) => {
      toast.success(variables.isLocked ? 'Đã mở khóa tài khoản' : 'Đã khóa tài khoản');
      queryClient.invalidateQueries(['users']);
    },
    onError: handleError
  });

  const onSubmit = (data) => {
    // Nếu đang update, password có thể rỗng -> xóa khỏi payload
    if (selectedUser && !data.password) {
      delete data.password;
    }
    
    // FIX: xóa role_id nếu không chọn (null/empty string) để backend không bị lỗi validate
    if (!data.role_id) delete data.role_id;

    if (selectedUser) {
      updateMutation.mutate({ id: selectedUser.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-6">
      
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Users className="text-indigo-600" />
            Quản lý Người dùng
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Quản lý thông tin, vai trò và trạng thái truy cập của tất cả tài khoản.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => handleOpenModal()}
            disabled={!canCreate}
            className={cn(
              "inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold shadow-sm transition-all",
              canCreate ? "bg-indigo-600 hover:bg-indigo-700 text-white" : "bg-slate-200 text-slate-400 cursor-not-allowed"
            )}
            title={!canCreate ? "Bạn không có quyền thực hiện hành động này" : ""}
          >
            <Plus size={16} />
            Thêm người dùng
          </button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input 
            type="text" 
            placeholder="Tìm kiếm theo email, họ tên..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
          />
        </div>
      </div>

      {/* Data Table */}
      <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-slate-50 border-b border-slate-200 text-slate-600">
              <tr>
                <th className="px-6 py-4 font-semibold">Người dùng</th>
                <th className="px-6 py-4 font-semibold">Vai trò</th>
                <th className="px-6 py-4 font-semibold">Trạng thái</th>
                <th className="px-6 py-4 font-semibold text-right">Hành động</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoadingUsers ? (
                // SKELETON LOADING
                Array.from({ length: 5 }).map((_, idx) => (
                  <tr key={idx}>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-slate-200 animate-pulse"></div>
                        <div className="space-y-2">
                          <div className="w-32 h-4 bg-slate-200 rounded animate-pulse"></div>
                          <div className="w-24 h-3 bg-slate-100 rounded animate-pulse"></div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4"><div className="w-20 h-5 bg-slate-200 rounded-full animate-pulse"></div></td>
                    <td className="px-6 py-4"><div className="w-16 h-5 bg-slate-200 rounded-full animate-pulse"></div></td>
                    <td className="px-6 py-4 text-right"><div className="w-8 h-8 bg-slate-200 rounded ml-auto animate-pulse"></div></td>
                  </tr>
                ))
              ) : users.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-12 text-center text-slate-500">
                    <div className="flex flex-col items-center justify-center">
                      <Users size={32} className="text-slate-300 mb-3" />
                      <p>Không tìm thấy người dùng nào phù hợp</p>
                    </div>
                  </td>
                </tr>
              ) : (
                users.map((user) => {
                  const isLocked = !user.is_active || user.status === 'LOCKED';
                  return (
                    <tr key={user.id} className="hover:bg-slate-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <img 
                            src={user.avatar || `https://ui-avatars.com/api/?name=${encodeURIComponent(user.full_name)}&background=e0e7ff&color=4f46e5`} 
                            alt={user.full_name} 
                            className="w-10 h-10 rounded-full border border-slate-200 object-cover"
                          />
                          <div>
                            <div className="font-semibold text-slate-900">{user.full_name}</div>
                            <div className="text-xs text-slate-500">{user.email}</div>
                          </div>
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        {user.role ? (
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-100">
                            {user.role.name}
                          </span>
                        ) : (
                          <span className="text-xs text-slate-400 italic">Chưa phân vai trò</span>
                        )}
                      </td>
                      <td className="px-6 py-4">
                        <span className={cn(
                          "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wider",
                          isLocked ? "bg-red-50 text-red-700 border border-red-100" : "bg-emerald-50 text-emerald-700 border border-emerald-100"
                        )}>
                          {isLocked ? <ShieldAlert size={12} /> : <ShieldCheck size={12} />}
                          {isLocked ? 'Bị Khóa' : 'Hoạt động'}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-right">
                        <div className="flex items-center justify-end gap-2">
                          <button 
                            onClick={() => handleOpenModal(user)}
                            disabled={!canUpdate}
                            className={cn(
                              "p-1.5 rounded-lg transition-colors",
                              canUpdate ? "text-slate-400 hover:text-indigo-600 hover:bg-indigo-50" : "text-slate-200 cursor-not-allowed"
                            )}
                            title={!canUpdate ? "Không có quyền sửa" : "Sửa thông tin"}
                          >
                            <Edit2 size={16} />
                          </button>
                          <button 
                            onClick={() => lockUnlockMutation.mutate({ id: user.id, isLocked })}
                            disabled={!canUpdate}
                            className={cn(
                              "p-1.5 rounded-lg transition-colors",
                              !canUpdate ? "text-slate-200 cursor-not-allowed" :
                              isLocked ? "text-emerald-500 hover:bg-emerald-50" : "text-red-500 hover:bg-red-50"
                            )}
                            title={!canUpdate ? "Không có quyền cập nhật trạng thái" : isLocked ? "Mở khóa tài khoản" : "Khóa tài khoản"}
                          >
                            {isLocked ? <ShieldCheck size={16} /> : <ShieldAlert size={16} />}
                          </button>
                          <button 
                            disabled={!canUpdate}
                            className={cn(
                              "p-1.5 rounded-lg transition-colors",
                              canUpdate ? "text-slate-400 hover:text-orange-600 hover:bg-orange-50" : "text-slate-200 cursor-not-allowed"
                            )}
                            title={!canUpdate ? "Không có quyền reset mật khẩu" : "Reset mật khẩu khẩn cấp"}
                            onClick={() => {
                              const newPass = prompt(`Nhập mật khẩu mới cho ${user.email}:`);
                              if (newPass) {
                                resetPasswordApi({ id: user.id, new_password: newPass })
                                  .then(() => toast.success('Đổi mật khẩu thành công'))
                                  .catch(() => toast.error('Lỗi khi đổi mật khẩu'));
                              }
                            }}
                          >
                            <KeyRound size={16} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal User Form */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
              <h2 className="text-lg font-bold text-slate-800">
                {selectedUser ? 'Sửa thông tin Người dùng' : 'Thêm Người dùng mới'}
              </h2>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                ✕
              </button>
            </div>
            
            <form onSubmit={form.handleSubmit(onSubmit)} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Họ và tên <span className="text-red-500">*</span></label>
                <input 
                  {...form.register('full_name')}
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                  placeholder="Nhập họ và tên..."
                />
                {form.formState.errors.full_name && <p className="text-xs text-red-500 mt-1">{form.formState.errors.full_name.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Email <span className="text-red-500">*</span></label>
                <input 
                  {...form.register('email')}
                  type="email"
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                  placeholder="admin@qlsv.edu.vn"
                  disabled={!!selectedUser}
                />
                {form.formState.errors.email && <p className="text-xs text-red-500 mt-1">{form.formState.errors.email.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">
                  Mật khẩu {selectedUser ? '(Để trống nếu không đổi)' : <span className="text-red-500">*</span>}
                </label>
                <input 
                  {...form.register('password')}
                  type="password"
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                  placeholder="******"
                />
                {form.formState.errors.password && <p className="text-xs text-red-500 mt-1">{form.formState.errors.password.message}</p>}
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1.5">Vai trò</label>
                <select 
                  {...form.register('role_id')}
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                >
                  <option value="">-- Không chọn vai trò --</option>
                  {roles.map(r => (
                    <option key={r.id} value={r.id}>{r.name}</option>
                  ))}
                </select>
                {form.formState.errors.role_id && <p className="text-xs text-red-500 mt-1">{form.formState.errors.role_id.message}</p>}
              </div>

              <div className="pt-4 flex gap-3">
                <button 
                  type="button" 
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 px-4 py-2 text-sm font-semibold text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors"
                >
                  Hủy
                </button>
                <button 
                  type="submit"
                  disabled={createMutation.isPending || updateMutation.isPending}
                  className="flex-1 px-4 py-2 text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 rounded-xl transition-colors flex items-center justify-center"
                >
                  {(createMutation.isPending || updateMutation.isPending) ? <Loader2 size={18} className="animate-spin" /> : 'Lưu lại'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
