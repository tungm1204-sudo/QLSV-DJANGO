import { useState, useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateStudent, useUpdateStudent } from "../features/students/hooks";

export default function StudentForm({ studentToEdit = null, isOpen, setIsOpen }) {
  const createMutation = useCreateStudent();
  const updateMutation = useUpdateStudent();
  
  const [formData, setFormData] = useState({
    username: "",
    password: "",
    email: "",
    first_name: "",
    last_name: "",
    mssv: "",
    dob: "",
    gender: "male",
    address: "",
    phone: "",
    parent_name: "",
    parent_phone: ""
  });

  useEffect(() => {
    if (studentToEdit) {
      setFormData({
        username: studentToEdit.user?.username || "",
        password: "", // Leave blank on edit unless changing
        email: studentToEdit.user?.email || "",
        first_name: studentToEdit.user?.first_name || "",
        last_name: studentToEdit.user?.last_name || "",
        mssv: studentToEdit.mssv || "",
        dob: studentToEdit.dob || "",
        gender: studentToEdit.gender || "male",
        address: studentToEdit.address || "",
        phone: studentToEdit.phone || "",
        parent_name: studentToEdit.parent?.full_name || "",
        parent_phone: studentToEdit.parent?.phone || "",
      });
    } else {
      setFormData({
        username: "", password: "", email: "", first_name: "", last_name: "",
        mssv: "", dob: "", gender: "male", address: "", phone: "",
        parent_name: "", parent_phone: ""
      });
    }
  }, [studentToEdit, isOpen]);

  const handleChange = (e) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Map flat form to DRF StudentCreateSerializer format
    const payload = {
      mssv: formData.mssv,
      first_name: formData.first_name,
      last_name: formData.last_name,
      email: formData.email,
      ...(formData.password ? { password: formData.password } : {}),
      dob: formData.dob || null,
      gender: formData.gender,
      address: formData.address,
      phone: formData.phone,
    };

    try {
      if (studentToEdit) {
        await updateMutation.mutateAsync({ mssv: studentToEdit.mssv, data: payload });
      } else {
        await createMutation.mutateAsync(payload);
      }
      setIsOpen(false);
    } catch (error) {
      console.error("Lỗi khi lưu sinh viên:", error.response?.data || error.message);
      alert("Đã xảy ra lỗi!\n" + JSON.stringify(error.response?.data));
    }
  };

  const isLoading = createMutation.isPending || updateMutation.isPending;

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{studentToEdit ? "Sửa Sinh Viên" : "Thêm Sinh Viên"}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={handleSubmit} className="space-y-4 py-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            <div className="space-y-2">
              <Label htmlFor="mssv">Mã số sinh viên (MSSV)</Label>
              <Input id="mssv" name="mssv" value={formData.mssv} onChange={handleChange} required disabled={!!studentToEdit} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="username">Tên Đăng Nhập</Label>
              <Input id="username" name="username" value={formData.username} onChange={handleChange} required disabled={!!studentToEdit} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Mật Khẩu {studentToEdit && "(Bỏ trống nếu không đổi)"}</Label>
              <Input id="password" type="password" name="password" value={formData.password} onChange={handleChange} required={!studentToEdit} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" name="email" value={formData.email} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="first_name">Họ & Tên đệm</Label>
              <Input id="first_name" name="first_name" value={formData.first_name} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="last_name">Tên</Label>
              <Input id="last_name" name="last_name" value={formData.last_name} onChange={handleChange} required />
            </div>

            <div className="space-y-2">
              <Label htmlFor="dob">Ngày Sinh</Label>
              <Input id="dob" type="date" name="dob" value={formData.dob} onChange={handleChange} />
            </div>

            <div className="space-y-2">
              <Label>Giới Tính</Label>
              <select 
                name="gender" 
                value={formData.gender} 
                onChange={handleChange}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
              >
                <option value="male">Nam</option>
                <option value="female">Nữ</option>
                <option value="other">Khác</option>
              </select>
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="phone">Số Điện Thoại</Label>
              <Input id="phone" name="phone" value={formData.phone} onChange={handleChange} />
            </div>
            
            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="address">Địa Chỉ</Label>
              <Input id="address" name="address" value={formData.address} onChange={handleChange} />
            </div>

            {/* Liên hệ khẩn cấp */}
            <div className="space-y-2 mt-4 pt-4 border-t col-span-1 md:col-span-2">
              <h3 className="text-sm font-semibold text-gray-500 uppercase">Thông tin liên hệ khẩn cấp</h3>
            </div>
            <div className="space-y-2">
              <Label htmlFor="parent_name">Tên Người Liên Hệ</Label>
              <Input id="parent_name" name="parent_name" value={formData.parent_name} onChange={handleChange} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="parent_phone">SĐT Người Liên Hệ</Label>
              <Input id="parent_phone" name="parent_phone" value={formData.parent_phone} onChange={handleChange} />
            </div>

          </div>

          <div className="flex justify-end pt-4 space-x-2">
            <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Thoát</Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Đang xử lý..." : "Lưu Sinh Viên"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
