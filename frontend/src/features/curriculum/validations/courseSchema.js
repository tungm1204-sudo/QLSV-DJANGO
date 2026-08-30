import { z } from 'zod';

export const courseSchema = z.object({
  code: z.string().min(1, 'Mã môn học là bắt buộc').max(50, 'Mã môn học không quá 50 ký tự'),
  name: z.string().min(1, 'Tên môn học là bắt buộc').max(255, 'Tên môn học không quá 255 ký tự'),
  credits: z.number().min(1, 'Số tín chỉ phải lớn hơn 0'),
  theory_credits: z.number().min(0, 'Số tín chỉ lý thuyết không hợp lệ'),
  practical_credits: z.number().min(0, 'Số tín chỉ thực hành không hợp lệ'),
  department: z.string().min(1, 'Bộ môn quản lý là bắt buộc').uuid('ID bộ môn không hợp lệ'),
  course_type: z.string().nullable().optional(),
  is_active: z.boolean().default(true),
});
