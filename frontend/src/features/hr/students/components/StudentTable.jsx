import { Edit2, Eye, Printer, Trash2, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StatusBadge from '../../../../components/ui/StatusBadge';
import AppPagination from '@/components/ui/AppPagination';

export default function StudentTable({
  students,
  isLoading,
  canUpdate,
  canDelete,
  handlePrintIdCard,
  setDeleteConfig,
  page,
  setPage,
  count
}) {
  const navigate = useNavigate();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden flex flex-col">
      <Table>
        <TableHeader className="bg-slate-50">
          <TableRow>
            <TableHead className="font-semibold px-6 py-4">Sinh viên</TableHead>
            <TableHead className="font-semibold px-6 py-4">Ngành / Lớp</TableHead>
            <TableHead className="font-semibold px-6 py-4">Trạng thái</TableHead>
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
          ) : students.length === 0 ? (
            <TableRow>
              <TableCell colSpan={4} className="px-6 py-12 text-center text-slate-500">
                <div className="flex flex-col items-center justify-center">
                  <Users size={32} className="text-slate-300 mb-3" />
                  <p>Không tìm thấy sinh viên nào phù hợp</p>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            students.map((student) => (
              <TableRow key={student.id} className="hover:bg-slate-50/50 transition-colors">
                <TableCell className="px-6 py-4">
                  <div className="flex items-center gap-3">
                    <img 
                      src={`https://ui-avatars.com/api/?name=${encodeURIComponent(student.user?.full_name || 'SV')}&background=e0e7ff&color=4f46e5`} 
                      alt={student.user?.full_name} 
                      className="w-10 h-10 rounded-full border border-slate-200 object-cover"
                    />
                    <div>
                      <div className="font-semibold text-slate-900 cursor-pointer hover:text-blue-600 transition-colors" onClick={() => navigate(`/hr/students/${student.id}`)}>
                        {student.user?.full_name || 'N/A'}
                      </div>
                      <div className="text-xs text-slate-500">{student.student_code} • {student.user?.email || 'N/A'}</div>
                    </div>
                  </div>
                </TableCell>
                <TableCell className="px-6 py-4">
                  <div className="text-sm text-slate-900">{student.major_detail?.name || 'Chưa xếp ngành'}</div>
                  <div className="text-xs text-slate-500">{student.administrative_class_code || 'Chưa xếp lớp'}</div>
                </TableCell>
                <TableCell className="px-6 py-4">
                  <StatusBadge status={student.status} />
                </TableCell>
                <TableCell className="px-6 py-4 text-right">
                  <div className="flex justify-end gap-1">
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-blue-50"
                      onClick={() => navigate(`/hr/students/${student.id}`)} title="Xem chi tiết"
                    >
                      <Eye className="h-4 w-4 text-blue-600" />
                    </Button>
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-slate-100"
                      onClick={() => handlePrintIdCard(student.id)} title="In thẻ Sinh viên"
                    >
                      <Printer className="h-4 w-4 text-slate-600" />
                    </Button>
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                      disabled={!canUpdate} onClick={() => navigate(`/hr/students/${student.id}/edit`)} title="Sửa thông tin"
                    >
                      <Edit2 className="h-4 w-4 text-indigo-600" />
                    </Button>
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                      disabled={!canDelete} onClick={() => setDeleteConfig({ isOpen: true, id: student.id })} title="Xóa sinh viên"
                    >
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
      
      {count > 0 && (
        <div className="px-6 py-4 border-t border-slate-200">
          <AppPagination page={page} setPage={setPage} count={count} pageSize={10} />
        </div>
      )}
    </div>
  );
}
