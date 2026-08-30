import { ShieldAlert, ShieldCheck, Edit2, KeyRound, Trash2, Users, MoreVertical } from 'lucide-react';
import { cn } from '../../../utils';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import AppPagination from '@/components/ui/AppPagination';

export default function UserTable({
  users,
  isLoadingUsers,
  currentUser,
  canUpdate,
  canDelete,
  handleOpenModal,
  lockUnlockMutation,
  setResetPasswordUser,
  setResetPasswordValue,
  setDeleteUserConfig,
  page,
  setPage,
  count
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
      <div className="overflow-x-auto flex-1">
        <Table>
          <TableHeader className="bg-slate-50">
            <TableRow>
              <TableHead className="font-semibold px-6 py-4">Người dùng</TableHead>
              <TableHead className="font-semibold px-6 py-4">Vai trò</TableHead>
              <TableHead className="font-semibold px-6 py-4">Trạng thái</TableHead>
              <TableHead className="font-semibold text-right px-6 py-4">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoadingUsers ? (
              // SKELETON LOADING
              Array.from({ length: 5 }).map((_, idx) => (
                <TableRow key={idx}>
                  <TableCell className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <Skeleton className="w-10 h-10 rounded-full" />
                      <div className="space-y-2">
                        <Skeleton className="w-32 h-4" />
                        <Skeleton className="w-24 h-3" />
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="px-6 py-4"><Skeleton className="w-20 h-5 rounded-full" /></TableCell>
                  <TableCell className="px-6 py-4"><Skeleton className="w-16 h-5 rounded-full" /></TableCell>
                  <TableCell className="px-6 py-4 text-right"><Skeleton className="w-8 h-8 rounded ml-auto" /></TableCell>
                </TableRow>
              ))
            ) : users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="px-6 py-12 text-center text-slate-500">
                  <div className="flex flex-col items-center justify-center">
                    <Users size={32} className="text-slate-300 mb-3" />
                    <p>Không tìm thấy người dùng nào phù hợp</p>
                  </div>
                </TableCell>
              </TableRow>
            ) : (
              users.map((user) => {
                const isTemporarilyLocked = user.locked_until && new Date(user.locked_until) > new Date();
                const isLocked = !user.is_active || user.status === 'LOCKED' || isTemporarilyLocked;
                const isCurrentUser = currentUser?.id === user.id;
                
                return (
                  <TableRow key={user.id} className="hover:bg-slate-50/50 transition-colors">
                    <TableCell className="px-6 py-4">
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
                    </TableCell>
                    <TableCell className="px-6 py-4">
                      {user.role ? (
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-100">
                          {user.role.name}
                        </span>
                      ) : (
                        <span className="text-xs text-slate-400 italic">Chưa phân vai trò</span>
                      )}
                    </TableCell>
                    <TableCell className="px-6 py-4">
                      <span className={cn(
                        "px-2.5 py-1 text-xs font-medium rounded-full flex items-center gap-1 w-max",
                        isLocked ? "bg-red-50 text-red-700 border border-red-100" : "bg-emerald-50 text-emerald-700 border border-emerald-100"
                      )}>
                        {isLocked ? <ShieldAlert size={12} /> : <ShieldCheck size={12} />}
                        {isTemporarilyLocked ? 'Bị Khóa (Tạm thời)' : isLocked ? 'Bị Khóa' : 'Hoạt động'}
                      </span>
                    </TableCell>
                    <TableCell className="px-6 py-4 text-right">
                      <div className="flex justify-end gap-1">
                        <Button 
                          variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                          disabled={!canUpdate} onClick={() => handleOpenModal(user)} title="Sửa thông tin"
                        >
                          <Edit2 className="h-4 w-4 text-indigo-600" />
                        </Button>
                        
                        <Button 
                          variant="ghost" size="icon" className="h-8 w-8 hover:bg-orange-50"
                          disabled={!canUpdate} onClick={() => { setResetPasswordUser(user); setResetPasswordValue(''); }} title="Đổi mật khẩu"
                        >
                          <KeyRound className="h-4 w-4 text-orange-600" />
                        </Button>
                        
                        <Button 
                          variant="ghost" size="icon" className={cn("h-8 w-8", isLocked ? "hover:bg-emerald-50" : "hover:bg-red-50")}
                          disabled={!canUpdate || isCurrentUser} onClick={() => lockUnlockMutation.mutate({ id: user.id, isLocked })} title={isLocked ? "Mở khóa tài khoản" : "Khóa tài khoản"}
                        >
                          {isLocked ? <ShieldCheck className="h-4 w-4 text-emerald-600" /> : <ShieldAlert className="h-4 w-4 text-red-600" />}
                        </Button>
  
                        <Button 
                          variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                          disabled={!canDelete || isCurrentUser} onClick={() => setDeleteUserConfig({ isOpen: true, userId: user.id })} title="Xóa người dùng"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                );
              })
            )}
          </TableBody>
        </Table>
      </div>

      {count > 0 && (
        <div className="px-6 py-4 border-t border-slate-200">
          <AppPagination page={page} setPage={setPage} count={count} pageSize={10} />
        </div>
      )}
    </div>
  );
}
