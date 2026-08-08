import apiClient from '../../../api/client';

/**
 * auth.js - Tập hợp tất cả các hàm gọi API liên quan đến Xác thực.
 * Không chứa logic nghiệp vụ, chỉ wrap API call.
 */

// Đăng nhập bằng email/password
export const loginApi = (credentials) =>
  apiClient.post('/identity/auth/login/', credentials);

// Yêu cầu gửi OTP về email/sms
export const requestOtpApi = (payload) =>
  apiClient.post('/identity/auth/otp/request/', payload);

// Xác minh mã OTP
export const verifyOtpApi = (payload) =>
  apiClient.post('/identity/auth/otp/verify/', payload);

// Lấy thông tin user đang đăng nhập
export const getMeApi = () =>
  apiClient.get('/identity/users/me/');

// Lấy danh sách phiên đăng nhập của user hiện tại
export const getSessionsApi = () =>
  apiClient.get('/identity/auth/sessions/');

// Đăng xuất một phiên đăng nhập cụ thể từ xa (remote logout)
export const revokeSessionApi = (sessionId) =>
  apiClient.delete(`/identity/auth/sessions/${sessionId}/`);

// Đăng xuất phiên hiện tại
export const logoutApi = () =>
  apiClient.post('/identity/auth/logout/', {});

// Yêu cầu OTP khôi phục mật khẩu
export const requestPasswordResetOtpApi = (payload) =>
  apiClient.post('/identity/auth/password-reset/request-otp/', payload);

// Đặt lại mật khẩu mới
export const resetPasswordApi = (payload) =>
  apiClient.post('/identity/auth/reset-password/', payload);
