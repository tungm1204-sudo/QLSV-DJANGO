import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateTeacher, useUpdateTeacher } from "../features/teachers/hooks";

export default function TeacherForm({ teacherToEdit = null, isOpen, setIsOpen }) {
  const createMutation = useCreateTeacher();
  const updateMutation = useUpdateTeacher();
  
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    mgv: "",
    specialization: "",
    department_id: ""
  });

  useEffect(() => {
    if (teacherToEdit) {
      setFormData({
        username: teacherToEdit.user?.username || "",
        password: "",
        email: teacherToEdit.user?.email || "",
        first_name: teacherToEdit.user?.first_name || "",
        last_name: teacherToEdit.user?.last_name || "",
        mgv: teacherToEdit.mgv || "",
        specialization: teacherToEdit.specialization || "",
        department_id: teacherToEdit.department?.id || ""
      });
    } else {
      setFormData({
        username: "", password: "", email: "", first_name: "", last_name: "",
        mgv: "", specialization: "", department_id: ""
      });
    }
  }, [teacherToEdit, isOpen]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const payload = {
      mgv: formData.mgv,
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      ...(formData.password ? { password: formData.password } : {}),
      specialization: formData.specialization,
      ...(formData.department_id ? { department: parseInt(formData.department_id, 10) } : {})
    };

    try {
      if (teacherToEdit) {
        await updateMutation.mutateAsync({ mgv: teacherToEdit.mgv, data: payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      setIsOpen(false);
    } catch (error) {
      console.error("Lỗi khi lưu giáo viên:", error.response?.data || error.message);
      alert("Đã xảy ra lỗi!\n" + JSON.stringify(error.response?.data));
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{teacherToEdit ? "Sửa Giáo Viên" : "Thêm Giáo Viên"}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <div className="space-y-2">
              <Label>Mã Giáo Viên (MGV)</Label>
              <Input name="mgv" value={formData.mgv} onChange={handleChange} required disabled={!!teacherToEdit} />
            </div>

            <div className="space-y-2">
              <Label>Tên Đăng Nhập</Label>
              <Input name="username" value={formData.username} onChange={handleChange} required disabled={!!teacherToEdit} />
            </div>

            <div className="space-y-2">
              <Label>Mật Khẩu {teacherToEdit && "(Bỏ trống nếu không đổi)"}</Label>
              <Input type="password" name="password" value={formData.password} onChange={handleChange} required={!teacherToEdit} />
            </div>

            <div className="space-y-2">
              <Label>Email</Label>
              <Input type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label>Họ (First Name)</Label>
              <Input name="first_name" value={formData.first_name} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label>Tên (Last Name)</Label>
              <Input name="last_name" value={formData.last_name} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label>Chuyên Môn</Label>
              <Input name="specialization" value={formData.specialization} onChange={handleChange} />
            </div>

            <div className="space-y-2">
              <Label>ID Khoa/Bộ Môn</Label>
              <Input type="number" name="department_id" placeholder="VD: 1" value={formData.department_id} onChange={handleChange} />
              <p className="text-xs text-gray-400">Tạm thời nhập ID hệ thống trực tiếp</p>
            </div>

          </div>

          <div className="flex justify-end pt-4 space-x-2">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Thoát</Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Đang xử lý..." : "Lưu Giáo Viên"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
