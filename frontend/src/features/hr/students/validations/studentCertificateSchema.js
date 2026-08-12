import { z } from 'zod';

export const studentCertificateSchema = z.object({
  student: z.string().uuid('Sinh viên là bắt buộc'),
  certificate_type: z.string().min(1, 'Loại chứng chỉ là bắt buộc').max(100),
  certificate_name: z.string().min(1, 'Tên chứng chỉ là bắt buộc').max(255),
  issue_date: z.string().min(1, 'Ngày cấp là bắt buộc'),
  expiration_date: z.string().nullable().optional(),
  score: z.string().max(50).nullable().optional(),
  provider: z.string().max(255).nullable().optional(),
  status: z.string().min(1, 'Trạng thái là bắt buộc'),
  // file_proof: z.any().optional(), // Xử lý file ngoài schema
});
