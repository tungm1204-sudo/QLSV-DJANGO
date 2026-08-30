import { z } from 'zod';

export const knowledgeBlockSchema = z.object({
  code: z.string().min(1, 'Mã khối là bắt buộc').max(50, 'Mã khối không quá 50 ký tự'),
  name: z.string().min(1, 'Tên khối là bắt buộc').max(255, 'Tên khối không quá 255 ký tự'),
  mandatory_credits: z.number().min(0, 'Số TC bắt buộc không hợp lệ'),
  elective_credits: z.number().min(0, 'Số TC tự chọn không hợp lệ'),
  order: z.number().min(1, 'Thứ tự không hợp lệ'),
  notes: z.string().nullable().optional(),
});
