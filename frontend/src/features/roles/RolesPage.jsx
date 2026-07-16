import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Shield, Plus, MoreVertical, Trash2, Edit2, Search, CheckCircle2, ShieldCheck, Users } from 'lucide-react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { getRolesApi, createRoleApi, updateRoleApi, deleteRoleApi, getAvailablePermissionsApi } from '../../api/roles';
import { usePermissions } from '../../hooks/usePermissions';
import { cn } from '../../utils';

const roleSchema = z.object({
  name: z.string().min(2, 'Tên vai trò phải từ 2 ký tự').max(100, 'Tên vai trò tối đa 100 ký tự'),
  description: z.string().max(255).optional(),
  permissions: z.array(z.string()),
});

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
  const queryClient = useQueryClient();
  const { hasPermission } = usePermissions();
  const canCreate = hasPermission('ROLES_CREATE');
  const canUpdate = hasPermission('ROLES_UPDATE');
  const canDelete = hasPermission('ROLES_DELETE');

  const [selectedRole, setSelectedRole] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const { data: rolesResponse, isLoading: isLoadingRoles } = useQuery({
    queryKey: ['roles'],
    queryFn: async () => {
      const res = await getRolesApi();
      return res.data;
    }
  });

  const roles = Array.isArray(rolesResponse) ? rolesResponse : rolesResponse?.results || [];

  const { data: availablePermissions = [] } = useQuery({
    queryKey: ['permissions'],
    queryFn: async () => {
      const res = await getAvailablePermissionsApi();
      return res.data;
    }
  });

  const createMutation = useMutation({
    mutationFn: createRoleApi,
    onSuccess: (res) => {
      queryClient.invalidateQueries(['roles']);
      setSelectedRole(res.data);
      setIsCreating(false);
    }
  });

  const updateMutation = useMutation({
    mutationFn: updateRoleApi,
    onSuccess: () => {
      queryClient.invalidateQueries(['roles']);
    }
  });

  const deleteMutation = useMutation({
    mutationFn: deleteRoleApi,
    onSuccess: () => {
      queryClient.invalidateQueries(['roles']);
      setSelectedRole(null);
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
    const current = form.getValues('permissions');
    if (current.includes(permId)) {
      form.setValue('permissions', current.filter(id => id !== permId), { shouldDirty: true });
    } else {
      form.setValue('permissions', [...current, permId], { shouldDirty: true });
    }
  };

  const toggleAllPermissions = () => {
    const current = form.getValues('permissions');
    if (current.length === availablePermissions.length) {
      // If all are selected, unselect all
      form.setValue('permissions', [], { shouldDirty: true });
    } else {
      // Otherwise, select all
      form.setValue('permissions', availablePermissions.map(p => p.id), { shouldDirty: true });
    }
  };

  const toggleGroupPermissions = (permsInGroup) => {
    const current = form.getValues('permissions');
    const groupPermIds = permsInGroup.map(p => p.id);
    const allSelectedInGroup = groupPermIds.every(id => current.includes(id));

    if (allSelectedInGroup) {
      // Unselect all in this group
      form.setValue('permissions', current.filter(id => !groupPermIds.includes(id)), { shouldDirty: true });
    } else {
      // Select all in this group, ensuring no duplicates
      const newPerms = new Set([...current, ...groupPermIds]);
      form.setValue('permissions', Array.from(newPerms), { shouldDirty: true });
    }
  };

  const groupedPermissions = groupPermissions(availablePermissions);
  const filteredRoles = roles.filter(r => r.name.toLowerCase().includes(searchQuery.toLowerCase()));

  return (
    <div className="flex h-[calc(100vh-64px)] bg-slate-50 overflow-hidden">
      
      {/* LEFT PANEL: ROLE LIST */}
      <div className="w-80 flex-shrink-0 border-r border-slate-200 bg-white flex flex-col z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
        <div className="p-4 border-b border-slate-100">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-800 flex items-center gap-2">
              <Shield size={20} className="text-indigo-600" />
              Vai trò & Quyền
            </h2>
            <button 
              onClick={() => { setIsCreating(true); setSelectedRole(null); }}
              disabled={!canCreate}
              className={cn(
                "p-1.5 rounded-lg transition-all",
                canCreate ? "bg-indigo-50 text-indigo-600 hover:bg-indigo-100 hover:shadow-sm" : "bg-slate-100 text-slate-300 cursor-not-allowed"
              )}
              title="Thêm vai trò mới"
            >
              <Plus size={18} />
            </button>
          </div>
          
          <div className="relative">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Tìm kiếm vai trò..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {isLoadingRoles ? (
            <div className="animate-pulse space-y-3 p-2">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-16 bg-slate-100 rounded-xl"></div>
              ))}
            </div>
          ) : filteredRoles.length === 0 ? (
            <div className="text-center py-10 text-slate-400 text-sm">Không tìm thấy vai trò nào</div>
          ) : (
            filteredRoles.map(role => {
              const isActive = selectedRole?.id === role.id && !isCreating;
              // Mock logic for progress bar: assuming 15 total permissions for now
              const permCount = role.permissions?.length || 0;
              const percent = Math.min(100, Math.round((permCount / availablePermissions.length) * 100)) || 0;
              
              return (
                <div 
                  key={role.id}
                  onClick={() => { setSelectedRole(role); setIsCreating(false); }}
                  className={cn(
                    "p-3 rounded-xl cursor-pointer transition-all border duration-200 group relative overflow-hidden",
                    isActive 
                      ? "bg-indigo-600 border-indigo-600 text-white shadow-md shadow-indigo-200" 
                      : "bg-white border-slate-100 hover:border-indigo-200 hover:bg-indigo-50/50 hover:shadow-sm text-slate-700"
                  )}
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className={cn("font-bold text-sm", isActive ? "text-white" : "text-slate-800")}>
                      {role.name}
                    </h3>
                    <div className={cn("flex items-center gap-1 text-[10px] font-semibold px-2 py-0.5 rounded-full", isActive ? "bg-white/20 text-indigo-50" : "bg-slate-100 text-slate-500")}>
                      <Users size={12} />
                      <span className="opacity-80">Users</span>
                    </div>
                  </div>
                  <p className={cn("text-xs line-clamp-1 mb-3", isActive ? "text-indigo-100" : "text-slate-500")}>
                    {role.description || 'Không có mô tả'}
                  </p>
                  
                  {/* Progress Bar */}
                  <div className="flex items-center gap-2">
                    <div className="flex-1 h-1.5 rounded-full overflow-hidden bg-black/10">
                      <div 
                        className={cn("h-full rounded-full transition-all duration-500", isActive ? "bg-white" : "bg-indigo-500")} 
                        style={{ width: `${percent}%` }}
                      ></div>
                    </div>
                    <span className={cn("text-[10px] font-bold", isActive ? "text-indigo-100" : "text-indigo-600")}>
                      {permCount}/{availablePermissions.length}
                    </span>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* RIGHT PANEL: ROLE DETAIL / MATRIX */}
      <div className="flex-1 flex flex-col relative overflow-hidden bg-slate-50/50">
        {(!selectedRole && !isCreating) ? (
          <div className="flex-1 flex flex-col items-center justify-center text-slate-400 p-8 text-center">
            <div className="w-24 h-24 rounded-full bg-slate-100 flex items-center justify-center mb-6 border-8 border-white shadow-sm">
              <ShieldCheck size={40} className="text-slate-300" />
            </div>
            <h3 className="text-xl font-bold text-slate-700 mb-2">Quản trị Phân quyền</h3>
            <p className="max-w-md text-sm">
              Chọn một vai trò từ danh sách bên trái để xem và chỉnh sửa Ma trận Quyền hạn, 
              hoặc tạo một vai trò mới để thiết lập.
            </p>
          </div>
        ) : (
          <form onSubmit={form.handleSubmit(onSubmit)} className="flex-1 flex flex-col h-full animate-in fade-in duration-300">
            {/* Sticky Header */}
            <div className="px-8 py-5 bg-white border-b border-slate-200 flex items-center justify-between sticky top-0 z-20 shadow-sm">
              <div>
                <h2 className="text-xl font-extrabold text-slate-800 tracking-tight">
                  {isCreating ? 'Tạo Vai trò mới' : 'Chi tiết Vai trò'}
                </h2>
                <p className="text-sm text-slate-500 font-medium mt-1">
                  Thiết lập thông tin và cấu hình Ma trận quyền truy cập
                </p>
              </div>
              <div className="flex items-center gap-3">
                {!isCreating && (
                  <button 
                    type="button"
                    disabled={!canDelete}
                    onClick={() => {
                      if (window.confirm('Bạn có chắc chắn muốn xóa vai trò này?')) {
                        deleteMutation.mutate(selectedRole.id);
                      }
                    }}
                    className={cn(
                      "flex items-center gap-2 px-4 py-2 text-sm font-semibold rounded-xl transition-colors",
                      canDelete ? "text-red-600 bg-red-50 hover:bg-red-100" : "bg-slate-100 text-slate-400 cursor-not-allowed"
                    )}
                  >
                    <Trash2 size={16} />
                    Xóa
                  </button>
                )}
                <button 
                  type="submit"
                  disabled={(isCreating ? !canCreate : !canUpdate) || createMutation.isPending || updateMutation.isPending}
                  className="flex items-center gap-2 px-6 py-2 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-700 hover:shadow-lg hover:shadow-indigo-600/20 rounded-xl transition-all disabled:opacity-50"
                >
                  <CheckCircle2 size={18} />
                  {isCreating ? 'Tạo mới' : 'Lưu thay đổi'}
                </button>
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-8">
              <div className="max-w-4xl mx-auto space-y-8">
                
                {/* Basic Info Section */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                  <h3 className="text-base font-bold text-slate-800 mb-5 flex items-center gap-2">
                    <div className="w-1.5 h-4 bg-indigo-600 rounded-full"></div>
                    Thông tin cơ bản
                  </h3>
                  <div className="grid gap-5">
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Tên vai trò <span className="text-red-500">*</span></label>
                      <input 
                        {...form.register('name')}
                        className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all font-medium"
                        placeholder="VD: Quản trị viên, Trợ giảng..."
                      />
                      {form.formState.errors.name && (
                        <p className="text-xs text-red-500 mt-1.5 font-medium">{form.formState.errors.name.message}</p>
                      )}
                    </div>
                    <div>
                      <label className="block text-sm font-semibold text-slate-700 mb-1.5">Mô tả chi tiết</label>
                      <textarea 
                        {...form.register('description')}
                        rows={2}
                        className="w-full px-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all resize-none"
                        placeholder="Mô tả ngắn gọn về chức năng của vai trò này..."
                      />
                    </div>
                  </div>
                </div>

                {/* Permission Matrix Section */}
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-base font-bold text-slate-800 flex items-center gap-2">
                      <div className="w-1.5 h-4 bg-purple-500 rounded-full"></div>
                      Ma trận Quyền hạn (Permission Matrix)
                    </h3>
                    <div className="flex items-center gap-3">
                      <div className="text-xs font-semibold px-3 py-1 bg-slate-100 text-slate-600 rounded-lg">
                        Đã chọn: <span className="text-indigo-600">{form.watch('permissions').length}</span> / {availablePermissions.length}
                      </div>
                      <button
                        type="button"
                        onClick={toggleAllPermissions}
                        className="text-xs font-bold px-3 py-1.5 rounded-lg border border-indigo-200 text-indigo-700 bg-indigo-50 hover:bg-indigo-600 hover:text-white transition-colors"
                      >
                        {form.watch('permissions').length === availablePermissions.length ? 'Bỏ chọn tất cả' : 'Chọn tất cả'}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-6">
                    {Object.entries(groupedPermissions).map(([groupName, perms]) => {
                      if (perms.length === 0) return null;
                      
                      const groupPermIds = perms.map(p => p.id);
                      const allSelectedInGroup = groupPermIds.every(id => form.watch('permissions').includes(id));

                      return (
                        <div key={groupName} className="border border-slate-100 rounded-xl overflow-hidden">
                          <div className="px-5 py-3 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
                            <h4 className="text-sm font-bold text-slate-700">{groupName}</h4>
                            <button
                              type="button"
                              onClick={() => toggleGroupPermissions(perms)}
                              className="text-[11px] font-bold px-2.5 py-1 rounded-md border border-slate-200 text-slate-600 bg-white hover:bg-slate-100 hover:text-slate-900 transition-colors"
                            >
                              {allSelectedInGroup ? 'Bỏ chọn' : 'Chọn tất cả'}
                            </button>
                          </div>
                          <div className="p-2 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                            {perms.map(perm => {
                              const isChecked = form.watch('permissions').includes(perm.id);
                              
                              // Determine color based on action type
                              let colorClass = "text-indigo-600 bg-indigo-50";
                              let toggleClass = "peer-checked:bg-indigo-600";
                              if (perm.id.includes('DELETE')) { colorClass = "text-red-600 bg-red-50"; toggleClass = "peer-checked:bg-red-500"; }
                              else if (perm.id.includes('CREATE') || perm.id.includes('UPDATE')) { colorClass = "text-emerald-600 bg-emerald-50"; toggleClass = "peer-checked:bg-emerald-500"; }
                              else if (perm.id.includes('EXPORT')) { colorClass = "text-orange-600 bg-orange-50"; toggleClass = "peer-checked:bg-orange-500"; }

                              return (
                                <div 
                                  key={perm.id}
                                  onClick={() => togglePermission(perm.id)}
                                  className={cn(
                                    "flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-all hover:shadow-sm",
                                    isChecked ? "border-slate-300 bg-white shadow-sm" : "border-transparent hover:border-slate-200 hover:bg-slate-50"
                                  )}
                                >
                                  <div className="relative inline-flex items-center cursor-pointer mt-0.5 shrink-0">
                                    <input type="checkbox" className="sr-only peer" checked={isChecked} readOnly />
                                    <div className={cn("w-9 h-5 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all", toggleClass)}></div>
                                  </div>
                                  <div>
                                    <p className={cn("text-xs font-bold leading-tight mb-1 transition-colors", isChecked ? "text-slate-900" : "text-slate-600")}>
                                      {perm.name}
                                    </p>
                                    <span className={cn("text-[9px] font-bold px-1.5 py-0.5 rounded uppercase tracking-wider", colorClass)}>
                                      {perm.id.split('_')[1]}
                                    </span>
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

              </div>
            </div>
          </form>
        )}
      </div>

    </div>
  );
}
