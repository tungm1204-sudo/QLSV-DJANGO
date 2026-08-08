import * as z from 'zod';

export const userSchema = z.object({
  email: z.string().email('Email không hợp lệ'),
  full_name: z.string().min(2, 'Tên phải từ 2 ký tự').max(100),
  password: z.string().min(8, 'Mật khẩu phải từ 8 ký tự').optional().or(z.literal('')),
  // FIX: field phải là role_id (UUID) để Backend xử lý qua UserCreateUpdateSerializer
  role_id: z.string().uuid('Vai trò không hợp lệ').optional().nullable(),
});
