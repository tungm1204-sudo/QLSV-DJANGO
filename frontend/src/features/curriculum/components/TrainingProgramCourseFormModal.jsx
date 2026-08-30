import { useEffect } from 'react';
import { useForm, Controller } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { zodResolver } from '@hookform/resolvers/zod';
import { trainingProgramCourseSchema } from '../validations/trainingProgramCourseSchema';
import { useCourses } from '../hooks/useCourses';

export default function TrainingProgramCourseFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  trainingProgramId,
  knowledgeBlockId,
  onSubmit, 
  isLoading = false 
}) {
  const { data: coursesData } = useCourses({ page_size: 1000, is_active: true });
  const courses = coursesData?.results || coursesData || [];

  const { register, handleSubmit, reset, control, formState: { errors } } = useForm({
    resolver: zodResolver(trainingProgramCourseSchema),
    defaultValues: {
      course: '',
      semester_expected: 1,
      is_mandatory: true,
      notes: ''
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        knowledge_block: initialData.knowledge_block_id || initialData.knowledge_block?.id || (typeof initialData.knowledge_block === 'string' ? initialData.knowledge_block : ''),
        course: initialData.course?.id || (typeof initialData.course === 'string' ? initialData.course : '') || '',
        notes: initialData.notes || ''
      });
    } else if (isOpen) {
      reset({
        course: '',
        semester_expected: 1,
        is_mandatory: true,
        notes: ''
      });
    }
  }, [initialData, isOpen, reset]);

  const handleFormSubmit = (data) => {
    onSubmit({
      ...data,
      training_program: trainingProgramId,
      knowledge_block: knowledgeBlockId
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl md:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Học phần' : 'Thêm mới Học phần'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 py-4">
          <div className="space-y-2">
            <Label>Học phần <span className="text-red-500">*</span></Label>
            <Controller
              name="course"
              control={control}
              render={({ field }) => (
                <Select onValueChange={field.onChange} value={field.value || ""}>
                  <SelectTrigger>
                    <SelectValue placeholder="Chọn học phần">
                      {field.value 
                        ? courses.find(c => c.id === field.value)?.name || field.value
                        : undefined}
                    </SelectValue>
                  </SelectTrigger>
                  <SelectContent>
                    {courses.map((item) => (
                      <SelectItem key={item.id} value={item.id}>
                        {item.code} - {item.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {errors.course && <p className="text-sm text-red-500">{errors.course.message}</p>}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="semester_expected">Học kỳ dự kiến <span className="text-red-500">*</span></Label>
              <Input id="semester_expected" type="number" min={1} {...register('semester_expected', { valueAsNumber: true })} />
              {errors.semester_expected && <p className="text-sm text-red-500">{errors.semester_expected.message}</p>}
            </div>
            
            <div className="space-y-2 flex flex-col justify-center">
              <Label className="mb-3">Loại</Label>
              <div className="flex items-center space-x-4">
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input type="radio" value="true" {...register('is_mandatory')} className="w-4 h-4" defaultChecked={true} />
                  <span>Bắt buộc</span>
                </label>
                <label className="flex items-center space-x-2 cursor-pointer">
                  <input type="radio" value="false" {...register('is_mandatory')} className="w-4 h-4" />
                  <span>Tự chọn</span>
                </label>
              </div>
              {errors.is_mandatory && <p className="text-sm text-red-500">{errors.is_mandatory.message}</p>}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Ghi chú</Label>
            <Input id="notes" placeholder="Ghi chú thêm..." {...register('notes')} />
            {errors.notes && <p className="text-sm text-red-500">{errors.notes.message}</p>}
          </div>

          <DialogFooter className="mt-6">
            <Button type="button" variant="outline" onClick={onClose} disabled={isLoading}>
              Hủy
            </Button>
            <Button type="submit" disabled={isLoading} className="bg-indigo-600 hover:bg-indigo-700">
              {isLoading ? 'Đang lưu...' : (initialData ? 'Lưu thay đổi' : 'Thêm mới')}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
