import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { trainingProgramSchema } from '../validations/trainingProgramSchema';

export default function TrainingProgramFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  onSubmit, 
  majors = [],
  specializations = [],
  cohorts = [],
  isLoading = false 
}) {
  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(trainingProgramSchema),
    defaultValues: {
      code: '',
      name: '',
      major: '',
      specialization: null,
      cohort: '',
      total_credits: 120,
      is_active: true
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        major: initialData.major_id || initialData.major?.id || (typeof initialData.major === 'string' ? initialData.major : ''),
        specialization: initialData.specialization_id || initialData.specialization?.id || (typeof initialData.specialization === 'string' ? initialData.specialization : null),
        cohort: initialData.cohort_id || initialData.cohort?.id || (typeof initialData.cohort === 'string' ? initialData.cohort : ''),
      });
    } else if (isOpen) {
      reset({
        code: '',
        name: '',
        major: '',
        specialization: null,
        cohort: '',
        total_credits: 120,
        is_active: true
      });
    }
  }, [initialData, isOpen, reset]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl md:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Chương trình đào tạo' : 'Thêm mới Chương trình đào tạo'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="code">Mã chương trình <span className="text-red-500">*</span></Label>
              <Input id="code" placeholder="VD: TP-IT-K24" {...register('code')} />
              {errors.code && <p className="text-sm text-red-500">{errors.code.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="name">Tên chương trình <span className="text-red-500">*</span></Label>
              <Input id="name" placeholder="VD: Kỹ sư Công nghệ thông tin K24" {...register('name')} />
              {errors.name && <p className="text-sm text-red-500">{errors.name.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Ngành học <span className="text-red-500">*</span></Label>
              <Controller
                name="major"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn ngành học">
                        {field.value 
                          ? majors.find(m => m.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {majors.map((item) => (
                        <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.major && <p className="text-sm text-red-500">{errors.major.message}</p>}
            </div>

            <div className="space-y-2">
              <Label>Chuyên ngành</Label>
              <Controller
                name="specialization"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn chuyên ngành (tùy chọn)">
                        {field.value
                          ? specializations.find(s => s.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">-- Không chọn --</SelectItem>
                      {specializations.map((item) => (
                        <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.specialization && <p className="text-sm text-red-500">{errors.specialization.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Khóa học <span className="text-red-500">*</span></Label>
              <Controller
                name="cohort"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn khóa học">
                        {field.value 
                          ? cohorts.find(c => c.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      {cohorts.map((item) => (
                        <SelectItem key={item.value} value={item.value}>{item.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.cohort && <p className="text-sm text-red-500">{errors.cohort.message}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="total_credits">Tổng tín chỉ <span className="text-red-500">*</span></Label>
              <Input id="total_credits" type="number" min={1} {...register('total_credits', { valueAsNumber: true })} />
              {errors.total_credits && <p className="text-sm text-red-500">{errors.total_credits.message}</p>}
            </div>
          </div>

          {initialData && (
            <div className="flex items-center space-x-2 pt-2">
              <input type="checkbox" id="is_active" {...register('is_active')} className="w-4 h-4" />
              <Label htmlFor="is_active" className="cursor-pointer">Trạng thái Hoạt động</Label>
            </div>
          )}

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
