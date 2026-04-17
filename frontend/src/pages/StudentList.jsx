import { useState } from 'react';
import { useStudents, useDeleteStudent } from '../features/students/hooks';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { 
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { 
  Plus, Search, Pencil, Trash2, Download, Upload, FileSpreadsheet 
} from 'lucide-react';
import StudentForm from '@/components/StudentForm';
import { useExportStudents, useImportStudents } from '../features/students/hooks';

export default function StudentList() {
  const [searchQuery, setSearchQuery] = useState('');
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const { data, isLoading, isError } = useStudents({ search: searchQuery });
  const deleteMutation = useDeleteStudent();
  const exportMutation = useExportStudents();
  const importMutation = useImportStudents();

  // If using pagination, data will likely be { count, next, previous, results: [...] }
  // depending on DRF setup. Assuming default PageNumberPagination
  const students = Array.isArray(data) ? data : data?.results || [];

  const handleDelete = (mssv) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa sinh viên này?')) {
      deleteMutation.mutate(mssv);
    }
  };

  const handleOpenEdit = (student) => {
    setSelectedStudent(student);
    setIsFormOpen(true);
  };

  const handleOpenCreate = () => {
    setSelectedStudent(null);
    setIsFormOpen(true);
  };

  return (
    <div className="space-y-6">
      <StudentForm isOpen={isFormOpen} setIsOpen={setIsFormOpen} studentToEdit={selectedStudent} />

      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
            Quản lý Sinh viên
          </h1>
          <p className="text-sm text-gray-500">Danh sách toàn bộ sinh viên trong hệ thống</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => exportMutation.mutate()}>
            <Download className="mr-2 h-4 w-4" /> Xuất Excel
          </Button>
          <label className="cursor-pointer">
            <Button variant="outline" asChild>
              <div>
                <Upload className="mr-2 h-4 w-4" /> Nhập Excel
                <input
                  type="file"
                  className="hidden"
                  accept=".xlsx, .xls"
                  onChange={(e) => {
                    if (e.target.files?.[0]) {
                      importMutation.mutate(e.target.files[0]);
                    }
                  }}
                />
              </div>
            </Button>
          </label>
          <Button onClick={handleOpenCreate}>
            <Plus className="mr-2 h-4 w-4" /> Thêm Sinh Viên
          </Button>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-gray-500" />
          <Input
            placeholder="Tìm kiếm theo MSSV hoặc Tên..."
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
              <TableHead>MSSV</TableHead>
              <TableHead>Họ và Tên</TableHead>
              <TableHead>Ngày Sinh</TableHead>
              <TableHead>Giới Tính</TableHead>
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
            ) : students.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-gray-500">
                  Không tìm thấy sinh viên nào.
                </TableCell>
              </TableRow>
            ) : (
              students.map((student) => (
                <TableRow key={student.id}>
                  <TableCell className="font-medium">{student.mssv}</TableCell>
                  <TableCell>{student.full_name}</TableCell>
                  <TableCell>{new Date(student.dob).toLocaleDateString('vi-VN')}</TableCell>
                  <TableCell>
                    {student.gender === 'male' ? 'Nam' : student.gender === 'female' ? 'Nữ' : 'Khác'}
                  </TableCell>
                  <TableCell>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      student.status 
                        ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
                    }`}>
                      {student.status ? 'Đang học' : 'Nghỉ học'}
                    </span>
                  </TableCell>
                  <TableCell className="text-right space-x-2">
                    <Button variant="ghost" size="icon" onClick={() => handleOpenEdit(student)}>
                      <Pencil className="h-4 w-4 text-blue-600" />
                    </Button>
                    <Button variant="ghost" size="icon" onClick={() => handleDelete(student.mssv)}>
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
