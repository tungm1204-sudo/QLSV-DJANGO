import { z } from 'zod';

export const courseOfferingSchema = z.object({
  course: z.string().uuid('Vui lòng chọn môn học'),
  lecturer: z.string().uuid('Vui lòng chọn giảng viên').or(z.literal('')).nullable().optional(),
  min_capacity: z.number().min(1, 'Sức chứa tối thiểu phải > 0'),
  max_capacity: z.number().min(1, 'Sức chứa tối đa phải > 0'),
  status: z.string().optional(),
}).refine((data) => data.max_capacity >= data.min_capacity, {
  message: "Sức chứa tối đa phải lớn hơn hoặc bằng tối thiểu",
  path: ["max_capacity"],
});
