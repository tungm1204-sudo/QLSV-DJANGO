import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StudentForm from '../components/StudentForm';
import { useStudentDetail, useStudentMutations } from '../hooks/useStudents';

export default function StudentFormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isEditMode = location.pathname.includes('/edit');

  const { data: studentDetail, isLoading: isLoadingDetail } = useStudentDetail(isEditMode ? id : null);
  
  const handleSuccess = () => {
    // Quay về danh sách hoặc trang chi tiết tùy ngữ cảnh
    if (isEditMode) {
      navigate(`/hr/students/${id}`);
    } else {
      navigate('/hr/students');
    }
  };

  const { createMutation, updateMutation } = useStudentMutations(handleSuccess);

  const handleSubmit = (data) => {
    // Chuẩn bị dữ liệu gửi đi: loại bỏ các chuỗi rỗng để thành null cho FK nếu cần
    const payload = { ...data };
    Object.keys(payload).forEach(key => {
      if (payload[key] === '') payload[key] = null;
    });

    if (isEditMode) {
      updateMutation.mutate({ id, data: payload });
    } else {
      createMutation.mutate(payload);
    }
  };

  const isSubmitting = createMutation.isPending || updateMutation.isPending;

  if (isEditMode && isLoadingDetail) {
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

  // Tiền xử lý initialData (trải data từ API ra form)
  let initialData = undefined;
  if (isEditMode && studentDetail) {
    initialData = {
      ...studentDetail,
      // Flatten nested user object if it exists (tuỳ theo API trả về ntn)
      full_name: studentDetail.user?.full_name || '',
      email: studentDetail.user?.email || '',
      // Extract IDs for FK fields if API returns detail objects instead of UUIDs
      major: studentDetail.major || studentDetail.major_detail?.id || null,
      administrative_class: studentDetail.administrative_class || studentDetail.administrative_class_detail?.id || null,
      // Có thể cần map tương tự cho các field khác tuỳ thuộc vào ReadSerializer backend
    };
  }

  return (
    <div className="pb-10">
      <div className="flex items-center gap-4 mb-6">
        <Button 
          variant="outline" 
          size="icon" 
          onClick={() => navigate(-1)} 
          className="rounded-full bg-white hover:bg-slate-100"
        >
          <ArrowLeft size={18} />
        </Button>
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            {isEditMode ? 'Cập nhật Sinh viên' : 'Thêm mới Sinh viên'}
          </h1>
          <p className="text-sm text-slate-500">
            {isEditMode ? `Đang chỉnh sửa hồ sơ sinh viên ${studentDetail?.student_code || ''}` : 'Nhập thông tin hồ sơ sinh viên mới vào hệ thống'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <StudentForm 
          initialData={initialData}
          onSubmit={handleSubmit}
          onCancel={() => navigate(-1)}
          isLoading={isSubmitting}
        />
      </div>
    </div>
  );
}
