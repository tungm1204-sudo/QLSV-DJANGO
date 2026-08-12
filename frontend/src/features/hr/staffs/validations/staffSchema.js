import * as z from 'zod';

export const staffSchema = z.object({
  // Account Information (Only required on creation, optional on edit)
  email: z.string().email('Email không hợp lệ').optional().or(z.literal('')),
  password: z.string().min(6, 'Mật khẩu phải từ 6 ký tự').optional().or(z.literal('')),
  full_name: z.string().min(2, 'Họ tên không được để trống'),
  
  // Work Information
  staff_code: z.string().min(2, 'Mã CBNV không được để trống'),
  department: z.string().min(1, 'Phòng ban không được để trống'),
  position: z.string().nullable().optional(),
  degree: z.string().nullable().optional(),
  responsibilities: z.string().optional().nullable(),
  join_date: z.string().optional().nullable(),
  status: z.enum(['ACTIVE', 'RETIRED', 'RESIGNED']).default('ACTIVE'),
  
  // Personal Information
  date_of_birth: z.string().optional().nullable(),
  gender: z.enum(['MALE', 'FEMALE', 'OTHER']).optional().nullable().or(z.literal('')),
  id_card_number: z.string().optional().nullable(),
  place_of_birth: z.string().optional().nullable(),
  ethnicity: z.string().nullable().optional(),
  religion: z.string().nullable().optional(),
  nationality: z.string().nullable().optional(),
  
  // Contact Information
  personal_email: z.string().email('Email không hợp lệ').optional().nullable().or(z.literal('')),
  contact_phone: z.string().optional().nullable(),
  address: z.string().optional().nullable(),
  bank_account: z.string().optional().nullable(),
});
