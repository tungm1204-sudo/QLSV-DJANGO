import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { staffSchema } from '../validations/staffSchema';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  useDepartmentOptions,
  useDegreeOptions,
  usePositionOptions,
  useEthnicityOptions,
  useReligionOptions,
  useNationalityOptions
} from '../../../master_data/hooks/useMasterDataOptions';

export default function StaffForm({ initialData, onSubmit, onCancel, isLoading }) {
  const form = useForm({
    resolver: zodResolver(staffSchema),
    defaultValues: initialData || {
      email: '', password: '', full_name: '',
      staff_code: '', department: null, degree: null,
      position: null, responsibilities: '',
      join_date: '', status: 'ACTIVE',
      date_of_birth: '', gender: '', place_of_birth: '',
      ethnicity: null, religion: null, nationality: null, id_card_number: '',
      personal_email: '', contact_phone: '', address: '',
      bank_account: ''
    }
  });

  const { register, handleSubmit, formState: { errors }, setValue, watch } = form;

  // Master Data hooks
  const { data: departments = [] } = useDepartmentOptions();
  const { data: degrees = [] } = useDegreeOptions();
  const { data: positions = [] } = usePositionOptions();
  const { data: ethnicities = [] } = useEthnicityOptions();
  const { data: religions = [] } = useReligionOptions();
  const { data: nationalities = [] } = useNationalityOptions();

  // Helper for rendering select
  const renderSelect = (name, label, options, required = false) => (
    <div className="space-y-2">
      <Label htmlFor={name} className={required ? "after:content-['*'] after:ml-0.5 after:text-red-500" : ""}>
        {label}
      </Label>
      <Select
        key={options.length}
        value={watch(name) || ''}
        onValueChange={(val) => setValue(name, val, { shouldValidate: true })}
      >
        <SelectTrigger id={name} className={errors[name] ? "border-red-500" : ""}>
          <SelectValue placeholder={`Chọn ${label.toLowerCase()}`}>
            {watch(name) && options.find(opt => opt.value === watch(name)) ? 
              (() => {
                const opt = options.find(o => o.value === watch(name));
                return `${opt.label} ${opt.code ? `(${opt.code})` : ''}`;
              })() : undefined
            }
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="">-- Không chọn --</SelectItem>
          {options.map(opt => (
            <SelectItem key={opt.value} value={opt.value}>
              {opt.label} {opt.code ? `(${opt.code})` : ''}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {errors[name] && <p className="text-sm text-red-500">{errors[name]?.message}</p>}
    </div>
  );

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
      {/* Section 1: Thông tin tài khoản */}
      <section className="bg-slate-50/50 p-6 rounded-xl border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">1. Thông tin Tài khoản</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <Label htmlFor="full_name">Họ và tên</Label>
            <Input id="full_name" {...register('full_name')} className={errors.full_name ? "border-red-500" : ""} />
            {errors.full_name && <p className="text-sm text-red-500">{errors.full_name.message}</p>}
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email trường cấp</Label>
            <Input id="email" type="email" {...register('email')} />
            {errors.email && <p className="text-sm text-red-500">{errors.email.message}</p>}
          </div>
          {!initialData && (
            <div className="space-y-2">
              <Label htmlFor="password">Mật khẩu khởi tạo</Label>
              <Input id="password" type="password" {...register('password')} />
              {errors.password && <p className="text-sm text-red-500">{errors.password.message}</p>}
            </div>
          )}
        </div>
      </section>

      {/* Section 2: Thông tin công tác */}
      <section className="bg-slate-50/50 p-6 rounded-xl border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">2. Thông tin Công tác & Chuyên môn</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <Label htmlFor="staff_code" className="after:content-['*'] after:ml-0.5 after:text-red-500">Mã Cán bộ/Nhân viên</Label>
            <Input id="staff_code" {...register('staff_code')} className={errors.staff_code ? "border-red-500" : ""} />
            {errors.staff_code && <p className="text-sm text-red-500">{errors.staff_code.message}</p>}
          </div>
          
          {renderSelect('department', 'Đơn vị / Phòng ban', departments, true)}
          {renderSelect('position', 'Chức vụ', positions)}
          {renderSelect('degree', 'Trình độ / Học vị', degrees)}
          
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="responsibilities">Nhiệm vụ phụ trách</Label>
            <Input id="responsibilities" {...register('responsibilities')} placeholder="Ví dụ: Phụ trách giáo vụ khoa CNTT" />
          </div>

          <div className="space-y-2">
            <Label htmlFor="join_date">Ngày vào trường</Label>
            <Input id="join_date" type="date" {...register('join_date')} />
          </div>

          <div className="space-y-2">
            <Label htmlFor="status" className="after:content-['*'] after:ml-0.5 after:text-red-500">Trạng thái</Label>
            <Select value={watch('status')} onValueChange={(val) => setValue('status', val, { shouldValidate: true })}>
              <SelectTrigger id="status" className={errors.status ? "border-red-500" : ""}>
                <SelectValue placeholder="Trạng thái làm việc">
                  {
                    watch('status') === 'ACTIVE' ? 'Đang làm việc' :
                    watch('status') === 'RESIGNED' ? 'Đã nghỉ việc' :
                    watch('status') === 'RETIRED' ? 'Đã nghỉ hưu' :
                    watch('status') === 'SUSPENDED' ? 'Tạm đình chỉ' : undefined
                  }
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ACTIVE">Đang làm việc</SelectItem>
                <SelectItem value="RESIGNED">Đã nghỉ việc</SelectItem>
                <SelectItem value="RETIRED">Đã nghỉ hưu</SelectItem>
                <SelectItem value="SUSPENDED">Tạm đình chỉ</SelectItem>
              </SelectContent>
            </Select>
            {errors.status && <p className="text-sm text-red-500">{errors.status?.message}</p>}
          </div>
        </div>
      </section>

      {/* Section 3: Nhân khẩu học */}
      <section className="bg-slate-50/50 p-6 rounded-xl border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">3. Nhân khẩu học & Cá nhân</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <Label htmlFor="date_of_birth">Ngày sinh</Label>
            <Input id="date_of_birth" type="date" {...register('date_of_birth')} />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="gender">Giới tính</Label>
            <Select value={watch('gender') || ''} onValueChange={(val) => setValue('gender', val)}>
              <SelectTrigger id="gender">
                <SelectValue placeholder="Chọn giới tính">
                  {
                    watch('gender') === 'MALE' ? 'Nam' :
                    watch('gender') === 'FEMALE' ? 'Nữ' :
                    watch('gender') === 'OTHER' ? 'Khác' : undefined
                  }
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">-- Không chọn --</SelectItem>
                <SelectItem value="MALE">Nam</SelectItem>
                <SelectItem value="FEMALE">Nữ</SelectItem>
                <SelectItem value="OTHER">Khác</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="id_card_number">Số CMND/CCCD</Label>
            <Input id="id_card_number" {...register('id_card_number')} />
          </div>

          <div className="space-y-2 md:col-span-3">
            <Label htmlFor="place_of_birth">Nơi sinh (Tỉnh/Thành phố)</Label>
            <Input id="place_of_birth" {...register('place_of_birth')} />
          </div>

          {renderSelect('ethnicity', 'Dân tộc', ethnicities)}
          {renderSelect('religion', 'Tôn giáo', religions)}
          {renderSelect('nationality', 'Quốc tịch', nationalities)}
        </div>
      </section>

      {/* Section 4: Liên lạc */}
      <section className="bg-slate-50/50 p-6 rounded-xl border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">4. Thông tin Liên lạc</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <Label htmlFor="contact_phone">Số điện thoại liên hệ</Label>
            <Input id="contact_phone" {...register('contact_phone')} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="personal_email">Email cá nhân</Label>
            <Input id="personal_email" type="email" {...register('personal_email')} />
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="address">Địa chỉ hiện tại</Label>
            <Input id="address" {...register('address')} />
          </div>
          <div className="space-y-2 md:col-span-2">
            <Label htmlFor="bank_account">Số tài khoản ngân hàng</Label>
            <Input id="bank_account" {...register('bank_account')} placeholder="VD: 19035... (Techcombank)" />
          </div>
        </div>
      </section>

      {/* Actions */}
      <div className="flex justify-end gap-3 sticky bottom-0 bg-white p-4 border-t border-slate-200 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] -mx-6 -mb-6 z-10">
        <Button type="button" variant="outline" onClick={onCancel}>
          Hủy bỏ
        </Button>
        <Button type="submit" disabled={isLoading} className="min-w-[120px]">
          {isLoading ? 'Đang lưu...' : initialData ? 'Cập nhật' : 'Thêm mới'}
        </Button>
      </div>
    </form>
  );
}
