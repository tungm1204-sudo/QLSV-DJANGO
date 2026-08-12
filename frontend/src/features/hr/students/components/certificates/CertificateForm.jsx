import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { studentCertificateSchema } from '../../validations/studentCertificateSchema';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export default function CertificateForm({ isOpen, onClose, initialData, studentId, onSubmit, isLoading }) {
  const form = useForm({
    resolver: zodResolver(studentCertificateSchema),
    defaultValues: initialData || {
      student: studentId,
      certificate_type: '',
      certificate_name: '',
      issue_date: '',
      expiration_date: '',
      score: '',
      provider: '',
      status: 'PENDING'
    }
  });

  const { register, handleSubmit, formState: { errors }, setValue, watch, reset } = form;
  const [file, setFile] = useState(null);

  React.useEffect(() => {
    if (isOpen) {
      if (initialData) {
        reset(initialData);
      } else {
        reset({ student: studentId, status: 'PENDING', certificate_type: '', certificate_name: '', issue_date: '', expiration_date: '', score: '', provider: '' });
      }
      setFile(null);
    }
  }, [isOpen, initialData, reset, studentId]);

  const handleFormSubmit = (data) => {
    const payload = { ...data };
    Object.keys(payload).forEach(key => {
      if (payload[key] === '') payload[key] = null;
    });
    if (file) {
      payload.file_proof = file;
    }
    onSubmit(payload);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Chứng chỉ' : 'Thêm Chứng chỉ mới'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="certificate_type" className="after:content-['*'] after:ml-0.5 after:text-red-500">Loại chứng chỉ</Label>
              <Select value={watch('certificate_type') || ''} onValueChange={(val) => setValue('certificate_type', val)}>
                <SelectTrigger id="certificate_type">
                  <SelectValue placeholder="Chọn loại chứng chỉ" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="NGOAI_NGU">Ngoại ngữ</SelectItem>
                  <SelectItem value="TIN_HOC">Tin học</SelectItem>
                  <SelectItem value="GDQP">Giáo dục quốc phòng</SelectItem>
                  <SelectItem value="GDTX">Giáo dục thể chất</SelectItem>
                  <SelectItem value="KHAC">Khác</SelectItem>
                </SelectContent>
              </Select>
              {errors.certificate_type && <p className="text-sm text-red-500">{errors.certificate_type.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="certificate_name" className="after:content-['*'] after:ml-0.5 after:text-red-500">Tên chứng chỉ</Label>
              <Input id="certificate_name" {...register('certificate_name')} placeholder="VD: TOEIC 600" />
              {errors.certificate_name && <p className="text-sm text-red-500">{errors.certificate_name.message}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="issue_date" className="after:content-['*'] after:ml-0.5 after:text-red-500">Ngày cấp</Label>
              <Input id="issue_date" type="date" {...register('issue_date')} />
              {errors.issue_date && <p className="text-sm text-red-500">{errors.issue_date.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="expiration_date">Ngày hết hạn (Nếu có)</Label>
              <Input id="expiration_date" type="date" {...register('expiration_date')} />
            </div>

            <div className="space-y-2">
              <Label htmlFor="score">Điểm số / Xếp loại</Label>
              <Input id="score" {...register('score')} placeholder="VD: 650, Khá..." />
            </div>

            <div className="space-y-2">
              <Label htmlFor="provider">Tổ chức cấp</Label>
              <Input id="provider" {...register('provider')} placeholder="VD: IIG Vietnam" />
            </div>

            <div className="space-y-2">
              <Label htmlFor="status">Trạng thái</Label>
              <Select value={watch('status') || ''} onValueChange={(val) => setValue('status', val)}>
                <SelectTrigger id="status">
                  <SelectValue placeholder="Trạng thái duyệt" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="PENDING">Chờ duyệt</SelectItem>
                  <SelectItem value="APPROVED">Đã duyệt</SelectItem>
                  <SelectItem value="REJECTED">Từ chối</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label htmlFor="file_proof">File minh chứng (Ảnh/PDF)</Label>
              <Input 
                id="file_proof" 
                type="file" 
                accept=".jpg,.jpeg,.png,.pdf"
                onChange={(e) => setFile(e.target.files[0])} 
              />
              {initialData?.file_proof && !file && (
                <p className="text-sm text-blue-600 truncate mt-1">
                  Đã tải lên: {initialData.file_proof.split('/').pop()}
                </p>
              )}
            </div>
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t">
            <Button type="button" variant="outline" onClick={onClose}>Hủy</Button>
            <Button type="submit" disabled={isLoading}>{isLoading ? 'Đang lưu...' : initialData ? 'Cập nhật' : 'Thêm mới'}</Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
