import { useAssignments, useAttendances } from "../features/academics/hooks";
import { CalendarDays, ClipboardCheck } from "lucide-react";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

const statusMap = {
  present: { label: "Có mặt", color: "bg-emerald-100 text-emerald-700 hover:bg-emerald-200" },
  absent: { label: "Vắng", color: "bg-red-100 text-red-700 hover:bg-red-200" },
  late: { label: "Đi muộn", color: "bg-amber-100 text-amber-700 hover:bg-amber-200" },
  excused: { label: "Có phép", color: "bg-blue-100 text-blue-700 hover:bg-blue-200" },
};

export default function StudentSchedulePage() {
  const { data: assignmentsData, isLoading: loadingAssignments } = useAssignments({});
  const { data: attendancesData, isLoading: loadingAttendances } = useAttendances({});

  const assignments = Array.isArray(assignmentsData) ? assignmentsData : assignmentsData?.results || [];
  const attendances = Array.isArray(attendancesData) ? attendancesData : attendancesData?.results || [];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">Thời Khóa Biểu & Điểm Danh</h1>
        <p className="text-muted-foreground mt-1">Danh sách môn học bạn đang tham gia và lịch sử điểm danh.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Lịch học (Assignments) */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <CalendarDays className="h-5 w-5 text-primary" /> Lịch Học (Môn Học Đã Đăng Ký)
          </h2>
          <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead>Môn Học</TableHead>
                  <TableHead>Lớp</TableHead>
                  <TableHead>Giảng Viên</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loadingAssignments ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center">Đang tải...</TableCell>
                  </TableRow>
                ) : assignments.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center">Bạn chưa có lịch học nào.</TableCell>
                  </TableRow>
                ) : (
                  assignments.map(a => (
                    <TableRow key={a.id}>
                      <TableCell className="font-medium text-blue-700">{a.course_name}</TableCell>
                      <TableCell>{a.classroom_name}</TableCell>
                      <TableCell>{a.teacher_name}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </div>
        </div>

        {/* Lịch sử điểm danh */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <ClipboardCheck className="h-5 w-5 text-emerald-600" /> Lịch Sử Điểm Danh
          </h2>
          <div className="border rounded-lg bg-white shadow-sm overflow-hidden h-[400px] overflow-y-auto">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead>Ngày</TableHead>
                  <TableHead>Lớp</TableHead>
                  <TableHead>Trạng Thái</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {loadingAttendances ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center">Đang tải...</TableCell>
                  </TableRow>
                ) : attendances.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={3} className="h-24 text-center">Chưa có dữ liệu điểm danh.</TableCell>
                  </TableRow>
                ) : (
                  attendances.map(att => {
                    const statusInfo = statusMap[att.status] || { label: att.status, color: "bg-gray-100" };
                    return (
                      <TableRow key={att.id}>
                        <TableCell className="whitespace-nowrap font-medium text-gray-700">{att.date}</TableCell>
                        <TableCell>
                          {att.classroom_name || `Lớp ${att.classroom}`}
                          {att.remark && <div className="text-xs text-muted-foreground mt-0.5">{att.remark}</div>}
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline" className={`border-none ${statusInfo.color}`}>
                            {statusInfo.label}
                          </Badge>
                        </TableCell>
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  );
}
