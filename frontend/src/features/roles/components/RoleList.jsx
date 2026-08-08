import { Search, Plus, Shield, ShieldCheck, Users } from 'lucide-react';
import { cn } from '../../../utils';

export default function RoleList({
  filteredRoles,
  isLoadingRoles,
  searchQuery,
  setSearchQuery,
  selectedRole,
  setSelectedRole,
  isCreating,
  setIsCreating,
  canCreate,
  SYSTEM_ROLES,
  availablePermissions
}) {
  return (
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
            const permCount = role.permissions?.length || 0;
            const percent = Math.min(100, Math.round((permCount / (availablePermissions.length || 1)) * 100)) || 0;
            
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
                    {SYSTEM_ROLES.includes(role.name) && (
                      <ShieldCheck size={14} className={cn("inline ml-1", isActive ? "text-indigo-200" : "text-indigo-500")} title="Vai trò Hệ thống" />
                    )}
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
  );
}
