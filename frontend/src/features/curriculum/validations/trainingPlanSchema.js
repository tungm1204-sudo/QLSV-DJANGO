import { z } from 'zod';

export const trainingPlanSchema = z.object({
  name: z.string().min(1, 'Tên kế hoạch không được để trống'),
  semester: z.string().uuid('Vui lòng chọn học kỳ'),
  department: z.string().uuid('Vui lòng chọn khoa'),
});
