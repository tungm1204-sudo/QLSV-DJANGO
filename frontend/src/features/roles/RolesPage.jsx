import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { usePermissions } from '../../hooks/usePermissions';
import ConfirmModal from '../../components/ui/ConfirmModal';

// Import extracted hook and schema
import { useRoles, useRoleMutations } from './hooks/useRoles';
import { roleSchema, SYSTEM_ROLES } from './validations/roleSchema';
import RoleList from './components/RoleList';
import RoleForm from './components/RoleForm';

// Nhóm các quyền lại để hiển thị Ma trận đẹp hơn
const groupPermissions = (permissionsList) => {
  const groups = {
    'Quản trị Người dùng': [],
    'Phân quyền & Vai trò': [],
    'Hệ thống & Cấu hình': [],
    'Thông báo & Nhật ký': [],
    'Khác': []
  };

  permissionsList.forEach(p => {
    if (p.id.startsWith('USERS_')) groups['Quản trị Người dùng'].push(p);
    else if (p.id.startsWith('ROLES_')) groups['Phân quyền & Vai trò'].push(p);
    else if (p.id.startsWith('SYSTEM_')) groups['Hệ thống & Cấu hình'].push(p);
    else if (p.id.startsWith('NOTIF_') || p.id.startsWith('AUDIT_')) groups['Thông báo & Nhật ký'].push(p);
    else groups['Khác'].push(p);
  });

  return groups;
};

export default function RolesPage() {
  const { hasPermission } = usePermissions();
  const canCreate = hasPermission('ROLES_CREATE');
  const canUpdate = hasPermission('ROLES_UPDATE');
  const canDelete = hasPermission('ROLES_DELETE');

  const [selectedRole, setSelectedRole] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [deleteRoleConfig, setDeleteRoleConfig] = useState({ isOpen: false, roleId: null });

  const isSystemRole = selectedRole && !isCreating && SYSTEM_ROLES.includes(selectedRole.name);

  const { roles, availablePermissions, isLoadingRoles } = useRoles();
  const { createMutation, updateMutation, deleteMutation } = useRoleMutations((resData, actionType) => {
    if (actionType === 'create') {
      setSelectedRole(resData);
      setIsCreating(false);
    } else if (actionType === 'delete') {
      setSelectedRole(null);
      setDeleteRoleConfig({ isOpen: false, roleId: null });
    }
  });

  const form = useForm({
    resolver: zodResolver(roleSchema),
    defaultValues: {
      name: '',
      description: '',
      permissions: []
    }
  });

  // Reset form when selected role changes
  useEffect(() => {
    if (isCreating) {
      form.reset({ name: '', description: '', permissions: [] });
    } else if (selectedRole) {
      form.reset({
        name: selectedRole.name,
        description: selectedRole.description || '',
        permissions: selectedRole.permissions || []
      });
    }
  }, [selectedRole, isCreating, form]);

  const onSubmit = (data) => {
    if (isCreating) {
      createMutation.mutate(data);
    } else if (selectedRole) {
      updateMutation.mutate({ id: selectedRole.id, data });
    }
  };

  const togglePermission = (permId) => {
    if (isSystemRole) return;
    const current = form.getValues('permissions');
    if (current.includes(permId)) {
      form.setValue('permissions', current.filter(id => id !== permId), { shouldDirty: true });
    } else {
      form.setValue('permissions', [...current, permId], { shouldDirty: true });
    }
  };

  const toggleAllPermissions = () => {
    if (isSystemRole) return;
    const current = form.getValues('permissions');
    if (current.length === availablePermissions.length) {
      form.setValue('permissions', [], { shouldDirty: true });
    } else {
      form.setValue('permissions', availablePermissions.map(p => p.id), { shouldDirty: true });
    }
  };

  const toggleGroupPermissions = (permsInGroup) => {
    if (isSystemRole) return;
    const current = form.getValues('permissions');
    const groupPermIds = permsInGroup.map(p => p.id);
    const allSelectedInGroup = groupPermIds.every(id => current.includes(id));

    if (allSelectedInGroup) {
      form.setValue('permissions', current.filter(id => !groupPermIds.includes(id)), { shouldDirty: true });
    } else {
      const newPerms = new Set([...current, ...groupPermIds]);
      form.setValue('permissions', Array.from(newPerms), { shouldDirty: true });
    }
  };

  const groupedPermissions = groupPermissions(availablePermissions);
  const filteredRoles = roles.filter(r => r.name.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="flex h-[calc(100vh-64px)] bg-slate-50 overflow-hidden">
      
      {/* LEFT PANEL: ROLE LIST */}
      <RoleList 
        filteredRoles={filteredRoles}
        isLoadingRoles={isLoadingRoles}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        selectedRole={selectedRole}
        setSelectedRole={setSelectedRole}
        isCreating={isCreating}
        setIsCreating={setIsCreating}
        canCreate={canCreate}
        SYSTEM_ROLES={SYSTEM_ROLES}
        availablePermissions={availablePermissions}
      />

      {/* RIGHT PANEL: ROLE DETAIL / MATRIX */}
      <div className="flex-1 flex flex-col relative overflow-hidden bg-slate-50/50">
        <RoleForm 
          form={form}
          onSubmit={onSubmit}
          selectedRole={selectedRole}
          isCreating={isCreating}
          isSystemRole={isSystemRole}
          canCreate={canCreate}
          canUpdate={canUpdate}
          canDelete={canDelete}
          setDeleteRoleConfig={setDeleteRoleConfig}
          createMutation={createMutation}
          updateMutation={updateMutation}
          availablePermissions={availablePermissions}
          groupedPermissions={groupedPermissions}
          toggleAllPermissions={toggleAllPermissions}
          toggleGroupPermissions={toggleGroupPermissions}
          togglePermission={togglePermission}
        />
      </div>

      <ConfirmModal
        isOpen={deleteRoleConfig.isOpen}
        onClose={() => setDeleteRoleConfig({ isOpen: false, roleId: null })}
        onConfirm={() => deleteMutation.mutate(deleteRoleConfig.roleId)}
        title="Xóa Vai trò"
        message="Bạn có chắc chắn muốn xóa vai trò này? Các người dùng đang có vai trò này có thể bị mất quyền."
        isConfirming={deleteMutation.isPending}
        confirmText="Xóa vai trò"
        cancelText="Hủy bỏ"
        type="danger"
      />
    </div>
  );
}
