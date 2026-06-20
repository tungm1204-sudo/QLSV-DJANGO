import { useState } from "react";
import { useAssignments, useDeleteAssignment, useClassrooms, useCourses } from "../features/academics/hooks";
import { useTeachers } from "../features/teachers/hooks";
import AssignmentForm from "@/components/AssignmentForm";
import { Button } from "@/components/ui/button";
import { Plus, Edit, Trash2, CalendarDays, FilterX } from "lucide-react";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

export default function AssignmentList() {
  const [filterClassroom, setFilterClassroom] = useState("");
  const [filterCourse, setFilterCourse] = useState("");
  const [filterTeacher, setFilterTeacher] = useState("");

  const params = {};
  if (filterClassroom) params.classroom = filterClassroom;
  if (filterCourse) params.course = filterCourse;
  if (filterTeacher) params.teacher = filterTeacher;

  const { data, isLoading } = useAssignments(params);
  const deleteMutation = useDeleteAssignment();
  
  const { data: classroomsData } = useClassrooms();
  const { data: coursesData } = useCourses();
  const { data: teachersData } = useTeachers();

  const classrooms = Array.isArray(classroomsData) ? classroomsData : classroomsData?.results || [];
  const courses = Array.isArray(coursesData) ? coursesData : coursesData?.results || [];
  const teachers = Array.isArray(teachersData) ? teachersData : teachersData?.results || [];

  const [isOpen, setIsOpen] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState(null);

  const handleDelete = (id) => {
    if (window.confirm("Bạn có chắc chắn muốn xóa phân công này?")) {
      deleteMutation.mutate(id);
    }
  };

  const handleOpenEdit = (assignment) => {
    setSelectedAssignment(assignment);
    setIsOpen(true);
  };

  const handleOpenCreate = () => {
    setSelectedAssignment(null);
    setIsOpen(true);
  };

  const clearFilters = () => {
    setFilterClassroom("");
    setFilterCourse("");
    setFilterTeacher("");
  };

  const assignments = Array.isArray(data) ? data : data?.results || [];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Phân Công Giảng Dạy</h1>
          <p className="text-muted-foreground">Quản lý việc phân công giảng viên dạy các học phần cho từng lớp.</p>
        </div>
        <Button onClick={handleOpenCreate}>
          <Plus className="mr-2 h-4 w-4" /> Thêm Phân Công
        </Button>
      </div>

      <AssignmentForm isOpen={isOpen} setIsOpen={setIsOpen} assignmentToEdit={selectedAssignment} />

      <div className="bg-white p-4 rounded-lg shadow-sm border flex gap-4 items-end flex-wrap">
        <div className="space-y-1 flex-1 min-w-[200px]">
          <label className="text-sm font-medium">Lọc theo Lớp</label>
          <select 
            className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm"
            value={filterClassroom}
            onChange={(e) => setFilterClassroom(e.target.value)}
          >
            <option value="">-- Tất cả các lớp --</option>
            {classrooms.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="space-y-1 flex-1 min-w-[200px]">
          <label className="text-sm font-medium">Lọc theo Môn Học</label>
          <select 
            className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm"
            value={filterCourse}
            onChange={(e) => setFilterCourse(e.target.value)}
          >
            <option value="">-- Tất cả môn học --</option>
            {courses.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </div>
        <div className="space-y-1 flex-1 min-w-[200px]">
          <label className="text-sm font-medium">Lọc theo Giảng Viên</label>
          <select 
            className="flex h-9 w-full rounded-md border border-input bg-background px-3 py-1 text-sm shadow-sm"
            value={filterTeacher}
            onChange={(e) => setFilterTeacher(e.target.value)}
          >
            <option value="">-- Tất cả giảng viên --</option>
            {teachers.map(t => <option key={t.id} value={t.id}>{t.full_name}</option>)}
          </select>
        </div>
        {(filterClassroom || filterCourse || filterTeacher) && (
          <Button variant="ghost" className="h-9 text-muted-foreground" onClick={clearFilters}>
            <FilterX className="mr-2 h-4 w-4" /> Xóa lọc
          </Button>
        )}
      </div>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Lớp Sinh Hoạt</TableHead>
              <TableHead>Học Phần (Môn Học)</TableHead>
              <TableHead>Giảng Viên Phụ Trách</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">Đang tải danh sách phân công...</TableCell>
              </TableRow>
            ) : assignments?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={4} className="h-24 text-center">
                  Chưa có phân công giảng dạy nào.
                </TableCell>
              </TableRow>
            ) : (
              assignments?.map((assignment) => (
                <TableRow key={assignment.id} className="hover:bg-muted/30 transition-colors">
                  <TableCell className="font-semibold">
                    <div className="flex items-center">
                      <CalendarDays className="mr-2 h-4 w-4 text-muted-foreground" />
                      {assignment.classroom_name}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline" className="bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200">
                      {assignment.course_name}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium text-gray-700">
                    {assignment.teacher_name}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600" onClick={() => handleOpenEdit(assignment)}>
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600" onClick={() => handleDelete(assignment.id)}>
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
