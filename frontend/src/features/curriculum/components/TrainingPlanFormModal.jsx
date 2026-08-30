import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { trainingPlanSchema } from '../validations/trainingPlanSchema';

export default function TrainingPlanFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  onSubmit, 
  semesters = [], 
  departments = [], 
  isLoading = false 
}) {
  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(trainingPlanSchema),
    defaultValues: {
      name: '',
      semester: '',
      department: '',
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        semester: initialData.semester_id || initialData.semester?.id || (typeof initialData.semester === 'string' ? initialData.semester : ''),
        department: initialData.department_id || initialData.department?.id || (typeof initialData.department === 'string' ? initialData.department : ''),
      });
    } else if (isOpen) {
      reset({
        name: '',
        semester: '',
        department: '',
      });
    }
  }, [initialData, isOpen, reset]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Kế hoạch đào tạo' : 'Thêm mới Kế hoạch đào tạo'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label htmlFor="name">Tên kế hoạch <span className="text-red-500">*</span></Label>
            <Input id="name" placeholder="VD: Kế hoạch đào tạo HK1 (2024-2025) Khoa CNTT" {...register('name')} />
            {errors.name && <p className="text-sm text-red-500">{errors.name.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Học kỳ <span className="text-red-500">*</span></Label>
              <Controller
                name="semester"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn học kỳ">
                        {field.value 
                          ? semesters.find(s => s.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {semesters.map((sem) => (
                        <SelectItem key={sem.value} value={sem.value}>{sem.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.semester && <p className="text-sm text-red-500">{errors.semester.message}</p>}
            </div>

            <div className="space-y-2">
              <Label>Khoa quản lý <span className="text-red-500">*</span></Label>
              <Controller
                name="department"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn khoa">
                        {field.value 
                          ? departments.find(d => d.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {departments.map((dept) => (
                        <SelectItem key={dept.value} value={dept.value}>{dept.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.department && <p className="text-sm text-red-500">{errors.department.message}</p>}
            </div>
          </div>

          <DialogFooter className="mt-6">
            <Button type="button" variant="outline" onClick={onClose} disabled={isLoading}>
              Hủy
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? 'Đang lưu...' : (initialData ? 'Lưu thay đổi' : 'Thêm mới')}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
