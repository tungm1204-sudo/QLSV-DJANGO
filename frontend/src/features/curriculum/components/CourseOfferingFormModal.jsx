import { useEffect, useState } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { courseOfferingSchema } from '../validations/courseOfferingSchema';
import apiClient from '@/api/client';

export default function CourseOfferingFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  onSubmit, 
  isLoading = false 
}) {
  const [courses, setCourses] = useState([]);
  const [lecturers, setLecturers] = useState([]);
  const [isFetchingOptions, setIsFetchingOptions] = useState(false);

  useEffect(() => {
    if (isOpen) {
      const fetchOptions = async () => {
        setIsFetchingOptions(true);
        try {
          const [courseRes, lecturerRes] = await Promise.all([
            apiClient.get('/curriculum/course/', { params: { page_size: 1000, is_active: true } }),
            apiClient.get('/hr/lecturer/', { params: { page_size: 1000 } })
          ]);
          setCourses(courseRes.data.results || courseRes.data || []);
          setLecturers(lecturerRes.data.results || lecturerRes.data || []);
        } catch (error) {
          console.error('Failed to fetch options', error);
        } finally {
          setIsFetchingOptions(false);
        }
      };
      fetchOptions();
    }
  }, [isOpen]);

  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(courseOfferingSchema),
    defaultValues: {
      course: '',
      lecturer: '',
      min_capacity: 10,
      max_capacity: 50,
      status: 'PLANNED',
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        course: initialData.course_id || initialData.course?.id || (typeof initialData.course === 'string' ? initialData.course : ''),
        lecturer: initialData.lecturer_id || initialData.lecturer?.id || (typeof initialData.lecturer === 'string' ? initialData.lecturer : ''),
      });
    } else if (isOpen) {
      reset({
        course: '',
        lecturer: '',
        min_capacity: 10,
        max_capacity: 50,
        status: 'PLANNED',
      });
    }
  }, [initialData, isOpen, reset]);

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Lớp học phần' : 'Thêm mới Lớp học phần'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label>Môn học <span className="text-red-500">*</span></Label>
            <Controller
              name="course"
              control={control}
              render={({ field }) => (
                <Select onValueChange={field.onChange} value={field.value || ""}>
                  <SelectTrigger disabled={isFetchingOptions || !!initialData}>
                    <SelectValue placeholder="Chọn môn học" />
                  </SelectTrigger>
                  <SelectContent>
                    {courses.map((c) => (
                      <SelectItem key={c.id} value={c.id}>{c.code} - {c.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.course && <p className="text-sm text-red-500">{errors.course.message}</p>}
          </div>

          <div className="space-y-2">
            <Label>Giảng viên phụ trách</Label>
            <Controller
              name="lecturer"
              control={control}
              render={({ field }) => (
                <Select onValueChange={field.onChange} value={field.value || ""}>
                  <SelectTrigger disabled={isFetchingOptions}>
                    <SelectValue placeholder="Chưa phân công" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">-- Chưa phân công --</SelectItem>
                    {lecturers.map((l) => (
                      <SelectItem key={l.id} value={l.id}>
                         {l.user?.last_name} {l.user?.first_name} ({l.employee_id})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.lecturer && <p className="text-sm text-red-500">{errors.lecturer.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="min_capacity">Sức chứa tối thiểu <span className="text-red-500">*</span></Label>
              <Input id="min_capacity" type="number" min={1} {...register('min_capacity', { valueAsNumber: true })} />
              {errors.min_capacity && <p className="text-sm text-red-500">{errors.min_capacity.message}</p>}
            </div>
            <div className="space-y-2">
              <Label htmlFor="max_capacity">Sức chứa tối đa <span className="text-red-500">*</span></Label>
              <Input id="max_capacity" type="number" min={1} {...register('max_capacity', { valueAsNumber: true })} />
              {errors.max_capacity && <p className="text-sm text-red-500">{errors.max_capacity.message}</p>}
            </div>
          </div>
          
          {initialData && (
            <div className="space-y-2">
              <Label>Trạng thái</Label>
              <Controller
                name="status"
                control={control}
                render={({ field }) => (
                  <Select onValueChange={field.onChange} value={field.value || ""}>
                    <SelectTrigger>
                      <SelectValue placeholder="Chọn trạng thái" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="PLANNED">Theo kế hoạch</SelectItem>
                      <SelectItem value="OPEN">Mở đăng ký</SelectItem>
                      <SelectItem value="CLOSED">Đóng đăng ký</SelectItem>
                      <SelectItem value="CANCELLED">Đã hủy</SelectItem>
                    </SelectContent>
                  </Select>
                )}
              />
            </div>
          )}

          <DialogFooter className="mt-6">
            <Button type="button" variant="outline" onClick={onClose} disabled={isLoading}>
              Hủy
            </Button>
            <Button type="submit" disabled={isLoading || isFetchingOptions}>
              {isLoading ? 'Đang lưu...' : (initialData ? 'Lưu thay đổi' : 'Thêm mới')}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
