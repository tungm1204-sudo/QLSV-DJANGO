import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { GraduationCap, Eye, EyeOff, Loader2, ShieldCheck, Sparkles, Server } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { cn } from '../../utils/index';
import { loginSchema, otpSchema, forgotSchema, resetPasswordSchema } from './validations/authSchema';
import { useAuth } from './hooks/useAuth';

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  
  const {
    step, setStep,
    serverError, setServerError,
    resetEmail,
    loginMutation,
    otpMutation,
    requestResetMutation,
    resetMutation,
  } = useAuth();

  const loginForm = useForm({ resolver: zodResolver(loginSchema), defaultValues: { email: '', password: '' } });
  const otpForm = useForm({ resolver: zodResolver(otpSchema), defaultValues: { otp: '' } });
  const forgotForm = useForm({ resolver: zodResolver(forgotSchema), defaultValues: { email: '' } });
  const resetForm = useForm({ resolver: zodResolver(resetPasswordSchema), defaultValues: { code: '', new_password: '' } });

  return (
    <div className="min-h-screen flex font-sans bg-white">
      {/* Cột trái: Branding & Abstract Glassmorphism */}
      <div className="hidden lg:flex lg:w-1/2 bg-[#0a0f1c] relative flex-col justify-center items-center p-12 overflow-hidden border-r border-slate-800">
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[60%] h-[60%] bg-blue-600/30 rounded-full mix-blend-screen filter blur-[120px] animate-pulse" style={{ animationDuration: '8s' }}></div>
          <div className="absolute bottom-[-20%] right-[-10%] w-[70%] h-[70%] bg-indigo-900/40 rounded-full mix-blend-screen filter blur-[150px]"></div>
          <div className="absolute top-[30%] right-[20%] w-[40%] h-[40%] bg-cyan-500/20 rounded-full mix-blend-screen filter blur-[100px]"></div>
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdHRoIGQ9Ik0gNDAgMCBMIDAgMCAwIDQwIiBmaWxsPSJub25lIiBzdHJva2U9InJnYmEoMjU1LDI1NSwyNTUsMC4wMikiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-50"></div>
        </div>

        <div className="absolute top-10 left-12 flex items-center gap-3 z-20">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/30">
            <GraduationCap size={20} className="text-white" />
          </div>
          <span className="text-white text-xl font-bold tracking-tight">QLSV ACADEMY</span>
        </div>

        <div className="relative z-10 p-10 bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl max-w-lg w-full transform transition-transform duration-500">
          <div className="w-14 h-14 bg-slate-800/80 border border-slate-700/50 rounded-2xl flex items-center justify-center mb-8 shadow-inner">
            <Server size={28} className="text-blue-400" />
          </div>
          
          <h2 className="text-3xl font-bold leading-tight mb-4 tracking-tight text-white">
            Nền tảng quản lý<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">
              Đại học thế hệ mới
            </span>
          </h2>
          
          <p className="text-slate-400 text-lg leading-relaxed font-medium">
            Kiến trúc bảo mật chuẩn Enterprise. Quản lý sinh viên, điểm số và dữ liệu hệ thống tập trung trên một nền tảng duy nhất với hiệu suất tối đa.
          </p>
        </div>
        
        <div className="absolute bottom-8 left-12 right-12 flex justify-between items-center z-10 text-slate-500 text-sm font-medium">
          <span>© 2026 QLSV Academy</span>
          <div className="flex gap-6">
            <a href="#" className="hover:text-slate-300 transition-colors">Enterprise Security</a>
          </div>
        </div>
      </div>

      {/* Cột phải: Form đăng nhập */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8 sm:p-12 relative z-10">
        <div className="w-full max-w-[420px]">
          
          <div className="lg:hidden flex items-center justify-center gap-3 mb-12">
            <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
              <GraduationCap size={24} className="text-white" />
            </div>
            <span className="text-slate-900 text-2xl font-extrabold tracking-tight">QLSV ACADEMY</span>
          </div>

          {step === 'login' && (
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="mb-10">
                <h3 className="text-4xl font-extrabold text-slate-900 tracking-tight">Đăng nhập</h3>
                <p className="text-slate-500 mt-3 font-medium text-base">Vui lòng nhập thông tin quản trị viên để truy cập hệ thống.</p>
              </div>

              <form onSubmit={loginForm.handleSubmit((d) => loginMutation.mutate(d))} className="space-y-6">
                <div>
                  <Label className="block text-sm font-bold text-slate-700 mb-2">Địa chỉ Email</Label>
                  <Input
                    {...loginForm.register('email')}
                    type="email"
                    placeholder="admin@qlsv.edu.vn"
                    className={cn(
                      'w-full px-4 h-12 rounded-xl bg-white transition-all outline-none shadow-sm',
                      'placeholder:text-slate-400 text-slate-900 font-medium',
                      loginForm.formState.errors.email
                        ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10 bg-red-50/30'
                        : 'border-slate-200 focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 hover:border-slate-300'
                    )}
                  />
                  {loginForm.formState.errors.email && (
                    <p className="mt-2 text-sm text-red-500 font-medium flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-red-500 inline-block" />
                      {loginForm.formState.errors.email.message}
                    </p>
                  )}
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <Label className="block text-sm font-bold text-slate-700">Mật khẩu</Label>
                    <button type="button" onClick={() => setStep('forgot')} className="text-sm font-bold text-blue-600 hover:text-blue-800 transition-colors">
                      Quên mật khẩu?
                    </button>
                  </div>
                  <div className="relative">
                    <Input
                      {...loginForm.register('password')}
                      type={showPassword ? 'text' : 'password'}
                      placeholder="••••••••"
                      className={cn(
                        'w-full px-4 pr-12 h-12 rounded-xl bg-white transition-all outline-none shadow-sm',
                        'placeholder:text-slate-400 text-slate-900 font-medium tracking-wide',
                        loginForm.formState.errors.password
                          ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10 bg-red-50/30'
                          : 'border-slate-200 focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 hover:border-slate-300'
                      )}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword((v) => !v)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 transition-colors"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  {loginForm.formState.errors.password && (
                    <p className="mt-2 text-sm text-red-500 font-medium flex items-center gap-1">
                      <span className="w-1.5 h-1.5 rounded-full bg-red-500 inline-block" />
                      {loginForm.formState.errors.password.message}
                    </p>
                  )}
                </div>

                {serverError && (
                  <div className="p-4 bg-red-50 border border-red-100 rounded-xl">
                    <p className="text-sm text-red-600 font-semibold">{serverError}</p>
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={loginMutation.isPending}
                  className="w-full h-12 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base shadow-lg shadow-blue-600/30 mt-8"
                >
                  {loginMutation.isPending ? <Loader2 size={20} className="animate-spin mr-2" /> : null}
                  {loginMutation.isPending ? 'Đang xác thực...' : 'Đăng nhập vào hệ thống'}
                </Button>
              </form>
            </div>
          )}

          {step === 'otp' && (
            <div className="animate-in fade-in slide-in-from-right-8 duration-500">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-blue-50 border border-blue-100 mb-6 shadow-inner">
                  <ShieldCheck size={36} className="text-blue-600" />
                </div>
                <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight">Xác thực 2 bước</h3>
                <p className="text-slate-500 mt-3 px-4 font-medium text-base">
                  Mã bảo mật gồm 6 chữ số đã được gửi đến email của bạn.
                </p>
              </div>

              <form onSubmit={otpForm.handleSubmit((d) => otpMutation.mutate(d))} className="space-y-6">
                <div>
                  <Input
                    {...otpForm.register('otp')}
                    type="text"
                    maxLength={6}
                    placeholder="000000"
                    className={cn(
                      'w-full text-center px-4 h-16 rounded-2xl text-4xl tracking-[0.5em] font-mono transition-all outline-none shadow-sm',
                      'text-slate-900 bg-white',
                      otpForm.formState.errors.otp
                        ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10'
                        : 'border-slate-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10'
                    )}
                  />
                  {otpForm.formState.errors.otp && (
                    <p className="mt-3 text-sm text-red-500 text-center font-bold">
                      {otpForm.formState.errors.otp.message}
                    </p>
                  )}
                </div>

                {serverError && (
                  <div className="p-4 bg-red-50 border border-red-100 rounded-xl text-center">
                    <p className="text-sm text-red-600 font-semibold">{serverError}</p>
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={otpMutation.isPending}
                  className="w-full h-12 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base shadow-lg shadow-blue-600/30"
                >
                  {otpMutation.isPending ? <Loader2 size={20} className="animate-spin mr-2" /> : null}
                  {otpMutation.isPending ? 'Đang xác thực...' : 'Xác nhận OTP'}
                </Button>

                <div className="text-center mt-6">
                  <button
                    type="button"
                    onClick={() => { setStep('login'); setServerError(''); }}
                    className="text-sm font-bold text-slate-500 hover:text-slate-900 transition-colors"
                  >
                    ← Trở về đăng nhập
                  </button>
                </div>
              </form>
            </div>
          )}

          {step === 'forgot' && (
            <div className="animate-in fade-in slide-in-from-right-8 duration-500">
              <div className="mb-10">
                <h3 className="text-4xl font-extrabold text-slate-900 tracking-tight">Khôi phục mật khẩu</h3>
                <p className="text-slate-500 mt-3 font-medium text-base">
                  Nhập địa chỉ email liên kết với tài khoản của bạn. Chúng tôi sẽ gửi hướng dẫn đặt lại mật khẩu.
                </p>
              </div>

              <form onSubmit={forgotForm.handleSubmit((d) => requestResetMutation.mutate(d))} className="space-y-6">
                <div>
                  <Label className="block text-sm font-bold text-slate-700 mb-2">Địa chỉ Email</Label>
                  <Input
                    {...forgotForm.register('email')}
                    type="email"
                    placeholder="admin@qlsv.edu.vn"
                    className={cn(
                      'w-full px-4 h-12 rounded-xl bg-white transition-all outline-none shadow-sm',
                      'placeholder:text-slate-400 text-slate-900 font-medium',
                      forgotForm.formState.errors.email
                        ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10'
                        : 'border-slate-200 focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 hover:border-slate-300'
                    )}
                  />
                  {forgotForm.formState.errors.email && (
                    <p className="mt-2 text-sm text-red-500 font-medium">{forgotForm.formState.errors.email.message}</p>
                  )}
                </div>

                {serverError && (
                  <div className="p-4 bg-red-50 border border-red-100 rounded-xl">
                    <p className="text-sm text-red-600 font-semibold">{serverError}</p>
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={requestResetMutation.isPending}
                  className="w-full h-12 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-base shadow-lg shadow-slate-900/20 mt-8"
                >
                  {requestResetMutation.isPending ? <Loader2 size={20} className="animate-spin mr-2" /> : null}
                  {requestResetMutation.isPending ? 'Đang gửi...' : 'Gửi mã xác nhận'}
                </Button>

                <div className="text-center mt-6">
                  <button
                    type="button"
                    onClick={() => { setStep('login'); setServerError(''); }}
                    className="text-sm font-bold text-slate-500 hover:text-slate-900 transition-colors"
                  >
                    ← Quay lại đăng nhập
                  </button>
                </div>
              </form>
            </div>
          )}

          {step === 'forgot-reset' && (
            <div className="animate-in fade-in slide-in-from-right-8 duration-500">
              <div className="mb-10">
                <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight">Tạo mật khẩu mới</h3>
                <p className="text-slate-500 mt-3 font-medium text-base">
                  Mã xác nhận đã được gửi đến <strong>{resetEmail}</strong>. Vui lòng nhập mã và mật khẩu mới.
                </p>
              </div>

              <form onSubmit={resetForm.handleSubmit((d) => resetMutation.mutate(d))} className="space-y-6">
                <div>
                  <Label className="block text-sm font-bold text-slate-700 mb-2">Mã OTP (6 số)</Label>
                  <Input
                    {...resetForm.register('code')}
                    type="text"
                    maxLength={6}
                    placeholder="000000"
                    className={cn(
                      'w-full px-4 h-12 rounded-xl text-center tracking-widest bg-white transition-all outline-none shadow-sm',
                      'text-slate-900 font-mono',
                      resetForm.formState.errors.code
                        ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10'
                        : 'border-slate-200 focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 hover:border-slate-300'
                    )}
                  />
                  {resetForm.formState.errors.code && (
                    <p className="mt-2 text-sm text-red-500 font-medium">{resetForm.formState.errors.code.message}</p>
                  )}
                </div>

                <div>
                  <Label className="block text-sm font-bold text-slate-700 mb-2">Mật khẩu mới</Label>
                  <div className="relative">
                    <Input
                      {...resetForm.register('new_password')}
                      type={showPassword ? 'text' : 'password'}
                      placeholder="••••••••"
                      className={cn(
                        'w-full px-4 pr-12 h-12 rounded-xl bg-white transition-all outline-none shadow-sm',
                        'placeholder:text-slate-400 text-slate-900 font-medium tracking-wide',
                        resetForm.formState.errors.new_password
                          ? 'border-red-400 focus:border-red-500 focus:ring-4 focus:ring-red-500/10 bg-red-50/30'
                          : 'border-slate-200 focus:border-blue-400 focus:ring-4 focus:ring-blue-500/10 hover:border-slate-300'
                      )}
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword((v) => !v)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 transition-colors"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                  {resetForm.formState.errors.new_password && (
                    <p className="mt-2 text-sm text-red-500 font-medium">{resetForm.formState.errors.new_password.message}</p>
                  )}
                </div>

                {serverError && (
                  <div className="p-4 bg-red-50 border border-red-100 rounded-xl">
                    <p className="text-sm text-red-600 font-semibold">{serverError}</p>
                  </div>
                )}

                <Button
                  type="submit"
                  disabled={resetMutation.isPending}
                  className="w-full h-12 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base shadow-lg shadow-blue-600/30 mt-8"
                >
                  {resetMutation.isPending ? <Loader2 size={20} className="animate-spin mr-2" /> : null}
                  {resetMutation.isPending ? 'Đang xử lý...' : 'Xác nhận đổi mật khẩu'}
                </Button>

                <div className="text-center mt-6">
                  <button
                    type="button"
                    onClick={() => { setStep('forgot'); setServerError(''); }}
                    className="text-sm font-bold text-slate-500 hover:text-slate-900 transition-colors"
                  >
                    ← Quay lại nhập Email
                  </button>
                </div>
              </form>
            </div>
          )}

          {step === 'forgot-success' && (
            <div className="animate-in fade-in zoom-in-95 duration-500 text-center py-8">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-emerald-50 border border-emerald-100 mb-6 shadow-inner">
                <ShieldCheck size={36} className="text-emerald-500" />
              </div>
              <h3 className="text-3xl font-extrabold text-slate-900 tracking-tight mb-4">Thành công!</h3>
              <p className="text-slate-500 font-medium text-base leading-relaxed mb-8">
                Mật khẩu của bạn đã được thay đổi thành công. Toàn bộ phiên đăng nhập trên các thiết bị khác đã bị đăng xuất để đảm bảo an toàn.
              </p>
              <button
                onClick={() => setStep('login')}
                className="w-full px-4 py-4 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-base transition-all shadow-lg shadow-blue-600/30"
              >
                Trở về trang đăng nhập
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
