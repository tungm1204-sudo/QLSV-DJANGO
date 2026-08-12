import { z } from 'zod';

export const studentSchema = z.object({
  // Section 1: Thông tin tài khoản
  email: z.string().email('Email không hợp lệ').optional().or(z.literal('')),
  password: z.string().min(8, 'Mật khẩu tối thiểu 8 ký tự').optional().or(z.literal('')),
  full_name: z.string().min(2, 'Họ tên tối thiểu 2 ký tự').optional().or(z.literal('')),

  // Section 2: Thông tin học tập
  student_code: z.string().min(1, 'Mã sinh viên là bắt buộc').regex(/^[a-zA-Z0-9]+$/, 'Mã sinh viên chỉ chứa chữ và số'),
  major: z.string().uuid('Ngành không hợp lệ').nullable().optional(),
  administrative_class: z.string().uuid('Lớp không hợp lệ').nullable().optional(),
  education_system: z.string().uuid('Hệ đào tạo không hợp lệ').nullable().optional(),
  admission_type: z.string().uuid('Loại hình tuyển sinh không hợp lệ').nullable().optional(),
  priority_category: z.string().uuid('Đối tượng ưu tiên không hợp lệ').nullable().optional(),
  cohort: z.string().uuid('Khóa không hợp lệ').nullable().optional(),
  status: z.string().min(1, 'Trạng thái là bắt buộc'),
  enrollment_date: z.string().nullable().optional(),

  // Section 3: Thông tin cá nhân
  date_of_birth: z.string().nullable().optional(),
  gender: z.string().nullable().optional(),
  place_of_birth: z.string().max(255).nullable().optional(),
  ethnicity: z.string().uuid().nullable().optional(),
  religion: z.string().uuid().nullable().optional(),
  nationality: z.string().uuid().nullable().optional(),
  id_card_number: z.string().max(50).nullable().optional(),

  // Section 4: Liên hệ & Khác
  personal_email: z.string().email('Email cá nhân không hợp lệ').nullable().optional().or(z.literal('')),
  contact_phone: z.string().max(20).nullable().optional(),
  address: z.string().nullable().optional(),
  permanent_address: z.string().nullable().optional(),
  bank_account: z.string().max(100).nullable().optional(),
  health_insurance_number: z.string().max(50).nullable().optional(),
});
