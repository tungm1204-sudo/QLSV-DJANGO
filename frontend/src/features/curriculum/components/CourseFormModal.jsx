import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { courseSchema } from '../validations/courseSchema';

export default function CourseFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  onSubmit, 
  departments = [], 
  courseTypes = [], 
  isLoading = false 
}) {
  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(courseSchema),
    defaultValues: {
      code: '',
      name: '',
      credits: 0,
      theory_credits: 0,
      practical_credits: 0,
      department: '',
      course_type: '',
      is_active: true
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        department: initialData.department_id || initialData.department?.id || (typeof initialData.department === 'string' ? initialData.department : ''),
        course_type: initialData.course_type_id || initialData.course_type?.id || (typeof initialData.course_type === 'string' ? initialData.course_type : ''),
      });
    } else if (isOpen) {
      reset({
        code: '',
        name: '',
        credits: 0,
        theory_credits: 0,
        practical_credits: 0,
        department: '',
        course_type: '',
        is_active: true
      });
    }
  }, [initialData, isOpen, reset]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl md:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Môn học' : 'Thêm mới Môn học'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="code">Mã môn học <span className="text-red-500">*</span></Label>
              <Input id="code" placeholder="VD: CS101" {...register('code')} />
              {errors.code && <p className="text-sm text-red-500">{errors.code.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="name">Tên môn học <span className="text-red-500">*</span></Label>
              <Input id="name" placeholder="VD: Nhập môn Lập trình" {...register('name')} />
              {errors.name && <p className="text-sm text-red-500">{errors.name.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="credits">Tổng tín chỉ <span className="text-red-500">*</span></Label>
              <Input id="credits" type="number" min={0} {...register('credits', { valueAsNumber: true })} />
              {errors.credits && <p className="text-sm text-red-500">{errors.credits.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="theory_credits">Lý thuyết</Label>
              <Input id="theory_credits" type="number" min={0} {...register('theory_credits', { valueAsNumber: true })} />
              {errors.theory_credits && <p className="text-sm text-red-500">{errors.theory_credits.message}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="practical_credits">Thực hành</Label>
              <Input id="practical_credits" type="number" min={0} {...register('practical_credits', { valueAsNumber: true })} />
              {errors.practical_credits && <p className="text-sm text-red-500">{errors.practical_credits.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label>Bộ môn quản lý <span className="text-red-500">*</span></Label>
              <Controller
                name="department"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn bộ môn">
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

            <div className="space-y-2">
              <Label>Loại hình học phần</Label>
              <Controller
                name="course_type"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn loại (tùy chọn)">
                        {field.value
                          ? courseTypes.find(t => t.value === field.value)?.label || field.value
                          : undefined}
                      </SelectValue>
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="">-- Không chọn --</SelectItem>
                      {courseTypes.map((type) => (
                        <SelectItem key={type.value} value={type.value}>{type.label}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                )}
              />
              {errors.course_type && <p className="text-sm text-red-500">{errors.course_type.message}</p>}
            </div>
          </div>

          {initialData && (
            <div className="flex items-center space-x-2 pt-2">
              <input type="checkbox" id="is_active" {...register('is_active')} className="w-4 h-4" />
              <Label htmlFor="is_active" className="cursor-pointer">Hoạt động</Label>
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
