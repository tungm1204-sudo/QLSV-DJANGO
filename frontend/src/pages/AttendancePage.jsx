import { useState, useEffect } from "react";
import { useClassrooms, useAttendanceSheet, useBulkUpdateAttendance } from "../features/academics/hooks";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { 
  Table, TableBody, TableCell, TableHead, 
  TableHeader, TableRow 
} from "@/components/ui/table";
import { Save, CheckCircle2 } from "lucide-react";

export default function AttendancePage() {
  const { data: classroomsData } = useClassrooms();
  const classrooms = Array.isArray(classroomsData) ? classroomsData : classroomsData?.results || [];

  const [selectedClassroom, setSelectedClassroom] = useState("");
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  
  const { data: sheetData, isLoading, isFetching } = useAttendanceSheet(selectedClassroom, selectedDate);
  const updateMutation = useBulkUpdateAttendance();

  const [attendanceState, setAttendanceState] = useState({});

  useEffect(() => {
    if (sheetData) {
      const initialState = {};
      sheetData.forEach(item => {
        initialState[item.student_id] = {
          status: item.status,
          remark: item.remark || ""
        };
      });
      setAttendanceState(initialState);
    }
  }, [sheetData]);

  const handleStatusChange = (studentId, status) => {
    setAttendanceState(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], status }
    }));
  };

  const handleRemarkChange = (studentId, remark) => {
    setAttendanceState(prev => ({
      ...prev,
      [studentId]: { ...prev[studentId], remark }
    }));
  };

  const handleSave = async () => {
    if (!selectedClassroom || !selectedDate) return;

    const attendances = Object.keys(attendanceState).map(studentId => ({
      student: studentId,
      classroom: selectedClassroom,
      date: selectedDate,
      status: attendanceState[studentId].status,
      remark: attendanceState[studentId].remark
    }));

    try {
      await updateMutation.mutateAsync({ attendances });
      alert("Đã lưu điểm danh thành công!");
    } catch (error) {
      console.error("Lỗi khi lưu điểm danh:", error);
      alert("Đã xảy ra lỗi khi lưu điểm danh.");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Điểm danh</h1>
          <p className="text-muted-foreground">Theo dõi và ghi nhận sự có mặt của sinh viên trong lớp học.</p>
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg shadow-sm border border-gray-200 flex flex-col sm:flex-row gap-4 items-end">
        <div className="space-y-2 flex-1">
          <Label>Chọn Lớp Sinh Hoạt</Label>
          <select 
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedClassroom}
            onChange={(e) => setSelectedClassroom(e.target.value)}
          >
            <option value="" disabled>-- Chọn lớp --</option>
            {classrooms.map(c => (
              <option key={c.id} value={c.id}>{c.name} - {c.semester_name}</option>
            ))}
          </select>
        </div>
        
        <div className="space-y-2 flex-1">
          <Label>Ngày Điểm Danh</Label>
          <Input 
            type="date" 
            value={selectedDate} 
            onChange={(e) => setSelectedDate(e.target.value)} 
          />
        </div>

        <div className="flex-1">
          <Button 
            className="w-full" 
            onClick={handleSave} 
            disabled={!selectedClassroom || Object.keys(attendanceState).length === 0 || updateMutation.isPending}
          >
            <Save className="mr-2 h-4 w-4" /> 
            {updateMutation.isPending ? "Đang lưu..." : "Lưu Điểm Danh"}
          </Button>
        </div>
      </div>

      {selectedClassroom && (
        <div className="border rounded-lg bg-white shadow-sm overflow-hidden relative">
          {(isLoading || isFetching) && (
            <div className="absolute inset-0 bg-white/50 flex items-center justify-center z-10">
              <span className="text-gray-500 font-medium">Đang tải danh sách...</span>
            </div>
          )}

          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px]">MSSV</TableHead>
                <TableHead>Họ và Tên</TableHead>
                <TableHead className="text-center">Có mặt</TableHead>
                <TableHead className="text-center">Đi muộn</TableHead>
                <TableHead className="text-center">Có phép</TableHead>
                <TableHead className="text-center">Vắng mặt</TableHead>
                <TableHead>Ghi chú</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {(!sheetData || sheetData.length === 0) && !isLoading && !isFetching ? (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center text-muted-foreground">
                    Không có sinh viên nào trong lớp này hoặc chưa chọn lớp.
                  </TableCell>
                </TableRow>
              ) : (
                sheetData?.map((item) => {
                  const state = attendanceState[item.student_id];
                  if (!state) return null;

                  return (
                    <TableRow key={item.student_id} className="hover:bg-muted/30">
                      <TableCell className="font-mono text-xs">{item.mssv}</TableCell>
                      <TableCell className="font-medium">
                        {item.student_name}
                        {item.is_recorded && (
                          <CheckCircle2 className="inline ml-2 h-3 w-3 text-green-500" title="Đã có dữ liệu" />
                        )}
                      </TableCell>
                      
                      <TableCell className="text-center">
                        <input 
                          type="radio" 
                          name={`status-${item.student_id}`} 
                          checked={state.status === "present"}
                          onChange={() => handleStatusChange(item.student_id, "present")}
                          className="w-4 h-4 text-green-600 focus:ring-green-500"
                        />
                      </TableCell>
                      <TableCell className="text-center">
                        <input 
                          type="radio" 
                          name={`status-${item.student_id}`} 
                          checked={state.status === "late"}
                          onChange={() => handleStatusChange(item.student_id, "late")}
                          className="w-4 h-4 text-yellow-600 focus:ring-yellow-500"
                        />
                      </TableCell>
                      <TableCell className="text-center">
                        <input 
                          type="radio" 
                          name={`status-${item.student_id}`} 
                          checked={state.status === "excused"}
                          onChange={() => handleStatusChange(item.student_id, "excused")}
                          className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                        />
                      </TableCell>
                      <TableCell className="text-center">
                        <input 
                          type="radio" 
                          name={`status-${item.student_id}`} 
                          checked={state.status === "absent"}
                          onChange={() => handleStatusChange(item.student_id, "absent")}
                          className="w-4 h-4 text-red-600 focus:ring-red-500"
                        />
                      </TableCell>
                      
                      <TableCell>
                        <Input 
                          placeholder="Ghi chú..." 
                          className="h-8 text-sm"
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
