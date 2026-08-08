import { Loader2 } from 'lucide-react';
import { Controller } from 'react-hook-form';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

export default function UserForm({
  isModalOpen,
  setIsModalOpen,
  selectedUser,
  form,
  onSubmit,
  roles,
  isPending
}) {
  return (
    <Dialog open={isModalOpen} onOpenChange={setIsModalOpen}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{selectedUser ? 'Sửa thông tin Người dùng' : 'Thêm Người dùng mới'}</DialogTitle>
        </DialogHeader>
        
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 pt-4">
          <div>
            <Label className="mb-2 block">Họ và tên <span className="text-red-500">*</span></Label>
            <Input 
              {...form.register('full_name')}
              placeholder="Nhập họ và tên..."
            />
            {form.formState.errors.full_name && <p className="text-xs text-red-500 mt-1">{form.formState.errors.full_name.message}</p>}
          </div>

          <div>
            <Label className="mb-2 block">Email <span className="text-red-500">*</span></Label>
            <Input 
              {...form.register('email')}
              type="email"
              placeholder="admin@qlsv.edu.vn"
              disabled={!!selectedUser}
            />
            {form.formState.errors.email && <p className="text-xs text-red-500 mt-1">{form.formState.errors.email.message}</p>}
          </div>

          <div>
            <Label className="mb-2 block">Mật khẩu {selectedUser ? '(Để trống nếu không đổi)' : <span className="text-red-500">*</span>}</Label>
            <Input 
              {...form.register('password')}
              type="password"
              placeholder="******"
            />
            {form.formState.errors.password && <p className="text-xs text-red-500 mt-1">{form.formState.errors.password.message}</p>}
          </div>

          <div>
            <Label className="mb-2 block">Vai trò</Label>
            <Controller
              control={form.control}
              name="role_id"
              render={({ field }) => (
                <Select onValueChange={field.onChange} value={field.value || ""} disabled={field.disabled}>
                  <SelectTrigger>
                    <SelectValue placeholder="-- Không chọn vai trò --" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">-- Không chọn vai trò --</SelectItem>
                    {roles.map(r => (
                      <SelectItem key={r.id} value={r.id}>{r.name}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              )}
            />
            {form.formState.errors.role_id && <p className="text-xs text-red-500 mt-1">{form.formState.errors.role_id.message}</p>}
          </div>

          <div className="pt-4 flex items-center justify-end gap-3">
            <Button 
              type="button" 
              variant="outline"
              onClick={() => setIsModalOpen(false)}
            >
              Hủy bỏ
            </Button>
            <Button 
              type="submit" 
              disabled={isPending}
            >
              {isPending && <Loader2 size={16} className="animate-spin mr-2" />}
              {selectedUser ? 'Lưu thay đổi' : 'Tạo Người dùng'}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}
