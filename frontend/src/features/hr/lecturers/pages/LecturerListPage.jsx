import React, { useState, useRef } from 'react';
import { Plus, Search, FileDown, FileUp, Filter } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useLecturers, useLecturerMutations, useLecturerImport } from '../hooks/useLecturers';
import { exportLecturersApi } from '../api/lecturerApi';
import LecturerTable from '../components/LecturerTable';

import { usePermissions } from '@/hooks/usePermissions';
import { useDebounce } from '@/hooks/useDebounce';
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
  useDepartmentOptions, 
  useDegreeOptions,
} from '../../../master_data/hooks/useMasterDataOptions';

export default function LecturerListPage() {
  const navigate = useNavigate();
  const { hasPermission } = usePermissions();
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 500);
  const [page, setPage] = useState(1);
  const [deleteConfig, setDeleteConfig] = useState({ isOpen: false, id: null });
  const [isExporting, setIsExporting] = useState(false);
  const fileInputRef = useRef(null);
  
  const [isFilterOpen, setIsFilterOpen] = useState(false);
  const [filters, setFilters] = useState({
    status: '',
    department: '',
    degree: '',
    contract_type: '',
  });
  const [tempFilters, setTempFilters] = useState(filters);
  
  const { data: response, isLoading } = useLecturers({ search: debouncedSearchTerm, page, ...filters });
  const lecturers = response?.results || response || [];
  const { deleteMutation } = useLecturerMutations();
  const importMutation = useLecturerImport();

  const { data: departments = [] } = useDepartmentOptions();
  const { data: degrees = [] } = useDegreeOptions();
  
  // Handlers
  const handleImport = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    
    importMutation.mutate(file, {
      onSettled: () => {
        if (fileInputRef.current) fileInputRef.current.value = '';
      }
    });
  };

  const handleExport = async () => {
    try {
      setIsExporting(true);
      const res = await exportLecturersApi({ search: searchTerm, ...filters });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `danh-sach-giang-vien.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Xuất file thành công');
    } catch (error) {
      toast.error('Có lỗi khi xuất file');
    } finally {
      setIsExporting(false);
    }
  };

  const applyFilters = () => {
    setFilters(tempFilters);
    setIsFilterOpen(false);
  };

  const clearFilters = () => {
    const empty = { status: '', department: '', degree: '', contract_type: '' };
    setTempFilters(empty);
    setFilters(empty);
    setIsFilterOpen(false);
  };

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <Input 
              placeholder="Tìm kiếm theo mã, họ tên, email..." 
              className="pl-9"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        
        <Dialog open={isFilterOpen} onOpenChange={setIsFilterOpen}>
          <DialogTrigger asChild>
            <Button 
              variant="outline" 
              size="icon"
              className="shrink-0 bg-white" 
              title="Bộ lọc nâng cao"
              onClick={() => setTempFilters(filters)}
            >
              <Filter className="h-4 w-4" />
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <DialogHeader>
              <DialogTitle>Bộ lọc giảng viên</DialogTitle>
            </DialogHeader>
            <div className="py-4">
              <div className="grid gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="status">Trạng thái</Label>
                  <Select value={tempFilters.status} onValueChange={(val) => setTempFilters({...tempFilters, status: val})}>
                    <SelectTrigger id="status">
                      <SelectValue placeholder="Tất cả trạng thái">
                        {tempFilters.status === 'ACTIVE' ? 'Đang làm việc' : 
                         tempFilters.status === 'RESIGNED' ? 'Đã nghỉ việc' : 
                         tempFilters.status === 'RETIRED' ? 'Đã nghỉ hưu' : 
                         tempFilters.status === 'SUSPENDED' ? 'Tạm đình chỉ' : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Tất cả</SelectItem>
                      <SelectItem value="ACTIVE">Đang làm việc</SelectItem>
                      <SelectItem value="RESIGNED">Đã nghỉ việc</SelectItem>
                      <SelectItem value="RETIRED">Đã nghỉ hưu</SelectItem>
                      <SelectItem value="SUSPENDED">Tạm đình chỉ</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="grid gap-2">
                  <Label htmlFor="department">Khoa / Bộ môn</Label>
                  <Select value={tempFilters.department} onValueChange={(val) => setTempFilters({...tempFilters, department: val})}>
                    <SelectTrigger id="department">
                      <SelectValue placeholder="Tất cả khoa/bộ môn">
                        {tempFilters.department && departments.find(d => d.value === tempFilters.department) ? departments.find(d => d.value === tempFilters.department).label : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Tất cả</SelectItem>
                      {departments.map(dept => (
                        <SelectItem key={dept.value} value={dept.value}>{dept.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                
                <div className="grid gap-2">
                  <Label htmlFor="degree">Học vị</Label>
                  <Select value={tempFilters.degree} onValueChange={(val) => setTempFilters({...tempFilters, degree: val})}>
                    <SelectTrigger id="degree">
                      <SelectValue placeholder="Tất cả học vị">
                         {tempFilters.degree && degrees.find(d => d.value === tempFilters.degree) ? degrees.find(d => d.value === tempFilters.degree).label : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Tất cả</SelectItem>
                      {degrees.map(deg => (
                        <SelectItem key={deg.value} value={deg.value}>{deg.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="grid gap-2">
                  <Label htmlFor="contract_type">Loại hợp đồng</Label>
                  <Select value={tempFilters.contract_type} onValueChange={(val) => setTempFilters({...tempFilters, contract_type: val})}>
                    <SelectTrigger id="contract_type">
                      <SelectValue placeholder="Tất cả hợp đồng">
                        {tempFilters.contract_type === 'FULL_TIME' ? 'Cơ hữu' : 
                         tempFilters.contract_type === 'VISITING' ? 'Thỉnh giảng' : 
                         tempFilters.contract_type === 'GUEST' ? 'Khách mời' : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">Tất cả</SelectItem>
                      <SelectItem value="FULL_TIME">Cơ hữu</SelectItem>
                      <SelectItem value="VISITING">Thỉnh giảng</SelectItem>
                      <SelectItem value="GUEST">Khách mời</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
            <DialogFooter className="gap-2 sm:gap-0">
              <Button variant="outline" onClick={clearFilters}>Xóa lọc</Button>
              <Button onClick={applyFilters}>Áp dụng</Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
        </div>

        <div className="flex items-center gap-2">
          {/* File input ẩn cho chức năng Import */}
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept=".xlsx, .xls" 
            onChange={handleImport} 
          />
          <Button 
            variant="outline" 
            className="text-slate-600 bg-white" 
            onClick={() => fileInputRef.current?.click()} 
            disabled={importMutation.isPending}
          >
            <FileUp className="h-4 w-4 mr-2" /> 
            {importMutation.isPending ? 'Đang Import...' : 'Import'}
          </Button>
          
          <Button 
            variant="outline" 
            className="text-slate-600 bg-white" 
            onClick={handleExport} 
            disabled={isExporting || isLoading}
          >
            <FileDown className="h-4 w-4 mr-2" /> 
            {isExporting ? 'Đang Export...' : 'Export'}
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white" onClick={() => navigate('/hr/lecturers/new')}>
            <Plus className="h-4 w-4 mr-2" /> Thêm Giảng viên
          </Button>
        </div>
      </div>

      {/* Data Table */}
      <LecturerTable 
        lecturers={lecturers} 
        isLoading={isLoading} 
        canUpdate={true} 
        canDelete={true} 
        setDeleteConfig={setDeleteConfig}
      />

      <ConfirmModal 
        isOpen={deleteConfig.isOpen}
        title="Xóa giảng viên"
        content="Bạn có chắc chắn muốn xóa giảng viên này? Hành động này không thể hoàn tác."
        onConfirm={() => {
          deleteMutation.mutate(deleteConfig.id, {
            onSettled: () => setDeleteConfig({ isOpen: false, id: null })
          });
        }}
        onCancel={() => setDeleteConfig({ isOpen: false, id: null })}
        isLoading={deleteMutation.isPending}
      />
    </div>
  );
}
