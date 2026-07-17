import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Activity, Search, Calendar, Monitor, Globe, FileJson, ChevronLeft, ChevronRight, Download } from 'lucide-react';
import { getAuditLogsApi } from '../../api/audit_logs';
import { usePermissions } from '../../hooks/usePermissions';
import { cn } from '../../utils';

const ACTION_COLORS = {
  CREATE: 'bg-emerald-50 text-emerald-700 border-emerald-100',
  UPDATE: 'bg-blue-50 text-blue-700 border-blue-100',
  DELETE: 'bg-red-50 text-red-700 border-red-100',
  LOGIN: 'bg-purple-50 text-purple-700 border-purple-100',
  RESET_PASSWORD: 'bg-orange-50 text-orange-700 border-orange-100',
};

export default function AuditLogsPage() {
  const { hasPermission } = usePermissions();
  const canView = hasPermission('AUDIT_VIEW');
  // const canExport = hasPermission('AUDIT_EXPORT');

  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [selectedLog, setSelectedLog] = useState(null);

  const { data: logsData, isLoading } = useQuery({
    queryKey: ['auditLogs', searchQuery, page],
    queryFn: () => getAuditLogsApi({ search: searchQuery, page }),
    enabled: canView,
    keepPreviousData: true,
  });

  if (!canView) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500">
        <Activity size={48} className="mb-4 text-slate-300" />
        <p>Bạn không có quyền xem nhật ký hệ thống.</p>
      </div>
    );
  }

  const logs = logsData?.data?.results || [];
  const totalPages = logsData?.data?.total_pages || 1;

  const formatDate = (dateString) => {
    return new Intl.DateTimeFormat('vi-VN', {
      year: 'numeric', month: '2-digit', day: '2-digit',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    }).format(new Date(dateString));
  };

  return (
    <div className="h-full flex flex-col space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Nhật ký Hệ thống</h1>
          <p className="text-slate-500 text-sm mt-1">Theo dõi toàn bộ thao tác của người dùng trên hệ thống</p>
        </div>
        
        <div className="flex items-center gap-3 w-full sm:w-auto">
          <div className="relative flex-1 sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
            <input 
              type="text" 
              placeholder="Tìm kiếm log..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-white border border-slate-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all shadow-sm"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-xl hover:bg-slate-50 transition-colors shadow-sm text-sm font-medium">
            <Download size={16} />
            <span className="hidden sm:inline">Xuất Excel</span>
          </button>
        </div>
      </div>

      {/* Table Section */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex-1 flex flex-col">
        <div className="overflow-x-auto flex-1">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-200">
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Thời gian</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Người thao tác</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Hành động</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">Module</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider">IP / Thiết bị</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase tracking-wider text-right">Chi tiết</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoading ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-slate-500">
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-4 h-4 border-2 border-indigo-600 border-t-transparent rounded-full animate-spin" />
                      Đang tải dữ liệu...
                    </div>
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center text-slate-500">
                    Không tìm thấy nhật ký nào.
                  </td>
                </tr>
              ) : (
                logs.map((log) => (
                  <tr key={log.id} className="hover:bg-slate-50/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2 text-sm text-slate-600">
                        <Calendar size={14} className="text-slate-400" />
                        {formatDate(log.created_at)}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col">
                        <span className="text-sm font-medium text-slate-900">{log.user_full_name || 'Hệ thống'}</span>
                        <span className="text-xs text-slate-500">{log.user_email || 'System Action'}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={cn(
                        "px-2.5 py-1 text-xs font-semibold rounded-md border",
                        ACTION_COLORS[log.action] || "bg-slate-50 text-slate-700 border-slate-200"
                      )}>
                        {log.action}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600 font-medium">
                      {log.module}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex flex-col gap-1">
                        <div className="flex items-center gap-1.5 text-xs text-slate-600">
                          <Globe size={12} className="text-slate-400" />
                          {log.ip_address || 'N/A'}
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-slate-500" title={log.user_agent}>
                          <Monitor size={12} className="text-slate-400" />
                          <span className="truncate max-w-[120px]">{log.user_agent || 'N/A'}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      {log.payload && (
                        <button 
                          onClick={() => setSelectedLog(log)}
                          className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                          title="Xem dữ liệu (Payload)"
                        >
                          <FileJson size={18} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="px-6 py-4 border-t border-slate-100 flex items-center justify-between bg-slate-50/50 mt-auto">
          <p className="text-sm text-slate-500">
            Trang <span className="font-medium text-slate-900">{page}</span> / <span className="font-medium text-slate-900">{totalPages}</span>
          </p>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-2 border border-slate-200 rounded-lg bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft size={16} />
            </button>
            <button 
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-2 border border-slate-200 rounded-lg bg-white text-slate-600 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Payload Modal */}
      {selectedLog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={() => setSelectedLog(null)} />
          <div className="relative bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[80vh]">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-slate-900">Chi tiết dữ liệu (Payload)</h3>
                <p className="text-sm text-slate-500 mt-1">ID Bản ghi: {selectedLog.record_id || 'N/A'}</p>
              </div>
              <button 
                onClick={() => setSelectedLog(null)}
                className="p-2 text-slate-400 hover:bg-slate-100 rounded-xl transition-colors"
              >
                &times;
              </button>
            </div>
            <div className="p-6 overflow-y-auto bg-slate-50">
              <pre className="text-sm text-slate-700 whitespace-pre-wrap font-mono">
                {JSON.stringify(selectedLog.payload, null, 2)}
              </pre>
            </div>
            <div className="p-4 border-t border-slate-100 bg-white text-right">
              <button 
                onClick={() => setSelectedLog(null)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-xl transition-colors"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
