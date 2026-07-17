import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { Settings, Shield, Clock, AlertTriangle, Save, Loader2 } from 'lucide-react';
import { getSystemConfigsApi, updateSystemConfigApi, createSystemConfigApi } from '../../api/configs';
import { usePermissions } from '../../hooks/usePermissions';

export default function SystemConfigsPage() {
  const { hasPermission } = usePermissions();
  const canView = hasPermission('SYSTEM_VIEW');
  const canUpdate = hasPermission('SYSTEM_UPDATE');
  
  const queryClient = useQueryClient();
  
  const [maxAttempts, setMaxAttempts] = useState(5);
  const [lockoutDuration, setLockoutDuration] = useState(15);
  const [configIds, setConfigIds] = useState({ maxAttempts: null, lockoutDuration: null });

  const { data: configsData, isLoading } = useQuery({
    queryKey: ['systemConfigs'],
    queryFn: getSystemConfigsApi,
    enabled: canView,
  });

  useEffect(() => {
    if (configsData) {
      const configs = configsData?.data?.results || configsData?.data || [];
      const attemptsConfig = configs.find(c => c.key === 'MAX_LOGIN_ATTEMPTS');
      const durationConfig = configs.find(c => c.key === 'LOCKOUT_DURATION_MINUTES');
      
      if (attemptsConfig) {
        setMaxAttempts(Number(attemptsConfig.value));
        setConfigIds(prev => ({ ...prev, maxAttempts: attemptsConfig.id }));
      }
      if (durationConfig) {
        setLockoutDuration(Number(durationConfig.value));
        setConfigIds(prev => ({ ...prev, lockoutDuration: durationConfig.id }));
      }
    }
  }, [configsData]);

  const updateMutation = useMutation({
    mutationFn: async (payloads) => {
      const promises = payloads.map(p => {
        if (p.id) {
          return updateSystemConfigApi(p.id, { key: p.key, value: p.value });
        } else {
          return createSystemConfigApi({ key: p.key, value: p.value, description: p.description });
        }
      });
      return Promise.all(promises);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['systemConfigs']);
      toast.success('Lưu cấu hình thành công!');
    },
    onError: (error) => toast.error('Lỗi khi lưu cấu hình.'),
  });

  const handleSave = () => {
    const payloads = [
      { 
        id: configIds.maxAttempts, 
        key: 'MAX_LOGIN_ATTEMPTS', 
        value: maxAttempts, 
        description: 'Số lần đăng nhập sai tối đa trước khi khóa tài khoản' 
      },
      { 
        id: configIds.lockoutDuration, 
        key: 'LOCKOUT_DURATION_MINUTES', 
        value: lockoutDuration, 
        description: 'Thời gian khóa tài khoản (phút)' 
      }
    ];
    updateMutation.mutate(payloads);
  };

  if (!canView) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500">
        <Settings size={48} className="mb-4 text-slate-300" />
        <p>Bạn không có quyền xem cấu hình hệ thống.</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">Cấu hình Hệ thống</h1>
          <p className="text-slate-500 mt-1">Quản lý các tham số hoạt động cốt lõi của hệ thống</p>
        </div>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-6 border-b border-slate-100 bg-slate-50/50 flex items-center gap-3">
          <div className="p-2 bg-indigo-100 text-indigo-600 rounded-lg">
            <Shield size={20} />
          </div>
          <div>
            <h2 className="text-lg font-semibold text-slate-800">Bảo mật & Đăng nhập</h2>
            <p className="text-sm text-slate-500">Thiết lập các chính sách bảo vệ tài khoản người dùng</p>
          </div>
        </div>
        
        <div className="p-6 space-y-8">
          {isLoading ? (
            <div className="flex justify-center py-8">
              <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
            </div>
          ) : (
            <>
              {/* Field 1 */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl border border-slate-100 hover:border-indigo-100 hover:bg-indigo-50/30 transition-colors">
                <div className="flex gap-4">
                  <div className="mt-1 text-slate-400">
                    <AlertTriangle size={20} />
                  </div>
                  <div>
                    <label className="font-medium text-slate-700 block">Giới hạn đăng nhập sai</label>
                    <span className="text-sm text-slate-500">Số lần nhập sai mật khẩu tối đa trước khi tài khoản bị khóa tạm thời.</span>
                  </div>
                </div>
                <div className="sm:w-32 flex-shrink-0">
                  <div className="relative">
                    <input 
                      type="number" 
                      min="1" 
                      max="20"
                      value={maxAttempts}
                      onChange={(e) => setMaxAttempts(Number(e.target.value))}
                      disabled={!canUpdate || updateMutation.isPending}
                      className="w-full px-4 py-2 bg-white border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:bg-slate-50 font-medium"
                    />
                    <span className="absolute right-8 top-2.5 text-sm text-slate-400 pointer-events-none">lần</span>
                  </div>
                </div>
              </div>

              {/* Field 2 */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl border border-slate-100 hover:border-indigo-100 hover:bg-indigo-50/30 transition-colors">
                <div className="flex gap-4">
                  <div className="mt-1 text-slate-400">
                    <Clock size={20} />
                  </div>
                  <div>
                    <label className="font-medium text-slate-700 block">Thời gian khóa tài khoản</label>
                    <span className="text-sm text-slate-500">Thời gian người dùng không thể đăng nhập sau khi vượt quá giới hạn sai.</span>
                  </div>
                </div>
                <div className="sm:w-40 flex-shrink-0">
                  <div className="relative">
                    <input 
                      type="number" 
                      min="1" 
                      max="1440"
                      value={lockoutDuration}
                      onChange={(e) => setLockoutDuration(Number(e.target.value))}
                      disabled={!canUpdate || updateMutation.isPending}
                      className="w-full px-4 py-2 bg-white border border-slate-300 rounded-lg text-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 disabled:opacity-50 disabled:bg-slate-50 font-medium pr-14"
                    />
                    <span className="absolute right-4 top-2.5 text-sm text-slate-400 pointer-events-none">phút</span>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {canUpdate && (
          <div className="p-6 border-t border-slate-100 bg-slate-50 flex justify-end">
            <button
              onClick={handleSave}
              disabled={updateMutation.isPending || isLoading}
              className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg shadow-sm shadow-indigo-200 transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {updateMutation.isPending ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Đang lưu...
                </>
              ) : (
                <>
                  <Save size={18} />
                  Lưu thay đổi
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
