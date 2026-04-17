import { useState } from "react";
import { useCourses } from "../features/academics/hooks";
import { Button } from "@/components/ui/button";
import { Plus, Edit, Trash2, Library } from "lucide-react";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function CourseList() {
  const { data, isLoading } = useCourses();
  const [isOpen, setIsOpen] = useState(false);

  const courses = Array.isArray(data) ? data : data?.results || [];

  if (isLoading) return <div className="p-8 text-center">Đang tải danh sách môn học...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Cấu trúc Khối & Môn học</h1>
          <p className="text-muted-foreground">Quản lý danh mục môn học và phân bổ tín chỉ.</p>
        </div>
        <Button onClick={() => setIsOpen(true)}>
          <Plus className="mr-2 h-4 w-4" /> Thêm Môn học
        </Button>
      </div>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead className="w-[120px]">Mã Môn</TableHead>
              <TableHead>Tên Môn Học</TableHead>
              <TableHead>Khối Lớp</TableHead>
              <TableHead>Số Tín Chỉ</TableHead>
              <TableHead>Mô tả</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {courses?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  Chưa có môn học nào được định nghĩa.
                </TableCell>
              </TableRow>
            ) : (
              courses?.map((course) => (
                <TableRow key={course.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-mono text-xs font-bold">{course.code}</TableCell>
                  <TableCell className="font-medium">{course.name}</TableCell>
                  <TableCell>
                    <Badge variant="outline">{course.grade_name}</Badge>
                  </TableCell>
                  <TableCell>
                    <span className="flex items-center">
                      <Library className="mr-2 h-3 w-3 text-primary" />
                      {course.credits} TC
                    </span>
                  </TableCell>
                  <TableCell className="max-w-[300px] truncate text-muted-foreground italic">
                    {course.description || "Không có mô tả"}
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
