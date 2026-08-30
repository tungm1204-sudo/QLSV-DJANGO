import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { zodResolver } from '@hookform/resolvers/zod';
import { knowledgeBlockSchema } from '../validations/knowledgeBlockSchema';

export default function KnowledgeBlockFormModal({ 
  isOpen, 
  onClose, 
  initialData = null, 
  trainingProgramId,
  onSubmit, 
  isLoading = false 
}) {
  const { register, handleSubmit, reset, formState: { errors } } = useForm({
    resolver: zodResolver(knowledgeBlockSchema),
    defaultValues: {
      code: '',
      name: '',
      mandatory_credits: 0,
      elective_credits: 0,
      order: 1,
      notes: ''
    }
  });

  useEffect(() => {
    if (initialData && isOpen) {
      reset({
        ...initialData,
        notes: initialData.notes || ''
      });
    } else if (isOpen) {
      reset({
        code: '',
        name: '',
        mandatory_credits: 0,
        elective_credits: 0,
        order: 1,
        notes: ''
      });
    }
  }, [initialData, isOpen, reset]);

  const handleFormSubmit = (data) => {
    onSubmit({
      ...data,
      training_program: trainingProgramId
    });
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="sm:max-w-2xl md:max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{initialData ? 'Cập nhật Khối kiến thức' : 'Thêm mới Khối kiến thức'}</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 py-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="code">Mã khối <span className="text-red-500">*</span></Label>
              <Input id="code" placeholder="VD: K1-DAICUONG" {...register('code')} />
              {errors.code && <p className="text-sm text-red-500">{errors.code.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="name">Tên khối <span className="text-red-500">*</span></Label>
              <Input id="name" placeholder="VD: Khối kiến thức đại cương" {...register('name')} />
              {errors.name && <p className="text-sm text-red-500">{errors.name.message}</p>}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="mandatory_credits">TC bắt buộc <span className="text-red-500">*</span></Label>
              <Input id="mandatory_credits" type="number" min={0} {...register('mandatory_credits', { valueAsNumber: true })} />
              {errors.mandatory_credits && <p className="text-sm text-red-500">{errors.mandatory_credits.message}</p>}
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="elective_credits">TC tự chọn <span className="text-red-500">*</span></Label>
              <Input id="elective_credits" type="number" min={0} {...register('elective_credits', { valueAsNumber: true })} />
              {errors.elective_credits && <p className="text-sm text-red-500">{errors.elective_credits.message}</p>}
            </div>

            <div className="space-y-2">
              <Label htmlFor="order">Thứ tự hiển thị <span className="text-red-500">*</span></Label>
              <Input id="order" type="number" min={1} {...register('order', { valueAsNumber: true })} />
              {errors.order && <p className="text-sm text-red-500">{errors.order.message}</p>}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Ghi chú</Label>
            <Textarea id="notes" placeholder="Ghi chú thêm..." {...register('notes')} />
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
