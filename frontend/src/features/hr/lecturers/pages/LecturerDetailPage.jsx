import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Award, Briefcase, Plus, Trash2, Printer } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import StatusBadge from '@/components/ui/StatusBadge';
import { useLecturerDetail } from '../hooks/useLecturers';

export default function LecturerDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Lecturer Data
  const { data: lecturer, isLoading: isLoadingLecturer } = useLecturerDetail(id);

  if (isLoadingLecturer) {
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

  if (!lecturer) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-slate-700">Không tìm thấy giảng viên</h2>
        <Button variant="link" onClick={() => navigate('/hr/lecturers')}>Quay lại danh sách</Button>
      </div>
    );
  }

  return (
    <div className="pb-10">
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-4">
          <Button 
            variant="outline" 
            size="icon" 
            onClick={() => navigate('/hr/lecturers')} 
            className="rounded-full bg-white hover:bg-slate-100"
          >
            <ArrowLeft size={18} />
          </Button>
          <div className="flex items-center gap-4">
            <img 
              src={`https://ui-avatars.com/api/?name=${encodeURIComponent(lecturer.user?.full_name || 'GV')}&background=e0e7ff&color=4f46e5&size=64`} 
              alt={lecturer.user?.full_name}
              className="w-16 h-16 rounded-full border-2 border-white shadow-sm"
            />
            <div>
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
                {lecturer.user?.full_name || 'N/A'}
                <StatusBadge status={lecturer.status} />
              </h1>
              <p className="text-sm text-slate-500 mt-1 flex items-center gap-2">
                <span>{lecturer.lecturer_code}</span>
                <span>•</span>
                <span>{lecturer.user?.email}</span>
                <span>•</span>
                <span className="font-medium text-slate-700">{lecturer.department_detail?.name || 'Chưa phân Khoa/Bộ môn'}</span>
              </p>
            </div>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button variant="outline" className="bg-white" onClick={() => navigate(`/hr/lecturers/${id}/edit`)}>
            Cập nhật hồ sơ
          </Button>
        </div>
      </div>

      <Tabs defaultValue="general" className="w-full">
        <TabsList className="bg-white border border-slate-200 p-1 mb-6 rounded-lg w-full justify-start h-auto">
          <TabsTrigger value="general" className="data-[state=active]:bg-slate-100 py-2.5 px-4 rounded-md">
            <User size={16} className="mr-2" /> Thông tin chung
          </TabsTrigger>
          <TabsTrigger value="teaching" disabled className="data-[state=active]:bg-slate-100 py-2.5 px-4 rounded-md opacity-50 cursor-not-allowed">
            <Briefcase size={16} className="mr-2" /> Chuyên môn giảng dạy
          </TabsTrigger>
          <TabsTrigger value="history" disabled className="data-[state=active]:bg-slate-100 py-2.5 px-4 rounded-md opacity-50 cursor-not-allowed">
            <Award size={16} className="mr-2" /> Lịch sử công tác
          </TabsTrigger>
        </TabsList>
        
        {/* Tab 1: General Info */}
        <TabsContent value="general">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Công tác</h3>
              <InfoRow label="Mã giảng viên" value={lecturer.lecturer_code} />
              <InfoRow label="Loại hợp đồng" value={
                lecturer.contract_type === 'FULL_TIME' ? 'Cơ hữu' :
                lecturer.contract_type === 'VISITING' ? 'Thỉnh giảng' :
                lecturer.contract_type === 'GUEST' ? 'Khách mời' : 'Khác'
              } />
              <InfoRow label="Khoa / Bộ môn" value={lecturer.department_detail?.name} />
              <InfoRow label="Học vị" value={lecturer.degree_detail?.name} />
              <InfoRow label="Học hàm" value={lecturer.academic_title_detail?.name} />
              <InfoRow label="Lĩnh vực giảng dạy" value={lecturer.teaching_domain} />
              <InfoRow label="Ngày vào trường" value={lecturer.join_date ? new Date(lecturer.join_date).toLocaleDateString('vi-VN') : 'N/A'} />
              <InfoRow label="Trạng thái" value={
                lecturer.status === 'ACTIVE' ? 'Đang làm việc' : 
                lecturer.status === 'RESIGNED' ? 'Đã nghỉ việc' :
                lecturer.status === 'RETIRED' ? 'Đã nghỉ hưu' :
                lecturer.status === 'SUSPENDED' ? 'Tạm đình chỉ' : 'N/A'
              } />
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Cá nhân</h3>
              <InfoRow label="Ngày sinh" value={lecturer.date_of_birth ? new Date(lecturer.date_of_birth).toLocaleDateString('vi-VN') : 'N/A'} />
              <InfoRow label="Giới tính" value={lecturer.gender === 'MALE' ? 'Nam' : lecturer.gender === 'FEMALE' ? 'Nữ' : lecturer.gender === 'OTHER' ? 'Khác' : 'N/A'} />
              <InfoRow label="Số CMND/CCCD" value={lecturer.id_card_number} />
              <InfoRow label="Nơi sinh" value={lecturer.place_of_birth} />
              <InfoRow label="Dân tộc" value={lecturer.ethnicity_detail?.name} />
              <InfoRow label="Tôn giáo" value={lecturer.religion_detail?.name} />
              <InfoRow label="Quốc tịch" value={lecturer.nationality_detail?.name} />
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Liên hệ</h3>
              <InfoRow label="SĐT di động" value={lecturer.contact_phone} />
              <InfoRow label="Email cá nhân" value={lecturer.personal_email} />
              <InfoRow label="Địa chỉ" value={lecturer.address} />
              <InfoRow label="Tài khoản ngân hàng" value={lecturer.bank_account} />
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex flex-col sm:flex-row sm:justify-between py-1 border-b border-slate-100 last:border-0">
      <span className="text-sm text-slate-500">{label}</span>
      <span className="text-sm font-medium text-slate-900 text-right">{value || <span className="text-slate-400 font-normal">N/A</span>}</span>
    </div>
  );
}
