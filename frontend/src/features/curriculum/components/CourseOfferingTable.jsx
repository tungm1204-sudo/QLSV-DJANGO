import { Edit, Trash2, CalendarDays } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import AppPagination from '@/components/ui/AppPagination';

const statusMap = {
  'PLANNED': { label: 'Theo kế hoạch', color: 'bg-slate-100 text-slate-700' },
  'OPEN': { label: 'Mở đăng ký', color: 'bg-green-100 text-green-700' },
  'CLOSED': { label: 'Đóng đăng ký', color: 'bg-yellow-100 text-yellow-700' },
  'CANCELLED': { label: 'Đã hủy', color: 'bg-red-100 text-red-700' },
};

export default function CourseOfferingTable({ 
  offerings, 
  count, 
  page, 
  setPage, 
  isLoading,
  canUpdate,
  canDelete,
  onEdit,
  onConfigSchedule,
  setDeleteConfig
}) {
  if (isLoading) return <div className="text-center py-8">Đang tải...</div>;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Mã môn</TableHead>
              <TableHead className="w-[250px]">Tên môn học</TableHead>
              <TableHead>Tín chỉ</TableHead>
              <TableHead>Giảng viên</TableHead>
              <TableHead>Sức chứa</TableHead>
              <TableHead>Trạng thái</TableHead>
              <TableHead className="text-right">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {offerings.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="text-center py-8 text-slate-500">
                  Chưa có lớp học phần nào trong kế hoạch này
                </TableCell>
              </TableRow>
            ) : (
              offerings.map((offering) => (
                <TableRow key={offering.id}>
                  <TableCell className="font-medium">{offering.course?.code}</TableCell>
                  <TableCell>{offering.course?.name}</TableCell>
                  <TableCell>{offering.course?.credits}</TableCell>
                  <TableCell>
                    {offering.lecturer 
                      ? `${offering.lecturer.user?.last_name} ${offering.lecturer.user?.first_name}`
                      : <span className="text-slate-400 italic">Chưa phân công</span>}
                  </TableCell>
                  <TableCell>
                    {offering.current_enrollment} / {offering.max_capacity}
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className={statusMap[offering.status]?.color}>
                      {statusMap[offering.status]?.label || offering.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => onConfigSchedule(offering)}
                        title="Xếp lịch"
                      >
                        <CalendarDays className="w-4 h-4 text-indigo-500" />
                      </Button>
                      {canUpdate && (
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => onEdit(offering)}
                          title="Sửa"
                        >
                          <Edit className="w-4 h-4 text-blue-500" />
                        </Button>
                      )}
                      {canDelete && (
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => setDeleteConfig({ isOpen: true, id: offering.id })}
                          title="Xóa"
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
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
        <AppPagination 
          page={page} 
          count={count} 
          setPage={setPage} 
        />
      )}
    </div>
  );
}
