import { useState } from "react";
import { useClassrooms } from "../features/academics/hooks";
import { Button } from "@/components/ui/button";
import { Plus, Edit, Trash2, Users } from "lucide-react";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function ClassroomList() {
  const { data, isLoading } = useClassrooms();
  const [isOpen, setIsOpen] = useState(false);

  const classrooms = Array.isArray(data) ? data : data?.results || [];

  if (isLoading) return <div className="p-8 text-center">Đang tải danh sách lớp...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Quản lý Lớp học</h1>
          <p className="text-muted-foreground">Danh sách các lớp học theo từng học kỳ.</p>
        </div>
        <Button onClick={() => setIsOpen(true)}>
          <Plus className="mr-2 h-4 w-4" /> Thêm Lớp học
        </Button>
      </div>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="w-[150px]">Tên Lớp</TableHead>
              <TableHead>Khối</TableHead>
              <TableHead>Học Kỳ</TableHead>
              <TableHead>GV Chủ Nhiệm</TableHead>
              <TableHead>Sĩ Số</TableHead>
              <TableHead>Trạng Thái</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {classrooms?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} className="h-24 text-center">
                  Chưa có lớp học nào.
                </TableCell>
              </TableRow>
            ) : (
              classrooms?.map((cls) => (
                <TableRow key={cls.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-semibold">{cls.name}</TableCell>
                  <TableCell>{cls.grade_name}</TableCell>
                  <TableCell>{cls.semester_name}</TableCell>
                  <TableCell>{cls.teacher_name}</TableCell>
                  <TableCell>
                    <div className="flex items-center">
                      <Users className="mr-1 h-3 w-3 text-muted-foreground" />
                      0 / {cls.max_students}
                    </div>
                  </TableCell>
                  <TableCell>
                    {cls.status ? (
                      <Badge variant="success" className="bg-green-100 text-green-700 hover:bg-green-200 border-none">Hoạt động</Badge>
                    ) : (
                      <Badge variant="secondary">Đã đóng</Badge>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600">
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
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
