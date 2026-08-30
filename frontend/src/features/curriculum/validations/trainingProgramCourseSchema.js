import { z } from 'zod';

export const trainingProgramCourseSchema = z.object({
  course: z.string().min(1, 'Học phần là bắt buộc').uuid('ID học phần không hợp lệ'),
  semester_expected: z.number().min(1, 'Học kỳ dự kiến tối thiểu là 1'),
  is_mandatory: z.boolean().default(true),
  notes: z.string().max(255, 'Ghi chú không quá 255 ký tự').nullable().optional(),
});
