import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { useCreateAssignment, useUpdateAssignment, useClassrooms, useCourses } from "../features/academics/hooks";
import { useTeachers } from "../features/teachers/hooks";

export default function AssignmentForm({ assignmentToEdit = null, isOpen, setIsOpen }) {
  const createMutation = useCreateAssignment();
  const updateMutation = useUpdateAssignment();

  const { data: classroomsData } = useClassrooms();
  const { data: coursesData } = useCourses();
  const { data: teachersData } = useTeachers();

  const classrooms = Array.isArray(classroomsData) ? classroomsData : classroomsData?.results || [];
  const courses = Array.isArray(coursesData) ? coursesData : coursesData?.results || [];
  const teachers = Array.isArray(teachersData) ? teachersData : teachersData?.results || [];

  const [formData, setFormData] = useState({
    classroom: "",
    course: "",
    teacher: "",
  });

  useEffect(() => {
    if (assignmentToEdit) {
      setFormData({
        classroom: assignmentToEdit.classroom || "",
        course: assignmentToEdit.course || "",
        teacher: assignmentToEdit.teacher || "",
      });
    } else {
      setFormData({ classroom: "", course: "", teacher: "" });
    }
  }, [assignmentToEdit, isOpen]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (assignmentToEdit) {
        await updateMutation.mutateAsync({ id: assignmentToEdit.id, data: formData });
      } else {
        await createMutation.mutateAsync(formData);
      }
      setIsOpen(false);
    } catch (error) {
      console.error("Lỗi khi lưu phân công:", error.response?.data || error.message);
      alert("Đã xảy ra lỗi!\n" + JSON.stringify(error.response?.data));
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{assignmentToEdit ? "Sửa Phân Công" : "Phân Công Giảng Dạy"}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label>Lớp Sinh Hoạt</Label>
            <select 
              name="classroom" 
              value={formData.classroom} 
              onChange={handleChange}
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="" disabled>-- Chọn lớp --</option>
              {classrooms.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label>Học Phần (Môn Học)</Label>
            <select 
              name="course" 
              value={formData.course} 
              onChange={handleChange}
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="" disabled>-- Chọn môn học --</option>
              {courses.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="space-y-2">
            <Label>Giảng Viên Phụ Trách</Label>
            <select 
              name="teacher" 
              value={formData.teacher} 
              onChange={handleChange}
              required
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            >
              <option value="" disabled>-- Chọn giảng viên --</option>
              {teachers.map(t => (
                <option key={t.id} value={t.id}>{t.full_name}</option>
              ))}
            </select>
          </div>

          <div className="flex justify-end pt-4 space-x-2">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Thoát</Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Đang xử lý..." : "Lưu Phân Công"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
