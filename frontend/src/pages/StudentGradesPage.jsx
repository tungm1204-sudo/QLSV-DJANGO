import { useStudentGPA, useCourses } from "../features/academics/hooks";
import { useAuthStore } from "../stores/authStore";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { BookOpen, GraduationCap, Trophy } from "lucide-react";

export default function StudentGradesPage() {
  const { user } = useAuthStore();
  const { data: coursesData } = useCourses();
  
  // For student role, pass undefined so backend uses request.user
  // For admin/teacher viewing a student, pass the student's id
  const studentIdParam = user?.role === "student" ? undefined : user?.id;
  const { data, isLoading } = useStudentGPA(studentIdParam);

  // Build a quick lookup map: course id -> course name
  const coursesArray = Array.isArray(coursesData) ? coursesData : coursesData?.results || [];
  const courseNameMap = {};
  coursesArray.forEach(c => { courseNameMap[c.id] = c.name; });

  if (isLoading) return <div className="p-8 text-center">Đang tải kết quả học tập...</div>;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Kết Quả Học Tập</h1>
        <p className="text-muted-foreground">Theo dõi tiến độ học tập và điểm trung bình tích lũy (GPA).</p>
      </div>

      {data && (
        <div className="grid gap-4 md:grid-cols-3">
          <div className="bg-white rounded-lg border shadow-sm p-6">
            <div className="flex flex-row items-center justify-between pb-2">
              <p className="text-sm font-medium text-muted-foreground">Tổng Tín Chỉ Tích Lũy</p>
              <BookOpen className="h-4 w-4 text-muted-foreground" />
            </div>
            <div className="text-2xl font-bold">{data.total_credits} TC</div>
          </div>
          
          <div className="bg-white rounded-lg border shadow-sm p-6">
            <div className="flex flex-row items-center justify-between pb-2">
              <p className="text-sm font-medium text-muted-foreground">GPA (Hệ 10)</p>
              <Trophy className="h-4 w-4 text-yellow-500" />
            </div>
            <div className="text-2xl font-bold">{data.gpa_10}</div>
          </div>
          
          <div className="bg-white rounded-lg border shadow-sm p-6">
            <div className="flex flex-row items-center justify-between pb-2">
              <p className="text-sm font-medium text-muted-foreground">GPA (Hệ 4)</p>
              <GraduationCap className="h-4 w-4 text-primary" />
            </div>
            <div className="text-2xl font-bold">{data.gpa_4}</div>
          </div>
        </div>
      )}

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden mt-6">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Mã Môn</TableHead>
              <TableHead>Tín Chỉ</TableHead>
              <TableHead className="text-right">Điểm Tổng Kết (Hệ 10)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {(!data || data.course_details.length === 0) ? (
              <TableRow>
                <TableCell colSpan={3} className="h-24 text-center text-muted-foreground">
                  Chưa có kết quả điểm số cho môn học nào.
                </TableCell>
              </TableRow>
            ) : (
              data.course_details.map((course) => (
                <TableRow key={course.course_id} className="hover:bg-muted/30">
                  <TableCell className="font-semibold">
                    {courseNameMap[course.course_id] || `Môn #${course.course_id}`}
                  </TableCell>
                  <TableCell>{course.credits} TC</TableCell>
                  <TableCell className="text-right font-bold text-primary">
                    {course.final_score}
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
