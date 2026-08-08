import * as z from 'zod';

export const SYSTEM_ROLES = ['Administrator', 'Giáo vụ', 'Giảng viên', 'Sinh viên', 'Kế toán', 'Công tác SV'];

export const roleSchema = z.object({
  name: z.string().min(2, 'Tên vai trò phải từ 2 ký tự').max(100, 'Tên vai trò tối đa 100 ký tự'),
  description: z.string().max(255).optional(),
  permissions: z.array(z.string()),
});
