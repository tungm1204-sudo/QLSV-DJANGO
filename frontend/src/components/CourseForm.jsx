import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateCourse, useUpdateCourse, useGrades } from "../features/academics/hooks";

export default function CourseForm({ courseToEdit = null, isOpen, setIsOpen }) {
  const createMutation = useCreateCourse();
  const updateMutation = useUpdateCourse();
  const { data: gradesData } = useGrades();

  const grades = Array.isArray(gradesData) ? gradesData : gradesData?.results || [];
  
  const [formData, setFormData] = useState({
    code: "",
    name: "",
    grade: "",
    credits: 3,
    description: "",
  });

  useEffect(() => {
    if (courseToEdit) {
      setFormData({
        code: courseToEdit.code || "",
        name: courseToEdit.name || "",
        grade: courseToEdit.grade || "",
        credits: courseToEdit.credits || 3,
        description: courseToEdit.description || "",
      });
    } else {
      setFormData({
        code: "", name: "", grade: "", credits: 3, description: ""
      });
    }
  }, [courseToEdit, isOpen]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (courseToEdit) {
        await updateMutation.mutateAsync({ id: courseToEdit.id, data: formData });
      } else {
        await createMutation.mutateAsync(formData);
      }
      setIsOpen(false);
    } catch (error) {
      console.error("Lỗi khi lưu môn học:", error.response?.data || error.message);
      alert("Đã xảy ra lỗi!\n" + JSON.stringify(error.response?.data));
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-md max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{courseToEdit ? "Sửa Môn Học" : "Thêm Môn Học"}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="code">Mã Môn</Label>
            <Input id="code" name="code" value={formData.code} onChange={handleChange} required />
          </div>

          <div className="space-y-2">
            <Label htmlFor="name">Tên Môn Học</Label>
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
            <Label htmlFor="credits">Số Tín Chỉ</Label>
            <Input id="credits" type="number" name="credits" value={formData.credits} onChange={handleChange} required min="1" max="10" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">Mô tả</Label>
            <Input id="description" name="description" value={formData.description} onChange={handleChange} />
          </div>

          <div className="flex justify-end pt-4 space-x-2">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Thoát</Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Đang xử lý..." : "Lưu Môn Học"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
