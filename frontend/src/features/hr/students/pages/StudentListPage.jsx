import React, { useState, useRef } from 'react';
import { Plus, Search, FileDown, FileUp, Filter } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useStudents, useStudentMutations, useStudentImport } from '../hooks/useStudents';
import { exportStudentsApi } from '../api/studentApi';
import StudentTable from '../components/StudentTable';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import ConfirmModal from '@/components/ui/ConfirmModal';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogFooter,
} from '@/components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { 
  useMajorOptions, 
  useAdministrativeClassOptions,
  useEducationSystemOptions
} from '../../../master_data/hooks/useMasterDataOptions';

export default function StudentListPage() {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });
  const [isExporting, setIsExporting] = useState(false);
  const fileInputRef = useRef(null);
  
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [filters, setFilters] = useState({
    status: '',
    major: '',
    administrative_class: '',
    education_system: '',
  });
  const [tempFilters, setTempFilters] = useState(filters);
  
  const { data: response, isLoading } = useStudents({ search: searchTerm, ...filters });
  const students = response?.results || response || [];
  const { deleteMutation } = useStudentMutations();
  const importMutation = useStudentImport();

  const { data: majors = [] } = useMajorOptions();
  const { data: classes = [] } = useAdministrativeClassOptions();
  const { data: eduSystems = [] } = useEducationSystemOptions();
  
  // Handlers
  const handlePrintIdCard = (id) => {
    // Implement print
    console.log("Print ID card for", id);
  };

  const handleImport = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    importMutation.mutate(file, {
      onSettled: () => {
        // Reset file input để có thể import lại cùng 1 file nếu cần
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    });
  };

  const handleExport = async () => {
    try {
      setIsExporting(true);
      const res = await exportStudentsApi({ search: searchTerm, ...filters });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'students.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Xuất file thành công');
    } catch (error) {
      toast.error('Có lỗi xảy ra khi xuất file');
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="space-y-4">
      {/* HrTableToolbar - Chúng ta sẽ tách ra sau, giờ build inline cho nhanh */}
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <Input 
              placeholder="Tìm theo MSSV, Tên, Email..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9"
            />
          </div>
            <Dialog open={isFilterOpen} onOpenChange={setIsFilterOpen}>
              <DialogTrigger asChild>
                <Button 
                  variant="outline" 
                  size="icon" 
                  className="shrink-0" 
                  title="Bộ lọc nâng cao"
                  onClick={() => setTempFilters(filters)}
                >
                  <Filter className="h-4 w-4" />
                </Button>
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                  <DialogTitle>Lọc sinh viên</DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="status">Trạng thái</Label>
                    <Select value={tempFilters.status} onValueChange={(val) => setTempFilters({...tempFilters, status: val})}>
                      <SelectTrigger id="status">
                        <SelectValue placeholder="Tất cả trạng thái">
                          {tempFilters.status === 'ACTIVE' ? 'Đang học' : tempFilters.status === 'PAUSED' ? 'Bảo lưu' : tempFilters.status === 'GRADUATED' ? 'Đã tốt nghiệp' : tempFilters.status === 'DROPPED_OUT' ? 'Thôi học' : undefined}
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Tất cả trạng thái</SelectItem>
                        <SelectItem value="ACTIVE">Đang học</SelectItem>
                        <SelectItem value="PAUSED">Bảo lưu</SelectItem>
                        <SelectItem value="GRADUATED">Đã tốt nghiệp</SelectItem>
                        <SelectItem value="DROPPED_OUT">Thôi học</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div className="grid gap-2">
                    <Label htmlFor="major">Ngành học</Label>
                    <Select value={tempFilters.major} onValueChange={(val) => setTempFilters({...tempFilters, major: val})}>
                      <SelectTrigger id="major">
                        <SelectValue placeholder="Tất cả ngành học">
                          {tempFilters.major && majors.find(m => m.value === tempFilters.major) ? majors.find(m => m.value === tempFilters.major).label : undefined}
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Tất cả ngành học</SelectItem>
                        {majors.map(m => (
                          <SelectItem key={m.value} value={m.value}>{m.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="class">Lớp hành chính</Label>
                    <Select value={tempFilters.administrative_class} onValueChange={(val) => setTempFilters({...tempFilters, administrative_class: val})}>
                      <SelectTrigger id="class">
                        <SelectValue placeholder="Tất cả lớp">
                          {tempFilters.administrative_class && classes.find(c => c.value === tempFilters.administrative_class) ? classes.find(c => c.value === tempFilters.administrative_class).label : undefined}
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Tất cả lớp</SelectItem>
                        {classes.map(c => (
                          <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="eduSystem">Hệ đào tạo</Label>
                    <Select value={tempFilters.education_system} onValueChange={(val) => setTempFilters({...tempFilters, education_system: val})}>
                      <SelectTrigger id="eduSystem">
                        <SelectValue placeholder="Tất cả hệ đào tạo">
                          {tempFilters.education_system && eduSystems.find(e => e.value === tempFilters.education_system) ? eduSystems.find(e => e.value === tempFilters.education_system).label : undefined}
                        </SelectValue>
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="">Tất cả hệ đào tạo</SelectItem>
                        {eduSystems.map(e => (
                          <SelectItem key={e.value} value={e.value}>{e.label}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>
                <DialogFooter>
                  <Button 
                    variant="outline" 
                    onClick={() => setTempFilters({ status: '', major: '', administrative_class: '', education_system: '' })}
                  >
                    Xóa lọc
                  </Button>
                  <Button onClick={() => { setFilters(tempFilters); setIsFilterOpen(false); }}>
                    Áp dụng
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        
        <div className="flex items-center gap-2">
          {/* File input ẩn cho chức năng Import */}
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleImport} 
            accept=".xlsx, .xls" 
            className="hidden" 
          />
          <Button 
            variant="outline" 
            className="text-slate-600"
            onClick={() => fileInputRef.current?.click()}
            disabled={importMutation.isPending}
          >
            <FileUp className="h-4 w-4 mr-2" /> 
            {importMutation.isPending ? 'Đang Import...' : 'Import'}
          </Button>
          
          <Button 
            variant="outline" 
            className="text-slate-600"
            onClick={handleExport}
            disabled={isExporting || isLoading}
          >
            <FileDown className="h-4 w-4 mr-2" /> 
            {isExporting ? 'Đang Export...' : 'Export'}
          </Button>
          
          <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => navigate('/hr/students/new')}>
            <Plus className="h-4 w-4 mr-2" /> Thêm Sinh viên
          </Button>
        </div>
      </div>

      <StudentTable 
        students={students}
        isLoading={isLoading}
        canUpdate={true} // Tạm hardcode để test UI
        canDelete={true} // Tạm hardcode để test UI
        handlePrintIdCard={handlePrintIdCard}
        setDeleteConfig={setDeleteConfig}
      />

      <ConfirmModal 
        isOpen={deleteConfig.isOpen}
        title="Xóa sinh viên"
        content="Bạn có chắc chắn muốn xóa sinh viên này? Tất cả dữ liệu liên quan (chứng chỉ, điểm...) cũng sẽ bị xóa và không thể khôi phục."
        onConfirm={() => deleteMutation.mutate(deleteConfig.id, {
          onSuccess: () => setDeleteConfig({ isOpen: false, id: null })
        })}
        onCancel={() => setDeleteConfig({ isOpen: false, id: null })}
        isLoading={deleteMutation.isPending}
      />
    </div>
  );
}
