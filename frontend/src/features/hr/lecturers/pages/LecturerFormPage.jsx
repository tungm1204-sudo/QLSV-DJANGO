import React, { useEffect, useState } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import LecturerForm from '../components/LecturerForm';
import { useLecturerDetail, useLecturerMutations } from '../hooks/useLecturers';

export default function LecturerFormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isEditMode = location.pathname.includes('/edit');

  const { data: lecturerDetail, isLoading: isLoadingDetail } = useLecturerDetail(isEditMode ? id : null);
  
  const handleSuccess = () => {
    if (isEditMode) {
      navigate(`/hr/lecturers/${id}`);
    } else {
      navigate('/hr/lecturers');
    }
  };

  const { createMutation, updateMutation } = useLecturerMutations(handleSuccess);

  const handleSubmit = (data) => {
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

  let initialData = undefined;
  if (isEditMode && lecturerDetail) {
    initialData = {
      ...lecturerDetail,
      full_name: lecturerDetail.user?.full_name || '',
      email: lecturerDetail.user?.email || '',
      department: lecturerDetail.department || lecturerDetail.department_detail?.id || null,
      degree: lecturerDetail.degree || lecturerDetail.degree_detail?.id || null,
      academic_title: lecturerDetail.academic_title || lecturerDetail.academic_title_detail?.id || null,
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
            {isEditMode ? 'Cập nhật Giảng viên' : 'Thêm mới Giảng viên'}
          </h1>
          <p className="text-sm text-slate-500">
            {isEditMode ? `Đang chỉnh sửa hồ sơ giảng viên ${lecturerDetail?.lecturer_code || ''}` : 'Nhập thông tin hồ sơ giảng viên mới vào hệ thống'}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
        <LecturerForm 
          initialData={initialData}
          onSubmit={handleSubmit}
          onCancel={() => navigate(-1)}
          isLoading={isSubmitting}
        />
      </div>
    </div>
  );
}
