import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Email không hợp lệ'),
  password: z.string().min(8, 'Mật khẩu ít nhất 8 ký tự'),
});

export const otpSchema = z.object({
  otp: z.string().length(6, 'Mã OTP gồm đúng 6 chữ số').regex(/^\d+$/, 'Mã OTP chỉ chứa chữ số'),
});

export const forgotSchema = z.object({
  email: z.string().email('Email không hợp lệ'),
});

export const resetPasswordSchema = z.object({
  code: z.string().length(6, 'Mã OTP phải gồm 6 chữ số'),
  new_password: z.string().min(8, 'Mật khẩu ít nhất 8 ký tự'),
});
