import { Edit2, Trash2, BookOpen } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StatusBadge from '@/components/ui/StatusBadge';
import AppPagination from '@/components/ui/AppPagination';

export default function CourseTable({
  courses,
  isLoading,
  canUpdate,
  canDelete,
  onEdit,
  setDeleteConfig,
  page,
  setPage,
  count,
  departments = [],
  courseTypes = []
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-x-auto flex flex-col">
      <Table className="text-sm">
        <TableHeader className="bg-slate-50">
          <TableRow>
            <TableHead className="font-semibold px-3 py-3 w-[8%]">Mã môn</TableHead>
            <TableHead className="font-semibold px-3 py-3 w-[20%]">Tên môn học</TableHead>
            <TableHead className="font-semibold px-3 py-3">Loại học phần</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Tổng TC</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Lý thuyết</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Thực hành</TableHead>
            <TableHead className="font-semibold px-3 py-3">Bộ môn quản lý</TableHead>
            <TableHead className="font-semibold px-3 py-3 text-center">Trạng thái</TableHead>
            <TableHead className="font-semibold text-right px-3 py-3">Hành động</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            Array.from({ length: 5 }).map((_, idx) => (
              <TableRow key={idx}>
                <TableCell className="px-3 py-3"><Skeleton className="w-20 h-4" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-40 h-4" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-20 h-4" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-6 h-4 mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-6 h-4 mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-6 h-4 mx-auto" /></TableCell>
                <TableCell className="px-3 py-3"><Skeleton className="w-32 h-4" /></TableCell>
                <TableCell className="px-3 py-3 text-center"><Skeleton className="w-20 h-5 rounded-full mx-auto" /></TableCell>
                <TableCell className="px-3 py-3 text-right"><Skeleton className="w-16 h-8 rounded ml-auto" /></TableCell>
              </TableRow>
            ))
          ) : courses.length === 0 ? (
            <TableRow>
              <TableCell colSpan={9} className="px-3 py-12 text-center text-slate-500">
                <div className="flex flex-col items-center justify-center">
                  <BookOpen size={32} className="text-slate-300 mb-3" />
                  <p>Không tìm thấy môn học nào</p>
                </div>
              </TableCell>
            </TableRow>
          ) : (
            courses.map((course) => (
              <TableRow key={course.id} className="hover:bg-slate-50/50 transition-colors">
                <TableCell className="px-3 py-3 font-medium text-slate-700">
                  {course.code}
                </TableCell>
                <TableCell className="px-3 py-3">
                  <div className="font-semibold text-slate-900">{course.name}</div>
                </TableCell>
                <TableCell className="px-3 py-3">
                  <span className="text-sm text-slate-700">
                    {course.course_type 
                      ? courseTypes.find(t => t.value === course.course_type)?.label || course.course_type.name || ''
                      : '-'}
                  </span>
                </TableCell>
                <TableCell className="px-3 py-3 text-center font-semibold text-slate-900">{course.credits}</TableCell>
                <TableCell className="px-3 py-3 text-center text-slate-600">{course.theory_credits}</TableCell>
                <TableCell className="px-3 py-3 text-center text-slate-600">{course.practical_credits}</TableCell>
                <TableCell className="px-3 py-3">
                  <span className="text-sm text-slate-700">
                    {departments.find(d => d.value === course.department)?.label || course.department?.name || 'N/A'}
                  </span>
                </TableCell>
                <TableCell className="px-3 py-3 text-center">
                  <StatusBadge status={course.is_active ? 'ACTIVE' : 'INACTIVE'} />
                </TableCell>
                <TableCell className="px-3 py-3 text-right">
                  <div className="flex justify-end gap-1">
                    <Button
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                      disabled={!canUpdate} onClick={() => onEdit(course)} title="Sửa môn học"
                    >
                      <Edit2 className="h-4 w-4 text-indigo-600" />
                    </Button>
                    <Button
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                      disabled={!canDelete} onClick={() => setDeleteConfig({ isOpen: true, id: course.id })} title="Xóa môn học"
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
