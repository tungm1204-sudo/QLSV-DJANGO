import { useState } from "react";
import { useClassrooms, useEnrollments, useAddEnrollment, useRemoveEnrollment } from "../features/academics/hooks";
import { useStudents } from "../features/students/hooks";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import {
  Table, TableBody, TableCell, TableHead,
  TableHeader, TableRow
} from "@/components/ui/table";
import { UserPlus, Trash2, Users, Search, ChevronRight } from "lucide-react";

export default function EnrollmentPage() {
  const { data: classroomsData } = useClassrooms();
  const classrooms = Array.isArray(classroomsData) ? classroomsData : classroomsData?.results || [];

  const [selectedClassroom, setSelectedClassroom] = useState(null);
  const [classroomSearch, setClassroomSearch] = useState("");
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [studentSearch, setStudentSearch] = useState("");

  // Danh sách SV đã enrolled trong lớp được chọn
  const { data: enrollmentsData, isLoading: enrollLoading } = useEnrollments(selectedClassroom?.id);
  const enrollments = Array.isArray(enrollmentsData) ? enrollmentsData : enrollmentsData?.results || [];

  // Danh sách tất cả SV (để chọn thêm vào lớp)
  const { data: studentsData } = useStudents({ search: studentSearch });
  const allStudents = Array.isArray(studentsData) ? studentsData : studentsData?.results || [];

  const addMutation = useAddEnrollment();
  const removeMutation = useRemoveEnrollment();

  // Set MSSV đã enrolled để tránh thêm trùng
  const enrolledStudentIds = new Set(enrollments.map(e => e.student));

  const handleAddStudent = async (studentId) => {
    try {
      await addMutation.mutateAsync({
        classroom: selectedClassroom.id,
        student: studentId,
      });
    } catch (err) {
      if (err.response?.status === 400) {
        alert("Sinh viên này đã có trong lớp!");
      } else {
        alert("Lỗi: " + JSON.stringify(err.response?.data));
      }
    }
  };

  const handleRemove = (enrollment) => {
    if (window.confirm(`Xóa sinh viên "${enrollment.student_name}" khỏi lớp "${selectedClassroom.name}"?`)) {
      removeMutation.mutate({ id: enrollment.id, classroomId: String(selectedClassroom.id) });
    }
  };

  const filteredClassrooms = classrooms.filter(c =>
    c.name.toLowerCase().includes(classroomSearch.toLowerCase()) ||
    (c.semester_name || "").toLowerCase().includes(classroomSearch.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Quản Lý Sinh Viên Trong Lớp</h1>
        <p className="text-muted-foreground">Ghi danh và quản lý danh sách sinh viên cho từng lớp sinh hoạt.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Panel trái: Danh sách lớp */}
        <div className="lg:col-span-1 bg-white rounded-lg border shadow-sm overflow-hidden">
          <div className="p-4 border-b bg-muted/30">
            <h2 className="font-semibold text-sm text-muted-foreground uppercase tracking-wider mb-3">Chọn Lớp Học</h2>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                className="pl-9 h-9"
                placeholder="Tìm lớp..."
                value={classroomSearch}
                onChange={e => setClassroomSearch(e.target.value)}
              />
            </div>
          </div>
          <div className="overflow-y-auto max-h-[calc(100vh-280px)]">
            {filteredClassrooms.length === 0 ? (
              <div className="p-6 text-center text-sm text-muted-foreground">Không tìm thấy lớp nào.</div>
            ) : (
              filteredClassrooms.map(c => (
                <button
                  key={c.id}
                  onClick={() => setSelectedClassroom(c)}
                  className={`w-full text-left px-4 py-3 flex items-center justify-between border-b last:border-0 transition-colors ${
                    selectedClassroom?.id === c.id
                      ? "bg-primary/10 text-primary font-medium"
                      : "hover:bg-muted/40"
                  }`}
                >
                  <div>
                    <p className="font-medium text-sm">{c.name}</p>
                    <p className="text-xs text-muted-foreground mt-0.5">{c.semester_name}</p>
                  </div>
                  <ChevronRight className={`h-4 w-4 shrink-0 ${selectedClassroom?.id === c.id ? "text-primary" : "text-muted-foreground"}`} />
                </button>
              ))
            )}
          </div>
        </div>

        {/* Panel phải: Danh sách SV trong lớp */}
        <div className="lg:col-span-2 bg-white rounded-lg border shadow-sm overflow-hidden">
          {!selectedClassroom ? (
            <div className="h-full flex flex-col items-center justify-center p-12 text-muted-foreground">
              <Users className="h-12 w-12 mb-4 opacity-20" />
              <p className="font-medium">Chọn một lớp học ở bên trái</p>
              <p className="text-sm">để xem và quản lý danh sách sinh viên.</p>
            </div>
          ) : (
            <>
              <div className="p-4 border-b bg-muted/30 flex items-center justify-between">
                <div>
                  <h2 className="font-semibold">
                    Lớp: <span className="text-primary">{selectedClassroom.name}</span>
                  </h2>
                  <p className="text-xs text-muted-foreground">
                    {selectedClassroom.semester_name} · {enrollments.length} sinh viên
                  </p>
                </div>
                <Button size="sm" onClick={() => setIsAddOpen(true)}>
                  <UserPlus className="mr-2 h-4 w-4" /> Thêm Sinh Viên
                </Button>
              </div>

              <Table>
                <TableHeader>
                  <TableRow className="bg-muted/20">
                    <TableHead className="w-[130px]">MSSV</TableHead>
                    <TableHead>Họ và Tên</TableHead>
                    <TableHead>Email</TableHead>
                    <TableHead>Ngày Ghi Danh</TableHead>
                    <TableHead className="text-right">Thao tác</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {enrollLoading ? (
                    <TableRow>
                      <TableCell colSpan={5} className="h-16 text-center">Đang tải...</TableCell>
                    </TableRow>
                  ) : enrollments.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} className="h-24 text-center text-muted-foreground">
                        Chưa có sinh viên nào trong lớp này.
                        <br />
                        <span className="text-sm">Bấm "Thêm Sinh Viên" để ghi danh.</span>
                      </TableCell>
                    </TableRow>
                  ) : (
                    enrollments.map(e => (
                      <TableRow key={e.id} className="hover:bg-muted/30">
                        <TableCell>
                          <Badge variant="outline" className="font-mono text-xs">{e.mssv || "—"}</Badge>
                        </TableCell>
                        <TableCell className="font-medium">{e.student_name}</TableCell>
                        <TableCell className="text-sm text-muted-foreground">{e.student_email}</TableCell>
                        <TableCell className="text-sm text-muted-foreground">
                          {e.enrolled_at ? new Date(e.enrolled_at).toLocaleDateString("vi-VN") : "—"}
                        </TableCell>
                        <TableCell className="text-right">
                          <Button
                            variant="ghost"
                            size="icon"
                            className="h-8 w-8 text-red-500 hover:text-red-700 hover:bg-red-50"
                            onClick={() => handleRemove(e)}
                            disabled={removeMutation.isPending}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </>
          )}
        </div>
      </div>

      {/* Dialog thêm sinh viên */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogContent className="max-w-lg max-h-[80vh] flex flex-col">
          <DialogHeader>
            <DialogTitle>
              Thêm Sinh Viên vào Lớp <span className="text-primary">{selectedClassroom?.name}</span>
            </DialogTitle>
          </DialogHeader>

          <div className="space-y-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                className="pl-9"
                placeholder="Tìm theo tên hoặc MSSV..."
                value={studentSearch}
                onChange={e => setStudentSearch(e.target.value)}
              />
            </div>
            <p className="text-xs text-muted-foreground">
              Sinh viên đã trong lớp sẽ bị mờ và không thể thêm lại.
            </p>
          </div>

          <div className="overflow-y-auto flex-1 border rounded-lg mt-2">
            {allStudents.length === 0 ? (
              <div className="p-6 text-center text-sm text-muted-foreground">Không tìm thấy sinh viên nào.</div>
            ) : (
              allStudents.map(s => {
                const studentId = s.user?.id || s.user;
                const alreadyEnrolled = enrolledStudentIds.has(studentId);
                return (
                  <div
                    key={s.mssv}
                    className={`flex items-center justify-between p-3 border-b last:border-0 ${
                      alreadyEnrolled ? "opacity-40" : "hover:bg-muted/30"
                    }`}
                  >
                    <div>
                      <p className="font-medium text-sm">{s.full_name}</p>
                      <p className="text-xs text-muted-foreground">MSSV: {s.mssv}</p>
                    </div>
                    {alreadyEnrolled ? (
                      <Badge variant="secondary" className="text-xs">Đã có</Badge>
                    ) : (
                      <Button
                        size="sm"
                        variant="outline"
                        className="h-8"
                        disabled={addMutation.isPending}
                        onClick={() => handleAddStudent(studentId)}
                      >
                        <UserPlus className="mr-1 h-3 w-3" /> Thêm
                      </Button>
                    )}
                  </div>
                );
              })
            )}
          </div>

          <div className="pt-3 flex justify-end">
            <Button variant="outline" onClick={() => setIsAddOpen(false)}>Đóng</Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
