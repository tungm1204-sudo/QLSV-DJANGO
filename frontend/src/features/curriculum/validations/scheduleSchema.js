import { z } from 'zod';

export const scheduleSchema = z.object({
  room: z.string().uuid('Vui lòng chọn phòng học'),
  day_of_week: z.number().min(2).max(8, 'Thứ phải từ 2 đến Chủ nhật (8)'),
  start_period: z.number().min(1).max(15, 'Tiết học từ 1 đến 15'),
  end_period: z.number().min(1).max(15, 'Tiết học từ 1 đến 15'),
}).refine((data) => data.end_period >= data.start_period, {
  message: "Tiết kết thúc phải lớn hơn hoặc bằng tiết bắt đầu",
  path: ["end_period"],
});
