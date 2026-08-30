import { z } from 'zod';

export const trainingProgramSchema = z.object({
  code: z.string().min(1, 'Mã chương trình là bắt buộc').max(50, 'Mã không quá 50 ký tự'),
  name: z.string().min(1, 'Tên chương trình là bắt buộc').max(255, 'Tên không quá 255 ký tự'),
  major: z.string().min(1, 'Ngành học là bắt buộc').uuid('ID ngành học không hợp lệ'),
  specialization: z.string().uuid('ID chuyên ngành không hợp lệ').nullable().optional(),
  cohort: z.string().min(1, 'Khóa học là bắt buộc').uuid('ID khóa học không hợp lệ'),
  total_credits: z.number().min(1, 'Tổng tín chỉ phải lớn hơn 0'),
  is_active: z.boolean().default(true),
});
