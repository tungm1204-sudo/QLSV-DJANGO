import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toast } from 'sonner';
import { Users, Search, Plus, Loader2 } from 'lucide-react';

import { usePermissions } from '../../hooks/usePermissions';
import useAuthStore from '../../stores/useAuthStore';
import ConfirmModal from '../../components/ui/ConfirmModal';
import { cn } from '../../utils';

import { useUsers, useUserMutations, useRolesOptions } from './hooks/useUsers';
import { userSchema } from './validations/userSchema';
import UserTable from './components/UserTable';
import UserForm from './components/UserForm';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog';

export default function UsersPage() {
  const { user: currentUser } = useAuthStore();
  const { hasPermission } = usePermissions();
  const canCreate = hasPermission('USERS_CREATE');
  const canUpdate = hasPermission('USERS_UPDATE');
  const canDelete = hasPermission('USERS_DELETE');

  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [resetPasswordUser, setResetPasswordUser] = useState(null);
  const [resetPasswordValue, setResetPasswordValue] = useState('');
  const [deleteUserConfig, setDeleteUserConfig] = useState({ isOpen: false, userId: null });

  // Fetch Users via Hook
  const { data: usersData, isLoading: isLoadingUsers } = useUsers(searchQuery);

  // Use Mutations via Hook
  const {
    createMutation,
    updateMutation,
    lockUnlockMutation,
    resetPasswordMutation,
    deleteMutation
  } = useUserMutations(() => {
    setIsModalOpen(false);
    setResetPasswordUser(null);
    setResetPasswordValue('');
    setDeleteUserConfig({ isOpen: false, userId: null });
  });

  // Fetch Roles for the Select Dropdown via Hook
  const { data: rolesData } = useRolesOptions();

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
          <Button 
            onClick={() => handleOpenModal()}
            disabled={!canCreate}
            className={cn(
              "shadow-sm",
              canCreate ? "bg-indigo-600 hover:bg-indigo-700 text-white" : ""
            )}
            title={!canCreate ? "Bạn không có quyền thực hiện hành động này" : ""}
          >
            <Plus size={16} className="mr-2" />
            Thêm người dùng
          </Button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <Input 
            type="text" 
            placeholder="Tìm kiếm theo email, họ tên..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-slate-50 border-slate-200"
          />
        </div>
      </div>

      {/* Data Table Component */}
      <UserTable 
        users={users}
        isLoadingUsers={isLoadingUsers}
        currentUser={currentUser}
        canUpdate={canUpdate}
        canDelete={canDelete}
        handleOpenModal={handleOpenModal}
        lockUnlockMutation={lockUnlockMutation}
        setResetPasswordUser={setResetPasswordUser}
        setResetPasswordValue={setResetPasswordValue}
        setDeleteUserConfig={setDeleteUserConfig}
      />

      {/* Modal User Form Component */}
      <UserForm 
        isModalOpen={isModalOpen}
        setIsModalOpen={setIsModalOpen}
        selectedUser={selectedUser}
        form={form}
        onSubmit={onSubmit}
        roles={roles}
        isPending={createMutation.isPending || updateMutation.isPending}
      />

      {/* Reset Password Modal */}
      <Dialog open={!!resetPasswordUser} onOpenChange={(open) => {
        if (!open) setResetPasswordUser(null);
      }}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle>Reset Mật Khẩu</DialogTitle>
            <DialogDescription>
              Nhập mật khẩu mới cho tài khoản <span className="font-semibold text-slate-900">{resetPasswordUser?.email}</span>
            </DialogDescription>
          </DialogHeader>
          <div className="py-4">
            <Input
              type="password"
              value={resetPasswordValue}
              onChange={(e) => setResetPasswordValue(e.target.value)}
              placeholder="Mật khẩu mới (ít nhất 6 ký tự)"
            />
          </div>
          <DialogFooter className="sm:justify-end">
            <Button 
              type="button" 
              variant="outline" 
              onClick={() => setResetPasswordUser(null)}
            >
              Hủy
            </Button>
            <Button 
              onClick={() => {
                if (resetPasswordValue.length < 6) {
                  toast.error('Mật khẩu phải từ 6 ký tự');
                  return;
                }
                resetPasswordMutation.mutate({ id: resetPasswordUser.id, new_password: resetPasswordValue });
              }}
              disabled={resetPasswordMutation.isPending}
            >
              {resetPasswordMutation.isPending && <Loader2 size={16} className="animate-spin mr-2" />}
              Xác nhận
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirm Modal */}
      <ConfirmModal
        isOpen={deleteUserConfig.isOpen}
        onClose={() => setDeleteUserConfig({ isOpen: false, userId: null })}
        onConfirm={() => deleteMutation.mutate(deleteUserConfig.userId)}
        title="Xóa người dùng"
        message="Bạn có chắc chắn muốn xóa người dùng này khỏi hệ thống? Dữ liệu đã xóa sẽ không thể khôi phục."
      />
    </div>
  );
}
