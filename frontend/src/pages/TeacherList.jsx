import { useState } from 'react';
import { useTeachers, useDeleteTeacher } from '../features/teachers/hooks';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { Plus, Search, Pencil, Trash2 } from 'lucide-react';
import TeacherForm from '@/components/TeacherForm';

export default function TeacherList() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedTeacher, setSelectedTeacher] = useState(null);

  const { data, isLoading } = useTeachers({ search: searchQuery });
  const deleteMutation = useDeleteTeacher();

  const teachers = Array.isArray(data) ? data : data?.results || [];

  const handleDelete = (mgv) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa giáo viên này?')) {
      deleteMutation.mutate(mgv);
    }
  };

  const handleOpenEdit = (teacher) => {
    setSelectedTeacher(teacher);
    setIsFormOpen(true);
  };

  const handleOpenCreate = () => {
    setSelectedTeacher(null);
    setIsFormOpen(true);
  };

  return (
    <div className="space-y-6">
      <TeacherForm isOpen={isFormOpen} setIsOpen={setIsFormOpen} teacherToEdit={selectedTeacher} />

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            Quản lý Giáo viên
          </h1>
          <p className="text-sm text-gray-500">Danh sách toàn bộ giáo viên trong hệ thống</p>
        </div>
        <Button onClick={handleOpenCreate}>
          <Plus className="mr-2 h-4 w-4" /> Thêm Giáo Viên
        </Button>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
          <Input
            placeholder="Tìm kiếm theo MGV hoặc Tên..."
            className="pl-9"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>MGV</TableHead>
              <TableHead>Họ và Tên</TableHead>
              <TableHead>Khoa/Bộ Môn</TableHead>
              <TableHead>Chuyên Môn</TableHead>
              <TableHead>Trạng Thái</TableHead>
              <TableHead className="text-right">Hành động</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-gray-500">
                  Đang tải dữ liệu...
                </TableCell>
              </TableRow>
            ) : teachers.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-gray-500">
                  Không tìm thấy giáo viên nào.
                </TableCell>
              </TableRow>
            ) : (
              teachers.map((teacher) => (
                <TableRow key={teacher.id}>
                  <TableCell className="font-medium">{teacher.mgv}</TableCell>
                  <TableCell>{teacher.full_name}</TableCell>
                  <TableCell>{teacher.department_detail?.name || '---'}</TableCell>
                  <TableCell>{teacher.specialization || '---'}</TableCell>
                  <TableCell>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      teacher.status 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                    }`}>
                      {teacher.status ? 'Đang dạy' : 'Nghỉ việc'}
                    </span>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button variant="ghost" size="icon" onClick={() => handleOpenEdit(teacher)}>
                      <Pencil className="h-4 w-4 text-blue-600" />
                    </Button>
                    <Button variant="ghost" size="icon" onClick={() => handleDelete(teacher.mgv)}>
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
