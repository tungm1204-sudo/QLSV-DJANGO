import { ShieldCheck, Trash2, CheckCircle2 } from 'lucide-react';
import { cn } from '../../../utils';

export default function RoleForm({
  form,
  onSubmit,
  selectedRole,
  isCreating,
  isSystemRole,
  canCreate,
  canUpdate,
  canDelete,
  setDeleteRoleConfig,
  createMutation,
  updateMutation,
  availablePermissions,
  groupedPermissions,
  toggleAllPermissions,
  toggleGroupPermissions,
  togglePermission
}) {
  if (!selectedRole && !isCreating) {
    return (
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
    );
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)} className="flex-1 flex flex-col h-full animate-in fade-in duration-300">
      {/* Sticky Header */}
      <div className="px-8 py-5 bg-white border-b border-slate-200 flex items-center justify-between sticky top-0 z-20 shadow-sm">
        <div>
          <h2 className="text-xl font-extrabold text-slate-800 tracking-tight flex items-center gap-2">
            {isCreating ? 'Tạo Vai trò mới' : 'Chi tiết Vai trò'}
            {isSystemRole && (
              <span className="text-[10px] font-bold px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded-md border border-indigo-200 flex items-center gap-1">
                <ShieldCheck size={12} />
                Mặc định hệ thống
              </span>
            )}
          </h2>
          <p className="text-sm text-slate-500 font-medium mt-1">
            {isSystemRole 
              ? 'Đây là vai trò mặc định của hệ thống. Bạn chỉ có thể xem, không thể chỉnh sửa.' 
              : 'Thiết lập thông tin và cấu hình Ma trận quyền truy cập'}
          </p>
        </div>
        <div className="flex items-center gap-3">
          {!isCreating && (
            <button 
              type="button"
              disabled={!canDelete || isSystemRole}
              onClick={() => setDeleteRoleConfig({ isOpen: true, roleId: selectedRole.id })}
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
            disabled={(isCreating ? !canCreate : (!canUpdate || isSystemRole)) || createMutation.isPending || updateMutation.isPending}
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
                  disabled={isSystemRole}
                  className={cn(
                    "w-full px-4 py-2.5 border rounded-xl text-sm transition-all font-medium",
                    isSystemRole 
                      ? "bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed" 
                      : "bg-slate-50 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                  )}
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
                  disabled={isSystemRole}
                  className={cn(
                    "w-full px-4 py-2.5 border rounded-xl text-sm transition-all resize-none",
                    isSystemRole
                      ? "bg-slate-100 border-slate-200 text-slate-500 cursor-not-allowed"
                      : "bg-slate-50 border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
                  )}
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
                  Đã chọn: <span className="text-indigo-600">{form.watch('permissions').includes('*') ? availablePermissions.length : form.watch('permissions').length}</span> / {availablePermissions.length}
                </div>
                <button
                  type="button"
                  disabled={isSystemRole}
                  onClick={toggleAllPermissions}
                  className="text-xs font-bold px-3 py-1.5 rounded-lg border border-indigo-200 text-indigo-700 bg-indigo-50 hover:bg-indigo-600 hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {(form.watch('permissions').includes('*') || form.watch('permissions').length === availablePermissions.length) ? 'Bỏ chọn tất cả' : 'Chọn tất cả'}
                </button>
              </div>
            </div>

            <div className="space-y-6">
              {Object.entries(groupedPermissions).map(([groupName, perms]) => {
                if (perms.length === 0) return null;
                
                const groupPermIds = perms.map(p => p.id);
                const allSelectedInGroup = form.watch('permissions').includes('*') || groupPermIds.every(id => form.watch('permissions').includes(id));

                return (
                  <div key={groupName} className="border border-slate-100 rounded-xl overflow-hidden">
                    <div className="px-5 py-3 bg-slate-50 border-b border-slate-100 flex items-center justify-between">
                      <h4 className="text-sm font-bold text-slate-700">{groupName}</h4>
                      <button
                        type="button"
                        disabled={isSystemRole}
                        onClick={() => toggleGroupPermissions(perms)}
                        className="text-[11px] font-bold px-2.5 py-1 rounded-md border border-slate-200 text-slate-600 bg-white hover:bg-slate-100 hover:text-slate-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {allSelectedInGroup ? 'Bỏ chọn' : 'Chọn tất cả'}
                      </button>
                    </div>
                    <div className="p-2 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                      {perms.map(perm => {
                        const isChecked = form.watch('permissions').includes('*') || form.watch('permissions').includes(perm.id);
                        
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
                              "flex items-start gap-3 p-3 rounded-lg border transition-all",
                              isChecked ? "border-slate-300 bg-white shadow-sm" : "border-transparent",
                              !isSystemRole && !isChecked && "hover:border-slate-200 hover:bg-slate-50",
                              !isSystemRole && "cursor-pointer",
                              isSystemRole && "opacity-80"
                            )}
                          >
                            <div className={cn("relative inline-flex items-center mt-0.5 shrink-0", !isSystemRole && "cursor-pointer")}>
                              <input type="checkbox" className="sr-only peer" checked={isChecked} readOnly disabled={isSystemRole} />
                              <div className={cn("w-9 h-5 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all", toggleClass, isSystemRole && "opacity-70")}></div>
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
  );
}
