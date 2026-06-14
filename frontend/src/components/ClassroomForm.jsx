import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateClassroom, useUpdateClassroom, useGrades, useSemesters } from "../features/academics/hooks";
import { useTeachers } from "../features/teachers/hooks";

export default function ClassroomForm({ classroomToEdit = null, isOpen, setIsOpen }) {
  const createMutation = useCreateClassroom();
  const updateMutation = useUpdateClassroom();
  
  const { data: gradesData } = useGrades();
  const { data: semestersData } = useSemesters();
  const { data: teachersData } = useTeachers();

  const grades = Array.isArray(gradesData) ? gradesData : gradesData?.results || [];
  const semesters = Array.isArray(semestersData) ? semestersData : semestersData?.results || [];
  const teachers = Array.isArray(teachersData) ? teachersData : teachersData?.results || [];
  
  const [formData, setFormData] = useState({
    name: "",
    grade: "",
    semester: "",
    homeroom_teacher: "",
    max_students: 40,
    status: true,
    remarks: "",
  });

  useEffect(() => {
    if (classroomToEdit) {
      setFormData({
        name: classroomToEdit.name || "",
        grade: classroomToEdit.grade || "",
        semester: classroomToEdit.semester || "",
        homeroom_teacher: classroomToEdit.homeroom_teacher || "",
        max_students: classroomToEdit.max_students || 40,
        status: classroomToEdit.status ?? true,
        remarks: classroomToEdit.remarks || "",
      });
    } else {
      setFormData({
        name: "", grade: "", semester: "", homeroom_teacher: "", max_students: 40, status: true, remarks: ""
      });
    }
  }, [classroomToEdit, isOpen]);

  const handleChange = (e) => {
    const value = e.target.type === "checkbox" ? e.target.checked : e.target.value;
    setFormData((prev) => ({ ...prev, [e.target.name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = { ...formData };
    if (!payload.homeroom_teacher) {
      payload.homeroom_teacher = null;
    }

    try {
      if (classroomToEdit) {
        await updateMutation.mutateAsync({ id: classroomToEdit.id, data: payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      setIsOpen(false);
    } catch (error) {
      console.error("Lỗi khi lưu lớp sinh hoạt:", error.response?.data || error.message);
      alert("Đã xảy ra lỗi!\n" + JSON.stringify(error.response?.data));
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{classroomToEdit ? "Sửa Lớp Sinh Hoạt" : "Thêm Lớp Sinh Hoạt"}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Tên Lớp</Label>
            <Input id="name" name="name" value={formData.name} onChange={handleChange} required />
          </div>

          <div className="space-y-2">
            <Label>Khối Lớp</Label>
            <select 
              name="grade" 
              value={formData.grade} 
              onChange={handleChange}
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="" disabled>-- Chọn khối lớp --</option>
              {grades.map(g => (
                <option key={g.id} value={g.id}>{g.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label>Học Kỳ</Label>
            <select 
              name="semester" 
              value={formData.semester} 
              onChange={handleChange}
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="" disabled>-- Chọn học kỳ --</option>
              {semesters.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label>Giáo Viên Chủ Nhiệm</Label>
            <select 
              name="homeroom_teacher" 
              value={formData.homeroom_teacher || ""} 
              onChange={handleChange}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="">-- Chưa phân công --</option>
              {teachers.map(t => (
                <option key={t.id} value={t.id}>{t.full_name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="max_students">Sĩ Số Tối Đa</Label>
            <Input id="max_students" type="number" name="max_students" value={formData.max_students} onChange={handleChange} required min="1" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="remarks">Ghi chú</Label>
            <Input id="remarks" name="remarks" value={formData.remarks} onChange={handleChange} />
          </div>

          <div className="flex items-center space-x-2 mt-4">
            <input 
              type="checkbox" 
              id="status" 
              name="status" 
              checked={formData.status} 
              onChange={handleChange} 
              className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
            />
            <Label htmlFor="status" className="font-normal cursor-pointer">Lớp đang hoạt động</Label>
          </div>

          <div className="flex justify-end pt-4 space-x-2">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Thoát</Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Đang xử lý..." : "Lưu Lớp"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
