import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { loginApi, verifyOtpApi, getMeApi, requestPasswordResetOtpApi, resetPasswordApi } from '../api/authApi';
import useAuthStore from '../../../stores/useAuthStore';

export function useAuth() {
  const navigate = useNavigate();
  const { setTokens, setUser } = useAuthStore();
  
  const [step, setStep] = useState('login');
  const [serverError, setServerError] = useState('');
  const [otpToken, setOtpToken] = useState('');
  const [resetEmail, setResetEmail] = useState('');

  async function fetchAndRedirect(token) {
    try {
      const res = await getMeApi();
      setUser(res.data);
    } catch (e) {
      console.error(e);
    }
    navigate('/dashboard', { replace: true });
  }

  const loginMutation = useMutation({
    mutationFn: (data) => loginApi(data),
    onSuccess: (res) => {
      setServerError('');
      if (res.data.access) {
        setTokens(res.data.access);
        fetchAndRedirect(res.data.access);
        return;
      }
      if (res.data.otp_required) {
        setOtpToken(res.data.otp_token || '');
        setStep('otp');
      }
    },
    onError: (err) => {
      const errorData = err.response?.data;
      if (errorData?.code === 'account_locked') {
        setServerError(errorData?.detail || 'Tài khoản đã bị khóa do nhập sai quá nhiều lần.');
      } else {
        setServerError(errorData?.detail || 'Đăng nhập thất bại. Vui lòng kiểm tra lại email và mật khẩu.');
      }
    },
  });

  const otpMutation = useMutation({
    mutationFn: (data) => verifyOtpApi({ otp: data.otp, otp_token: otpToken }),
    onSuccess: (res) => {
      setServerError('');
      setTokens(res.data.access);
      fetchAndRedirect(res.data.access);
    },
    onError: (err) => setServerError(err.response?.data?.detail || 'Mã OTP không đúng hoặc đã hết hạn.'),
  });

  const requestResetMutation = useMutation({
    mutationFn: (data) => requestPasswordResetOtpApi(data),
    onSuccess: (_, variables) => {
      setServerError('');
      setResetEmail(variables.email);
      setStep('forgot-reset');
    },
    onError: (err) => setServerError(err.response?.data?.error || err.response?.data?.detail || 'Lỗi khi yêu cầu khôi phục mật khẩu.'),
  });

  const resetMutation = useMutation({
    mutationFn: (data) => resetPasswordApi({ email: resetEmail, ...data }),
    onSuccess: () => {
      setServerError('');
      setStep('forgot-success');
    },
    onError: (err) => setServerError(err.response?.data?.error || err.response?.data?.detail || 'Mã OTP không đúng hoặc có lỗi xảy ra.'),
  });

  return {
    step, setStep,
    serverError, setServerError,
    resetEmail,
    loginMutation,
    otpMutation,
    requestResetMutation,
    resetMutation,
  };
}

export function useLogout() {
  const navigate = useNavigate();
  const { clearAuth } = useAuthStore();

  const logoutMutation = useMutation({
    mutationFn: () => logoutApi(),
    onSettled: () => {
      clearAuth();
      navigate('/login', { replace: true });
    },
  });

  return { logoutMutation };
}

