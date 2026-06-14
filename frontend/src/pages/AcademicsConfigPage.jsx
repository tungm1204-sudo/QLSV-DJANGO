import { useState } from "react";
import {
  useSemesters, useCreateSemester, useUpdateSemester, useDeleteSemester,
  useGrades, useCreateGrade, useUpdateGrade, useDeleteGrade,
  useExamTypes, useCreateExamType, useUpdateExamType, useDeleteExamType,
} from "../features/academics/hooks";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import {
  Table, TableBody, TableCell, TableHead,
  TableHeader, TableRow
} from "@/components/ui/table";
import { Plus, Edit, Trash2, CalendarDays, GraduationCap, BookOpen, CheckCircle2, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";

// ─── Generic Confirm Delete ───────────────────────────────────────────────────
function useConfirmDelete(mutationHook) {
  const mutation = mutationHook();
  const handleDelete = (id, label) => {
    if (window.confirm(`Xóa "${label}"? Hành động này không thể hoàn tác.`)) {
      mutation.mutate(id);
    }
  };
  return { handleDelete, isPending: mutation.isPending };
}

// ─── SEMESTER SECTION ─────────────────────────────────────────────────────────
function SemesterSection() {
  const { data, isLoading } = useSemesters();
  const createMutation = useCreateSemester();
  const updateMutation = useUpdateSemester();
  const { handleDelete } = useConfirmDelete(useDeleteSemester);

  const semesters = Array.isArray(data) ? data : data?.results || [];

  const [isOpen, setIsOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: "", academic_year: "", start_date: "", end_date: "", is_current: false });

  const openCreate = () => {
    setEditing(null);
    setForm({ name: "", academic_year: "", start_date: "", end_date: "", is_current: false });
    setIsOpen(true);
  };

  const openEdit = (s) => {
    setEditing(s);
    setForm({ name: s.name, academic_year: s.academic_year, start_date: s.start_date, end_date: s.end_date, is_current: s.is_current });
    setIsOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await updateMutation.mutateAsync({ id: editing.id, data: form });
      } else {
        await createMutation.mutateAsync(form);
      }
      setIsOpen(false);
    } catch (err) {
      alert("Lỗi: " + JSON.stringify(err.response?.data));
    }
  };

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold">Học Kỳ</h2>
          <p className="text-sm text-muted-foreground">Quản lý các học kỳ trong năm học.</p>
        </div>
        <Button size="sm" onClick={openCreate}><Plus className="mr-2 h-4 w-4" /> Thêm Học Kỳ</Button>
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>{editing ? "Sửa Học Kỳ" : "Thêm Học Kỳ"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 py-2">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Tên học kỳ</Label>
                <Input required placeholder="HK1" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
              </div>
              <div className="space-y-2">
                <Label>Năm học</Label>
                <Input required placeholder="2024-2025" value={form.academic_year} onChange={e => setForm(p => ({ ...p, academic_year: e.target.value }))} />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Ngày bắt đầu</Label>
                <Input type="date" required value={form.start_date} onChange={e => setForm(p => ({ ...p, start_date: e.target.value }))} />
              </div>
              <div className="space-y-2">
                <Label>Ngày kết thúc</Label>
                <Input type="date" required value={form.end_date} onChange={e => setForm(p => ({ ...p, end_date: e.target.value }))} />
              </div>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="is_current"
                checked={form.is_current}
                onChange={e => setForm(p => ({ ...p, is_current: e.target.checked }))}
                className="w-4 h-4"
              />
              <Label htmlFor="is_current">Đây là học kỳ hiện tại</Label>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Hủy</Button>
              <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Đang lưu..." : "Lưu"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Tên Học Kỳ</TableHead>
              <TableHead>Năm Học</TableHead>
              <TableHead>Thời Gian</TableHead>
              <TableHead className="text-center">Hiện Tại</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={5} className="text-center h-16">Đang tải...</TableCell></TableRow>
            ) : semesters.length === 0 ? (
              <TableRow><TableCell colSpan={5} className="text-center h-16 text-muted-foreground">Chưa có học kỳ nào.</TableCell></TableRow>
            ) : semesters.map(s => (
              <TableRow key={s.id} className="hover:bg-muted/30">
                <TableCell className="font-semibold">{s.name}</TableCell>
                <TableCell>
                  <Badge variant="outline">{s.academic_year}</Badge>
                </TableCell>
                <TableCell className="text-sm text-muted-foreground">
                  {s.start_date} → {s.end_date}
                </TableCell>
                <TableCell className="text-center">
                  {s.is_current
                    ? <CheckCircle2 className="h-5 w-5 text-green-500 mx-auto" />
                    : <XCircle className="h-5 w-5 text-gray-300 mx-auto" />
                  }
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600" onClick={() => openEdit(s)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600" onClick={() => handleDelete(s.id, s.name)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

// ─── GRADE SECTION ────────────────────────────────────────────────────────────
function GradeSection() {
  const { data, isLoading } = useGrades();
  const createMutation = useCreateGrade();
  const updateMutation = useUpdateGrade();
  const { handleDelete } = useConfirmDelete(useDeleteGrade);

  const grades = Array.isArray(data) ? data : data?.results || [];

  const [isOpen, setIsOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: "", description: "" });

  const openCreate = () => {
    setEditing(null);
    setForm({ name: "", description: "" });
    setIsOpen(true);
  };

  const openEdit = (g) => {
    setEditing(g);
    setForm({ name: g.name, description: g.description || "" });
    setIsOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await updateMutation.mutateAsync({ id: editing.id, data: form });
      } else {
        await createMutation.mutateAsync(form);
      }
      setIsOpen(false);
    } catch (err) {
      alert("Lỗi: " + JSON.stringify(err.response?.data));
    }
  };

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold">Khóa / Năm Học</h2>
          <p className="text-sm text-muted-foreground">Quản lý các khóa sinh viên (K20, K21...).</p>
        </div>
        <Button size="sm" onClick={openCreate}><Plus className="mr-2 h-4 w-4" /> Thêm Khóa</Button>
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>{editing ? "Sửa Khóa" : "Thêm Khóa"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 py-2">
            <div className="space-y-2">
              <Label>Tên Khóa</Label>
              <Input required placeholder="K20 / Năm 1..." value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
            </div>
            <div className="space-y-2">
              <Label>Mô tả</Label>
              <Input placeholder="Mô tả thêm..." value={form.description} onChange={e => setForm(p => ({ ...p, description: e.target.value }))} />
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Hủy</Button>
              <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Đang lưu..." : "Lưu"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Tên Khóa</TableHead>
              <TableHead>Mô Tả</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={3} className="text-center h-16">Đang tải...</TableCell></TableRow>
            ) : grades.length === 0 ? (
              <TableRow><TableCell colSpan={3} className="text-center h-16 text-muted-foreground">Chưa có khóa nào.</TableCell></TableRow>
            ) : grades.map(g => (
              <TableRow key={g.id} className="hover:bg-muted/30">
                <TableCell className="font-semibold">{g.name}</TableCell>
                <TableCell className="text-sm text-muted-foreground">{g.description || "—"}</TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600" onClick={() => openEdit(g)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600" onClick={() => handleDelete(g.id, g.name)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

// ─── EXAM TYPE SECTION ────────────────────────────────────────────────────────
function ExamTypeSection() {
  const { data, isLoading } = useExamTypes();
  const createMutation = useCreateExamType();
  const updateMutation = useUpdateExamType();
  const { handleDelete } = useConfirmDelete(useDeleteExamType);

  const examTypes = Array.isArray(data) ? data : data?.results || [];

  const [isOpen, setIsOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: "", weight: 1.0 });

  const openCreate = () => {
    setEditing(null);
    setForm({ name: "", weight: 1.0 });
    setIsOpen(true);
  };

  const openEdit = (t) => {
    setEditing(t);
    setForm({ name: t.name, weight: t.weight });
    setIsOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await updateMutation.mutateAsync({ id: editing.id, data: form });
      } else {
        await createMutation.mutateAsync(form);
      }
      setIsOpen(false);
    } catch (err) {
      alert("Lỗi: " + JSON.stringify(err.response?.data));
    }
  };

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold">Loại Kỳ Thi</h2>
          <p className="text-sm text-muted-foreground">Quản lý loại bài thi và hệ số điểm (Giữa kỳ, Cuối kỳ...).</p>
        </div>
        <Button size="sm" onClick={openCreate}><Plus className="mr-2 h-4 w-4" /> Thêm Loại</Button>
      </div>

      <Dialog open={isOpen} onOpenChange={setIsOpen}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle>{editing ? "Sửa Loại Kỳ Thi" : "Thêm Loại Kỳ Thi"}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 py-2">
            <div className="space-y-2">
              <Label>Tên loại</Label>
              <Input required placeholder="Cuối kỳ" value={form.name} onChange={e => setForm(p => ({ ...p, name: e.target.value }))} />
            </div>
            <div className="space-y-2">
              <Label>Hệ số (0.0 → 1.0)</Label>
              <Input type="number" required min="0" max="1" step="0.1" value={form.weight}
                onChange={e => setForm(p => ({ ...p, weight: parseFloat(e.target.value) }))} />
              <p className="text-xs text-muted-foreground">Ví dụ: Giữa kỳ = 0.4, Cuối kỳ = 0.6</p>
            </div>
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="outline" onClick={() => setIsOpen(false)}>Hủy</Button>
              <Button type="submit" disabled={isSubmitting}>{isSubmitting ? "Đang lưu..." : "Lưu"}</Button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      <div className="border rounded-lg bg-white shadow-sm overflow-hidden">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
              <TableHead>Tên Loại</TableHead>
              <TableHead className="text-center">Hệ Số</TableHead>
              <TableHead className="text-right">Thao tác</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={3} className="text-center h-16">Đang tải...</TableCell></TableRow>
            ) : examTypes.length === 0 ? (
              <TableRow><TableCell colSpan={3} className="text-center h-16 text-muted-foreground">Chưa có loại kỳ thi nào.</TableCell></TableRow>
            ) : examTypes.map(t => (
              <TableRow key={t.id} className="hover:bg-muted/30">
                <TableCell className="font-semibold">{t.name}</TableCell>
                <TableCell className="text-center">
                  <Badge className="bg-purple-100 text-purple-700 border-purple-200">{t.weight}x</Badge>
                </TableCell>
                <TableCell className="text-right">
                  <div className="flex justify-end gap-1">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600" onClick={() => openEdit(t)}>
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-red-600" onClick={() => handleDelete(t.id, t.name)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}

// ─── MAIN PAGE ────────────────────────────────────────────────────────────────
const TABS = [
  { id: "semesters", label: "Học Kỳ", icon: CalendarDays },
  { id: "grades",    label: "Khóa / Năm Học", icon: GraduationCap },
  { id: "examtypes", label: "Loại Kỳ Thi", icon: BookOpen },
];

export default function AcademicsConfigPage() {
  const [activeTab, setActiveTab] = useState("semesters");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Cấu Hình Hệ Thống</h1>
        <p className="text-muted-foreground">Quản lý dữ liệu nền tảng: Học kỳ, Khóa sinh viên và Loại kỳ thi.</p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-gray-200">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-gray-700 hover:border-gray-300"
            }`}
          >
            <tab.icon className="h-4 w-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div>
        {activeTab === "semesters" && <SemesterSection />}
        {activeTab === "grades"    && <GradeSection />}
        {activeTab === "examtypes" && <ExamTypeSection />}
      </div>
    </div>
  );
}
