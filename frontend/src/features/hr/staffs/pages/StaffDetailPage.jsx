import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, User, Award, Briefcase, Plus, Trash2, Printer } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import StatusBadge from '@/components/ui/StatusBadge';
import { useStaffDetail } from '../hooks/useStaffs';

export default function StaffDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  // Staff Data
  const { data: staff, isLoading: isLoadingStaff } = useStaffDetail(id);

  if (isLoadingStaff) {
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

  if (!staff) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-semibold text-slate-700">Không tìm thấy cán bộ/nhân viên</h2>
        <Button variant="link" onClick={() => navigate('/hr/staffs')}>Quay lại danh sách</Button>
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
            onClick={() => navigate('/hr/staffs')} 
            className="rounded-full bg-white hover:bg-slate-100"
          >
            <ArrowLeft size={18} />
          </Button>
          <div className="flex items-center gap-4">
            <img 
              src={`https://ui-avatars.com/api/?name=${encodeURIComponent(staff.user?.full_name || 'NV')}&background=e0e7ff&color=4f46e5&size=64`} 
              alt={staff.user?.full_name}
              className="w-16 h-16 rounded-full border-2 border-white shadow-sm"
            />
            <div>
              <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
                {staff.user?.full_name || 'N/A'}
                <StatusBadge status={staff.status} />
              </h1>
              <p className="text-sm text-slate-500 mt-1 flex items-center gap-2">
                <span>{staff.staff_code}</span>
                <span>•</span>
                <span>{staff.user?.email}</span>
                <span>•</span>
                <span className="font-medium text-slate-700">{staff.department_detail?.name || 'Chưa phân Phòng ban'}</span>
              </p>
            </div>
          </div>
        </div>
        
        <div className="flex gap-2">
          <Button onClick={() => navigate(`/hr/staffs/${id}/edit`)}>
            Cập nhật hồ sơ
          </Button>
        </div>
      </div>

      <Tabs defaultValue="general" className="w-full">
        <TabsList className="grid w-full grid-cols-2 max-w-[400px] mb-6">
          <TabsTrigger value="general" className="flex gap-2">
            <User size={16} /> Thông tin chung
          </TabsTrigger>
          <TabsTrigger value="history" disabled className="flex gap-2">
            <Award size={16} /> Lịch sử công tác
          </TabsTrigger>
        </TabsList>
        
        {/* Tab 1: General Info */}
        <TabsContent value="general">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Công tác</h3>
              <InfoRow label="Mã Cán bộ/NV" value={staff.staff_code} />
              <InfoRow label="Phòng ban" value={staff.department_detail?.name} />
              <InfoRow label="Trình độ" value={staff.degree_detail?.name} />
              <InfoRow label="Chức vụ" value={staff.position_detail?.name} />
              <InfoRow label="Nhiệm vụ phụ trách" value={staff.responsibilities} />
              <InfoRow label="Ngày vào trường" value={staff.join_date ? new Date(staff.join_date).toLocaleDateString('vi-VN') : 'N/A'} />
              <InfoRow label="Trạng thái" value={
                staff.status === 'ACTIVE' ? 'Đang làm việc' : 
                staff.status === 'RESIGNED' ? 'Đã nghỉ việc' :
                staff.status === 'RETIRED' ? 'Đã nghỉ hưu' :
                staff.status === 'SUSPENDED' ? 'Tạm đình chỉ' : 'N/A'
              } />
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Cá nhân</h3>
              <InfoRow label="Ngày sinh" value={staff.date_of_birth ? new Date(staff.date_of_birth).toLocaleDateString('vi-VN') : 'N/A'} />
              <InfoRow label="Giới tính" value={staff.gender === 'MALE' ? 'Nam' : staff.gender === 'FEMALE' ? 'Nữ' : staff.gender === 'OTHER' ? 'Khác' : 'N/A'} />
              <InfoRow label="Số CMND/CCCD" value={staff.id_card_number} />
              <InfoRow label="Nơi sinh" value={staff.place_of_birth} />
              <InfoRow label="Dân tộc" value={staff.ethnicity_detail?.name} />
              <InfoRow label="Tôn giáo" value={staff.religion_detail?.name} />
              <InfoRow label="Quốc tịch" value={staff.nationality_detail?.name} />
            </div>

            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
              <h3 className="font-semibold text-slate-900 border-b pb-2 mb-4">Thông tin Liên hệ</h3>
              <InfoRow label="SĐT di động" value={staff.contact_phone} />
              <InfoRow label="Email cá nhân" value={staff.personal_email} />
              <InfoRow label="Địa chỉ" value={staff.address} />
              <InfoRow label="Tài khoản ngân hàng" value={staff.bank_account} />
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
