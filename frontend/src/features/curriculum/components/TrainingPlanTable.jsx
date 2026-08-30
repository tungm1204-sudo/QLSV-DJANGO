import { Edit, Trash2, Eye } from 'lucide-react';
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
import { useNavigate } from 'react-router-dom';

const statusMap = {
  'DRAFT': { label: 'Nháp', color: 'bg-slate-100 text-slate-700' },
  'PENDING': { label: 'Chờ duyệt', color: 'bg-yellow-100 text-yellow-700' },
  'APPROVED': { label: 'Đã duyệt', color: 'bg-green-100 text-green-700' },
  'REJECTED': { label: 'Từ chối', color: 'bg-red-100 text-red-700' },
};

export default function TrainingPlanTable({ 
  plans, 
  count, 
  page, 
  setPage, 
  isLoading,
  canUpdate,
  canDelete,
  onEdit,
  setDeleteConfig
}) {
  const navigate = useNavigate();

  if (isLoading) return <div className="text-center py-8">Đang tải...</div>;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[300px]">Tên kế hoạch</TableHead>
              <TableHead>Học kỳ</TableHead>
              <TableHead>Khoa quản lý</TableHead>
              <TableHead>Trạng thái</TableHead>
              <TableHead className="text-right">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {plans.length === 0 ? (
              <TableRow>
                <TableCell colSpan={5} className="text-center py-8 text-slate-500">
                  Không tìm thấy kế hoạch đào tạo nào
                </TableCell>
              </TableRow>
            ) : (
              plans.map((plan) => (
                <TableRow key={plan.id}>
                  <TableCell className="font-medium">{plan.name}</TableCell>
                  <TableCell>{plan.semester?.name}</TableCell>
                  <TableCell>{plan.department?.name}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className={statusMap[plan.status]?.color}>
                      {statusMap[plan.status]?.label || plan.status}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => navigate(`/curriculum/training-plans/${plan.id}`)}
                        title="Xem chi tiết"
                      >
                        <Eye className="w-4 h-4 text-indigo-500" />
                      </Button>
                      {canUpdate && (
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => onEdit(plan)}
                        >
                          <Edit className="w-4 h-4 text-blue-500" />
                        </Button>
                      )}
                      {canDelete && (
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => setDeleteConfig({ isOpen: true, id: plan.id })}
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
