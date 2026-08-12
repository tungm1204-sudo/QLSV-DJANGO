import { z } from 'zod';

export const lecturerSchema = z.object({
  // Section 1: Thông tin tài khoản
  email: z.string().email('Email không hợp lệ').optional().or(z.literal('')),
  password: z.string().min(8, 'Mật khẩu tối thiểu 8 ký tự').optional().or(z.literal('')),
  full_name: z.string().min(2, 'Họ tên tối thiểu 2 ký tự').optional().or(z.literal('')),

  // Section 2: Thông tin công tác & Chuyên môn
  lecturer_code: z.string().min(1, 'Mã giảng viên là bắt buộc').regex(/^[a-zA-Z0-9_.-]+$/, 'Mã giảng viên không chứa ký tự đặc biệt'),
  department: z.string().uuid('Đơn vị/Khoa không hợp lệ').nullable().optional(),
  degree: z.string().uuid('Học vị không hợp lệ').nullable().optional(),
  academic_title: z.string().uuid('Học hàm không hợp lệ').nullable().optional(),
  contract_type: z.string().min(1, 'Loại hợp đồng là bắt buộc'),
  teaching_domain: z.string().nullable().optional(),
  join_date: z.string().nullable().optional(),
  status: z.string().min(1, 'Trạng thái là bắt buộc'),

  // Section 3: Nhân khẩu học
  date_of_birth: z.string().nullable().optional(),
  gender: z.string().nullable().optional(),
  id_card_number: z.string().max(50).nullable().optional(),
  place_of_birth: z.string().max(255).nullable().optional(),
  ethnicity: z.string().uuid().nullable().optional(),
  religion: z.string().uuid().nullable().optional(),
  nationality: z.string().uuid().nullable().optional(),

  // Section 4: Liên hệ
  contact_phone: z.string().max(20).nullable().optional(),
  personal_email: z.string().email('Email cá nhân không hợp lệ').nullable().optional().or(z.literal('')),
  address: z.string().nullable().optional(),
  bank_account: z.string().max(100).nullable().optional(),
});
