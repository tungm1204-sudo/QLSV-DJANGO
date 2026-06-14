import { useState, useEffect } from "react";
import { 
  useClassrooms, useCourses, useSemesters, useExamTypes, 
  useGradeSheet, useBulkUpdateGrades 
} from "../features/academics/hooks";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Save, CheckCircle2 } from "lucide-react";

export default function ExamResultPage() {
  const { data: classroomsData } = useClassrooms();
  const { data: coursesData } = useCourses();
  const { data: semestersData } = useSemesters();
  const { data: examTypesData } = useExamTypes();

  const classrooms = Array.isArray(classroomsData) ? classroomsData : classroomsData?.results || [];
  const courses = Array.isArray(coursesData) ? coursesData : coursesData?.results || [];
  const semesters = Array.isArray(semestersData) ? semestersData : semestersData?.results || [];
  const examTypes = Array.isArray(examTypesData) ? examTypesData : examTypesData?.results || [];

  const [selectedClassroom, setSelectedClassroom] = useState("");
  const [selectedCourse, setSelectedCourse] = useState("");
  const [selectedSemester, setSelectedSemester] = useState("");
  const [selectedExamType, setSelectedExamType] = useState("");
  
  const filterParams = {
    classroom: selectedClassroom,
    course: selectedCourse,
    semester: selectedSemester,
    exam_type: selectedExamType
  };

  const isFilterComplete = selectedClassroom && selectedCourse && selectedSemester && selectedExamType;
  
  const { data: sheetData, isLoading, isFetching } = useGradeSheet(filterParams);
  const updateMutation = useBulkUpdateGrades();

  const [gradesState, setGradesState] = useState({});

  useEffect(() => {
    if (sheetData) {
      const initialState = {};
      sheetData.forEach(item => {
        initialState[item.student_id] = {
          marks: item.marks !== "" ? item.marks : "",
          max_marks: item.max_marks || 10,
          remark: item.remarks || ""
        };
      });
      setGradesState(initialState);
    }
  }, [sheetData]);

  const handleMarkChange = (studentId, marks) => {
    setGradesState(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], marks }
    }));
  };

  const handleRemarkChange = (studentId, remark) => {
    setGradesState(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], remark }
    }));
  };

  const handleSave = async () => {
    if (!isFilterComplete) return;

    const results = Object.keys(gradesState)
      .filter(studentId => gradesState[studentId].marks !== "") // Only save if there's a mark
      .map(studentId => ({
        student: studentId,
        classroom: selectedClassroom,
        course: selectedCourse,
        semester: selectedSemester,
        exam_type: selectedExamType,
        marks: parseFloat(gradesState[studentId].marks),
        max_marks: parseFloat(gradesState[studentId].max_marks),
        remarks: gradesState[studentId].remark
      }));

    if (results.length === 0) {
      alert("Chưa có điểm nào được nhập!");
      return;
    }

    try {
      await updateMutation.mutateAsync({ results });
      alert("Đã lưu điểm thành công!");
    } catch (error) {
      console.error("Lỗi khi lưu điểm:", error);
      alert("Đã xảy ra lỗi khi lưu điểm.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Nhập Điểm</h1>
          <p className="text-muted-foreground">Nhập và quản lý điểm số sinh viên cho từng môn học.</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 grid grid-cols-1 md:grid-cols-5 gap-4 items-end">
        
        <div className="space-y-2">
          <Label>Học Kỳ</Label>
          <select 
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={selectedSemester}
            onChange={(e) => setSelectedSemester(e.target.value)}
          >
            <option value="" disabled>-- Chọn học kỳ --</option>
            {semesters.map(s => (
              <option key={s.id} value={s.id}>{s.name}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label>Lớp Sinh Hoạt</Label>
          <select 
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={selectedClassroom}
            onChange={(e) => setSelectedClassroom(e.target.value)}
          >
            <option value="" disabled>-- Chọn lớp --</option>
            {classrooms.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label>Học Phần (Môn)</Label>
          <select 
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={selectedCourse}
            onChange={(e) => setSelectedCourse(e.target.value)}
          >
            <option value="" disabled>-- Chọn môn --</option>
            {courses.map(c => (
              <option key={c.id} value={c.id}>{c.name}</option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label>Loại Kỳ Thi</Label>
          <select 
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={selectedExamType}
            onChange={(e) => setSelectedExamType(e.target.value)}
          >
            <option value="" disabled>-- Chọn kỳ thi --</option>
            {examTypes.map(t => (
              <option key={t.id} value={t.id}>{t.name} (HS: {t.weight})</option>
            ))}
          </select>
        </div>

        <div className="">
          <Button 
            className="w-full" 
            onClick={handleSave} 
            disabled={!isFilterComplete || Object.keys(gradesState).length === 0 || updateMutation.isPending}
          >
            <Save className="mr-2 h-4 w-4" /> 
            {updateMutation.isPending ? "Đang lưu..." : "Lưu Điểm"}
          </Button>
        </div>
      </div>

      {isFilterComplete && (
        <div className="border rounded-lg bg-white shadow-sm overflow-hidden relative">
          {(isLoading || isFetching) && (
            <div className="absolute inset-0 bg-white/50 flex items-center justify-center z-10">
              <span className="text-gray-500 font-medium">Đang tải danh sách...</span>
            </div>
          )}

          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[120px]">MSSV</TableHead>
                <TableHead>Họ và Tên</TableHead>
                <TableHead className="w-[150px]">Điểm</TableHead>
                <TableHead>Ghi chú</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(!sheetData || sheetData.length === 0) && !isLoading && !isFetching ? (
                <TableRow>
                  <TableCell colSpan={4} className="h-24 text-center text-muted-foreground">
                    Không có sinh viên nào trong lớp này.
                  </TableCell>
                </TableRow>
              ) : (
                sheetData?.map((item) => {
                  const state = gradesState[item.student_id];
                  if (!state) return null;

                  return (
                    <TableRow key={item.student_id} className="hover:bg-muted/30">
                      <TableCell className="font-mono text-sm font-medium">{item.mssv}</TableCell>
                      <TableCell className="font-medium">
                        {item.student_name}
                        {item.is_recorded && (
                          <CheckCircle2 className="inline ml-2 h-4 w-4 text-green-500" title="Đã có điểm" />
                        )}
                      </TableCell>
                      
                      <TableCell>
                        <div className="flex items-center space-x-2">
                          <Input 
                            type="number"
                            min="0"
                            max={state.max_marks}
                            step="0.1"
                            className="w-20 h-9"
                            value={state.marks}
                            onChange={(e) => handleMarkChange(item.student_id, e.target.value)}
                          />
                          <span className="text-sm text-muted-foreground">/ {state.max_marks}</span>
                        </div>
                      </TableCell>
                      
                      <TableCell>
                        <Input 
                          placeholder="Ghi chú..." 
                          className="h-9"
                          value={state.remark}
                          onChange={(e) => handleRemarkChange(item.student_id, e.target.value)}
                        />
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
