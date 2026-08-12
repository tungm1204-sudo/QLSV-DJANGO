import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { studentSchema } from '../validations/studentSchema';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  useMajorOptions, 
  useAdministrativeClassOptions,
  useEducationSystemOptions,
  useAdmissionTypeOptions,
  usePriorityCategoryOptions,
  useCohortOptions,
  useEthnicityOptions,
  useReligionOptions,
  useNationalityOptions
} from '../../../master_data/hooks/useMasterDataOptions';

export default function StudentForm({ initialData, onSubmit, onCancel, isLoading }) {
  const form = useForm({
    resolver: zodResolver(studentSchema),
    defaultValues: initialData || {
      email: '', password: '', full_name: '',
      student_code: '', major: null, administrative_class: null,
      education_system: null, admission_type: null, priority_category: null,
      cohort: null, status: 'ACTIVE', enrollment_date: '',
      date_of_birth: '', gender: '', place_of_birth: '',
      ethnicity: null, religion: null, nationality: null, id_card_number: '',
      personal_email: '', contact_phone: '', address: '', permanent_address: '',
      bank_account: '', health_insurance_number: ''
    }
  });

  const { register, handleSubmit, formState: { errors }, setValue, watch } = form;

  // Master Data hooks
  const { data: majors = [] } = useMajorOptions();
  const { data: classes = [] } = useAdministrativeClassOptions();
  const { data: eduSystems = [] } = useEducationSystemOptions();
  const { data: admissionTypes = [] } = useAdmissionTypeOptions();
  const { data: priorities = [] } = usePriorityCategoryOptions();
  const { data: cohorts = [] } = useCohortOptions();
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

      {/* Section 2: Thông tin đào tạo */}
      <section className="bg-slate-50/50 p-6 rounded-xl border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">2. Thông tin Đào tạo</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="space-y-2">
            <Label htmlFor="student_code" className="after:content-['*'] after:ml-0.5 after:text-red-500">Mã sinh viên</Label>
            <Input id="student_code" {...register('student_code')} className={errors.student_code ? "border-red-500" : ""} />
            {errors.student_code && <p className="text-sm text-red-500">{errors.student_code.message}</p>}
          </div>
          {renderSelect('major', 'Ngành học', majors)}
          {renderSelect('administrative_class', 'Lớp hành chính', classes)}
          
          {renderSelect('education_system', 'Hệ đào tạo', eduSystems)}
          {renderSelect('admission_type', 'Loại hình tuyển sinh', admissionTypes)}
          {renderSelect('cohort', 'Khóa học', cohorts)}
          
          <div className="space-y-2">
            <Label htmlFor="status" className="after:content-['*'] after:ml-0.5 after:text-red-500">Trạng thái</Label>
            <Select value={watch('status')} onValueChange={(val) => setValue('status', val, { shouldValidate: true })}>
              <SelectTrigger id="status" className={errors.status ? "border-red-500" : ""}>
                <SelectValue placeholder="Trạng thái học tập">
                  {
                    watch('status') === 'ACTIVE' ? 'Đang học' :
                    watch('status') === 'PAUSED' ? 'Bảo lưu' :
                    watch('status') === 'GRADUATED' ? 'Đã tốt nghiệp' :
                    watch('status') === 'DROPPED_OUT' ? 'Thôi học' : undefined
                  }
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ACTIVE">Đang học</SelectItem>
                <SelectItem value="PAUSED">Bảo lưu</SelectItem>
                <SelectItem value="GRADUATED">Đã tốt nghiệp</SelectItem>
                <SelectItem value="DROPPED_OUT">Thôi học</SelectItem>
              </SelectContent>
            </Select>
            {errors.status && <p className="text-sm text-red-500">{errors.status?.message}</p>}
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="enrollment_date">Ngày nhập học</Label>
            <Input id="enrollment_date" type="date" {...register('enrollment_date')} />
          </div>
          {renderSelect('priority_category', 'Đối tượng ưu tiên', priorities)}
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
        <h3 className="text-lg font-semibold text-slate-900 mb-4 border-b pb-2">4. Thông tin Liên hệ & Khác</h3>
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
            <Label htmlFor="permanent_address">Hộ khẩu thường trú</Label>
            <Input id="permanent_address" {...register('permanent_address')} />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="bank_account">Số tài khoản ngân hàng</Label>
            <Input id="bank_account" {...register('bank_account')} placeholder="VD: 19035... (Techcombank)" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="health_insurance_number">Số thẻ BHYT</Label>
            <Input id="health_insurance_number" {...register('health_insurance_number')} />
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
