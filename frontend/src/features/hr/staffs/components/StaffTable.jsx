import { Edit2, Eye, Trash2, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StatusBadge from '../../../../components/ui/StatusBadge';
import AppPagination from '@/components/ui/AppPagination';

export default function StaffTable({
  staffs,
  isLoading,
  canUpdate,
  canDelete,
  setDeleteConfig,
  page,
  setPage,
  count
}) {
  const navigate = useNavigate();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
      <div className="overflow-x-auto flex-1">
        <Table>
          <TableHeader className="bg-slate-50">
            <TableRow>
              <TableHead className="font-semibold px-6 py-4">Cán bộ / Nhân viên</TableHead>
              <TableHead className="font-semibold px-6 py-4">Phòng ban</TableHead>
              <TableHead className="font-semibold px-6 py-4">Chức vụ & Trạng thái</TableHead>
              <TableHead className="font-semibold text-right px-6 py-4">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
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
                  <TableCell className="px-6 py-4">
                    <div className="space-y-2">
                      <Skeleton className="w-32 h-4" />
                      <Skeleton className="w-20 h-3" />
                    </div>
                  </TableCell>
                  <TableCell className="px-6 py-4"><Skeleton className="w-20 h-5 rounded-full" /></TableCell>
                  <TableCell className="px-6 py-4 text-right"><Skeleton className="w-8 h-8 rounded ml-auto" /></TableCell>
                </TableRow>
              ))
            ) : staffs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="px-6 py-12 text-center text-slate-500">
                  <div className="flex flex-col items-center justify-center">
                    <Users size={32} className="text-slate-300 mb-3" />
                    <p>Không tìm thấy nhân viên nào phù hợp</p>
                  </div>
                </TableCell>
              </TableRow>
            ) : (
              staffs.map((staff) => (
                <TableRow key={staff.id} className="hover:bg-slate-50/50 transition-colors">
                  <TableCell className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <img 
                        src={`https://ui-avatars.com/api/?name=${encodeURIComponent(staff.user?.full_name || 'NV')}&background=e0e7ff&color=4f46e5`} 
                        alt={staff.user?.full_name} 
                        className="w-10 h-10 rounded-full border border-slate-200 object-cover"
                      />
                      <div>
                        <div className="font-semibold text-slate-900 cursor-pointer hover:text-blue-600 transition-colors" onClick={() => navigate(`/hr/staffs/${staff.id}`)}>
                          {staff.user?.full_name || 'N/A'}
                        </div>
                        <div className="text-xs text-slate-500">{staff.staff_code} • {staff.user?.email || 'N/A'}</div>
                      </div>
                    </div>
                  </TableCell>
                  <TableCell className="px-6 py-4">
                    <div className="text-sm text-slate-900">{staff.department_detail?.name || 'Chưa phân phòng ban'}</div>
                    <div className="text-xs text-slate-500">
                      {staff.degree_detail?.name || 'N/A'}
                    </div>
                  </TableCell>
                  <TableCell className="px-6 py-4">
                    <div className="flex flex-col gap-2 items-start">
                      <div className="text-sm text-slate-700 font-medium">
                        {staff.position_detail?.name || 'N/A'}
                      </div>
                      <StatusBadge status={staff.status} />
                    </div>
                  </TableCell>
                  <TableCell className="px-6 py-4 text-right">
                    <div className="flex justify-end gap-1">
                      <Button 
                        variant="ghost" size="icon" className="h-8 w-8 hover:bg-blue-50"
                        onClick={() => navigate(`/hr/staffs/${staff.id}`)} title="Xem chi tiết"
                      >
                        <Eye className="h-4 w-4 text-blue-600" />
                      </Button>
                      {canUpdate && (
                        <Button 
                          variant="ghost" size="icon" className="h-8 w-8 hover:bg-emerald-50"
                          onClick={() => navigate(`/hr/staffs/${staff.id}/edit`)} title="Cập nhật"
                        >
                          <Edit2 className="h-4 w-4 text-emerald-600" />
                        </Button>
                      )}
                      {canDelete && (
                        <Button 
                          variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                          onClick={() => setDeleteConfig({ isOpen: true, id: staff.id })} title="Xóa"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      )}
                    </div>
                  </TableCell>
                </TableRow>
              ))
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
