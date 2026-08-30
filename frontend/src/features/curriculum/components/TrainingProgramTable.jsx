import { Edit2, Trash2, Library, Settings } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StatusBadge from '@/components/ui/StatusBadge';
import AppPagination from '@/components/ui/AppPagination';
import { useNavigate } from 'react-router-dom';

export default function TrainingProgramTable({
  programs,
  isLoading,
  canUpdate,
  canDelete,
  onEdit,
  setDeleteConfig,
  page,
  setPage,
  count,
  majors = [],
  specializations = [],
  cohorts = []
}) {
  const navigate = useNavigate();

  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-x-auto flex flex-col">
      <Table className="text-sm min-w-[800px]">
        <TableHeader className="bg-slate-50">
          <TableRow>
            <TableHead className="font-semibold px-3 py-3 w-[15%]">Mã CTĐT</TableHead>
            <TableHead className="font-semibold px-3 py-3 w-[25%]">Tên chương trình</TableHead>
            <TableHead className="font-semibold px-3 py-3">Ngành học</TableHead>
            <TableHead className="font-semibold px-3 py-3">Chuyên ngành</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Khóa</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Tổng TC</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Trạng thái</TableHead>
            <TableHead className="font-semibold text-right px-3 py-3 w-[15%]">Hành động</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            Array.from({ length: 5 }).map((_, idx) => (
              <TableRow key={idx}>
                <TableCell className="px-3 py-3"><Skeleton className="w-24 h-4" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-48 h-4" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-32 h-4" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-32 h-4" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-12 h-4 mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-8 h-4 mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-20 h-5 rounded-full mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-right"><Skeleton className="w-24 h-8 rounded ml-auto" /></TableCell>
              </TableRow>
            ))
          ) : programs.length === 0 ? (
            <TableRow>
              <TableCell colSpan={8} className="px-3 py-12 text-center text-slate-500">
                <div className="flex flex-col items-center justify-center">
                  <Library size={32} className="text-slate-300 mb-3" />
                  <p>Không tìm thấy chương trình đào tạo nào</p>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            programs.map((program) => (
              <TableRow key={program.id} className="hover:bg-slate-50/50 transition-colors">
                <TableCell className="px-3 py-3 font-medium text-slate-700">
                  {program.code}
                </TableCell>
                <TableCell className="px-3 py-3">
                  <div className="font-semibold text-slate-900">{program.name}</div>
                </TableCell>
                <TableCell className="px-3 py-3">
                  <span className="text-sm text-slate-700">
                    {majors.find(m => m.value === program.major)?.label || program.major?.name || 'N/A'}
                  </span>
                </TableCell>
                <TableCell className="px-3 py-3">
                  <span className="text-sm text-slate-700">
                    {program.specialization 
                      ? specializations.find(s => s.value === program.specialization)?.label || program.specialization?.name || '-'
                      : '-'}
                  </span>
                </TableCell>
                <TableCell className="px-3 py-3 text-center font-medium">
                  {cohorts.find(c => c.value === program.cohort)?.label || program.cohort?.code || 'N/A'}
                </TableCell>
                <TableCell className="px-3 py-3 text-center font-semibold text-slate-900">
                  {program.total_credits}
                </TableCell>
                <TableCell className="px-3 py-3 text-center">
                  <StatusBadge status={program.is_active ? 'ACTIVE' : 'INACTIVE'} />
                </TableCell>
                <TableCell className="px-3 py-3 text-right">
                  <div className="flex justify-end gap-1">
                    <Button
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-slate-100"
                      onClick={() => navigate(`/curriculum/training-programs/${program.id}`)} title="Cấu hình Khung chương trình"
                    >
                      <Settings className="h-4 w-4 text-slate-600" />
                    </Button>
                    <Button
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                      disabled={!canUpdate} onClick={() => onEdit(program)} title="Sửa thông tin chung"
                    >
                      <Edit2 className="h-4 w-4 text-indigo-600" />
                    </Button>
                    <Button
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                      disabled={!canDelete} onClick={() => setDeleteConfig({ isOpen: true, id: program.id })} title="Xóa CTĐT"
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
