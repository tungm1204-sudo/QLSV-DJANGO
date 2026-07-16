import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { MonitorSmartphone, X, Laptop, Smartphone, MapPin, Globe, Loader2, AlertCircle } from 'lucide-react';
import { getSessionsApi, revokeSessionApi } from '../../api/auth';
import { cn } from '../../utils';
import { formatDistanceToNow } from 'date-fns';
import { vi } from 'date-fns/locale';

export default function SessionManagement({ isOpen, onClose }) {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['login-sessions'],
    queryFn: async () => {
      const res = await getSessionsApi();
      return res.data;
    },
    enabled: isOpen,
  });

  const revokeMutation = useMutation({
    mutationFn: (sessionId) => revokeSessionApi(sessionId),
    onSuccess: () => {
      // Refresh the session list
      queryClient.invalidateQueries(['login-sessions']);
    },
  });

  if (!isOpen) return null;

  const parseDevice = (userAgent) => {
    if (!userAgent) return { type: 'laptop', name: 'Unknown Device' };
    const ua = userAgent.toLowerCase();
    if (ua.includes('mobile') || ua.includes('android') || ua.includes('iphone')) {
      return { type: 'mobile', name: 'Điện thoại di động' };
    }
    return { type: 'laptop', name: 'Máy tính (PC/Laptop)' };
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="flex items-center justify-between px-6 py-5 border-b border-slate-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
              <MonitorSmartphone size={20} />
            </div>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Thiết bị đăng nhập</h2>
              <p className="text-xs font-medium text-slate-500">Quản lý các phiên đăng nhập của bạn</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X size={20} />
          </button>
        </div>

        <div className="p-6 max-h-[60vh] overflow-y-auto">
          {isLoading && (
            <div className="flex flex-col items-center justify-center py-12 text-slate-400">
              <Loader2 size={32} className="animate-spin mb-4 text-blue-500" />
              <p className="font-medium">Đang tải danh sách thiết bị...</p>
            </div>
          )}

          {isError && (
            <div className="flex flex-col items-center justify-center py-8 text-red-500 bg-red-50 rounded-xl border border-red-100">
              <AlertCircle size={32} className="mb-3" />
              <p className="font-medium text-sm text-center px-4">
                {error?.response?.data?.detail || 'Không thể tải danh sách thiết bị. Vui lòng thử lại.'}
              </p>
            </div>
          )}

          {data && data.length === 0 && (
            <div className="text-center py-10 text-slate-500">
              <p className="font-medium">Không tìm thấy phiên đăng nhập nào.</p>
            </div>
          )}

          {data && data.length > 0 && (
            <div className="space-y-4">
              {data.map((session) => {
                const device = parseDevice(session.user_agent);
                return (
                  <div
                    key={session.id}
                    className={cn(
                      'flex items-start justify-between p-4 rounded-xl border transition-all',
                      session.is_active ? 'bg-white border-slate-200' : 'bg-slate-50 border-slate-100 opacity-60'
                    )}
                  >
                    <div className="flex gap-4">
                      <div className="p-3 bg-slate-100 rounded-full text-slate-600 shrink-0">
                        {device.type === 'mobile' ? <Smartphone size={20} /> : <Laptop size={20} />}
                      </div>
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <p className="font-bold text-slate-900 text-sm">
                            {device.name}
                          </p>
                          {session.is_active && session === data[0] && ( // Tạm giả định session đầu tiên là session hiện tại
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-700">
                              HIỆN TẠI
                            </span>
                          )}
                          {!session.is_active && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-200 text-slate-600">
                              ĐÃ ĐĂNG XUẤT
                            </span>
                          )}
                        </div>

                        <div className="flex flex-col gap-1.5 mt-2">
                          <div className="flex items-center gap-2 text-xs font-medium text-slate-500">
                            <Globe size={13} className="text-slate-400" />
                            <span className="truncate max-w-[200px]" title={session.user_agent}>
                              {session.user_agent || 'Không xác định'}
                            </span>
                          </div>
                          
                          <div className="flex flex-wrap items-center gap-4 text-xs font-medium text-slate-500">
                            <div className="flex items-center gap-1.5">
                              <MapPin size={13} className="text-slate-400" />
                              <span>{session.ip_address || 'Unknown IP'}</span>
                            </div>
                            <div className="w-1 h-1 rounded-full bg-slate-300"></div>
                            <div className="flex items-center gap-1.5">
                              <span>
                                Đăng nhập:{' '}
                                {formatDistanceToNow(new Date(session.created_at), { addSuffix: true, locale: vi })}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {session.is_active && session !== data[0] && (
                      <button
                        onClick={() => revokeMutation.mutate(session.id)}
                        disabled={revokeMutation.isPending}
                        className="px-3 py-1.5 shrink-0 text-xs font-bold text-red-600 bg-red-50 hover:bg-red-100 rounded-md transition-colors disabled:opacity-50"
                      >
                        Đăng xuất
                      </button>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
        
        <div className="px-6 py-4 border-t border-slate-100 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-bold text-slate-600 hover:text-slate-900 transition-colors"
          >
            Đóng
          </button>
        </div>
      </div>
    </div>
  );
}
