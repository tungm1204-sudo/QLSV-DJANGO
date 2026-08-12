import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Award, Plus, Trash2, Printer } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import StatusBadge from '@/components/ui/StatusBadge';
import { useStudentDetail } from '../hooks/useStudents';
import { useStudentCertificates, useCertificateMutations } from '../hooks/useStudentCertificates';
import CertificateTable from '../components/certificates/CertificateTable';
import CertificateForm from '../components/certificates/CertificateForm';
import ConfirmModal from '../../../../components/ui/ConfirmModal';

export default function StudentDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Student Data
  const { data: student, isLoading: isLoadingStudent } = useStudentDetail(id);

  // Certificate Data
  const { data: certResponse, isLoading: isLoadingCertificates } = useStudentCertificates(id);
  const certificates = certResponse?.results || certResponse || [];
  
  // Certificate Modals State
  const [isCertFormOpen, setIsCertFormOpen] = useState(false);
  const [editingCert, setEditingCert] = useState(null);
  const [deleteCertId, setDeleteCertId] = useState(null);

  // Mutations
  const { createMutation, updateMutation, deleteMutation } = useCertificateMutations(id, () => {
    setIsCertFormOpen(false);
    setEditingCert(null);
    setDeleteCertId(null);
  });

  const handleCertSubmit = (data) => {
    if (editingCert) {
      updateMutation.mutate({ id: editingCert.id, data });
    } else {
      createMutation.mutate(data);
    }
  };

  const openEditCert = (cert) => {
    setEditingCert(cert);
    setIsCertFormOpen(true);
  };

  const openCreateCert = () => {
    setEditingCert(null);
    setIsCertFormOpen(true);
  };

  if (isLoadingStudent) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-4">
          <Skeleton className="h-10 w-10 rounded-full" />
          <Skeleton className="h-8 w-64" />
        </div>
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (!student) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-slate-700">Không tìm thấy sinh viên</h2>
        <Button variant="link" onClick={() => navigate('/hr/students')}>Quay lại danh sách</Button>
      </div>
    );
  }

  return (
    <div className="pb-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-4">
          <Button 
            variant="outline" size="icon" onClick={() => navigate('/hr/students')} 
            className="rounded-full bg-white hover:bg-slate-100 shrink-0"
          >
            <ArrowLeft size={18} />
          </Button>
          <div className="flex items-center gap-4">
            <img 
              src={`https://ui-avatars.com/api/?name=${encodeURIComponent(student.user?.full_name || 'SV')}&size=64&background=e0e7ff&color=4f46e5`} 
              alt={student.user?.full_name} 
              className="w-16 h-16 rounded-full border-2 border-white shadow-sm object-cover"
            />
            <div>
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
                {student.user?.full_name}
                <StatusBadge status={student.status} />
              </h1>
              <p className="text-sm text-slate-500 mt-1 flex items-center gap-2">
                <span className="font-medium text-slate-700">{student.student_code}</span> 
                &bull; {student.user?.email || 'Chưa có email'}
              </p>
            </div>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button variant="outline" className="bg-white" onClick={() => console.log('Print ID', student.id)}>
            <Printer size={16} className="mr-2" /> In thẻ
          </Button>
          <Button onClick={() => navigate(`/hr/students/${student.id}/edit`)}>
            Cập nhật hồ sơ
          </Button>
        </div>
      </div>

      {/* Tabs Layout */}
      <Tabs defaultValue="general" className="w-full">
        <TabsList className="grid w-full grid-cols-3 max-w-[600px] mb-6">
          <TabsTrigger value="general" className="flex gap-2"><User size={16}/> Thông tin chung</TabsTrigger>
          <TabsTrigger value="certificates" className="flex gap-2"><Award size={16}/> Chứng chỉ & Giải thưởng</TabsTrigger>
          <TabsTrigger value="academic" disabled className="flex gap-2">Lịch sử học tập</TabsTrigger>
        </TabsList>
        
        {/* Tab 1: General Info */}
        <TabsContent value="general">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2">Thông tin Đào tạo</h3>
              <div className="space-y-3">
                <div><span className="text-sm text-slate-500 block">Mã sinh viên</span><span className="font-medium">{student.student_code || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Trạng thái</span><span className="font-medium">
                  {student.status === 'ACTIVE' ? 'Đang học' : student.status === 'PAUSED' ? 'Bảo lưu' : student.status === 'GRADUATED' ? 'Đã tốt nghiệp' : student.status === 'DROPPED_OUT' ? 'Thôi học' : 'N/A'}
                </span></div>
                <div><span className="text-sm text-slate-500 block">Ngành học</span><span className="font-medium">{student.major_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Lớp hành chính</span><span className="font-medium">{student.administrative_class_detail?.name || student.administrative_class_code || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Hệ đào tạo</span><span className="font-medium">{student.education_system_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Loại hình tuyển sinh</span><span className="font-medium">{student.admission_type_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Khóa học</span><span className="font-medium">{student.cohort_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Ngày nhập học</span><span className="font-medium">{student.enrollment_date || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Đối tượng ưu tiên</span><span className="font-medium">{student.priority_category_detail?.name || 'N/A'}</span></div>
              </div>
            </div>

            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2">Nhân khẩu học</h3>
              <div className="space-y-3">
                <div><span className="text-sm text-slate-500 block">Ngày sinh</span><span className="font-medium">{student.date_of_birth || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Giới tính</span><span className="font-medium">
                  {student.gender === 'MALE' ? 'Nam' : student.gender === 'FEMALE' ? 'Nữ' : student.gender === 'OTHER' ? 'Khác' : 'N/A'}
                </span></div>
                <div><span className="text-sm text-slate-500 block">Số CMND/CCCD</span><span className="font-medium">{student.id_card_number || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Nơi sinh</span><span className="font-medium">{student.place_of_birth || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Dân tộc</span><span className="font-medium">{student.ethnicity_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Tôn giáo</span><span className="font-medium">{student.religion_detail?.name || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Quốc tịch</span><span className="font-medium">{student.nationality_detail?.name || 'N/A'}</span></div>
              </div>
            </div>

            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2">Liên lạc</h3>
              <div className="space-y-3">
                <div><span className="text-sm text-slate-500 block">SĐT liên hệ</span><span className="font-medium">{student.contact_phone || 'N/A'}</span></div>
                <div><span className="text-sm text-slate-500 block">Email cá nhân</span><span className="font-medium">{student.personal_email || 'N/A'}</span></div>
                <div className="col-span-full"><span className="text-sm text-slate-500 block">Địa chỉ</span><span className="font-medium">{student.address || 'N/A'}</span></div>
              </div>
            </div>
          </div>
        </TabsContent>

        {/* Tab 2: Certificates */}
        <TabsContent value="certificates">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">Quản lý Chứng chỉ</h3>
                <p className="text-sm text-slate-500">Các chứng chỉ phục vụ xét chuẩn đầu ra và tốt nghiệp</p>
              </div>
              <Button onClick={openCreateCert} className="bg-blue-600 hover:bg-blue-700">
                <Plus size={16} className="mr-2"/> Thêm chứng chỉ
              </Button>
            </div>

            <CertificateTable 
              certificates={certificates} 
              isLoading={isLoadingCertificates}
              canUpdate={true}
              canDelete={true}
              onEdit={openEditCert}
              onDelete={setDeleteCertId}
            />
          </div>
        </TabsContent>
      </Tabs>

      {/* Modals */}
      <CertificateForm 
        isOpen={isCertFormOpen}
        onClose={() => setIsCertFormOpen(false)}
        initialData={editingCert}
        studentId={student.id}
        onSubmit={handleCertSubmit}
        isLoading={createMutation.isPending || updateMutation.isPending}
      />

      <ConfirmModal 
        isOpen={!!deleteCertId}
        title="Xóa chứng chỉ"
        content="Bạn có chắc chắn muốn xóa chứng chỉ này? Hành động này không thể hoàn tác."
        onConfirm={() => deleteMutation.mutate(deleteCertId)}
        onCancel={() => setDeleteCertId(null)}
        isLoading={deleteMutation.isPending}
      />
    </div>
  );
}
