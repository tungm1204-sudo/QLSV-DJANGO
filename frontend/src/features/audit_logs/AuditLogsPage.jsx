import { useState } from 'react';
import { Activity, Search, Download } from 'lucide-react';
import { usePermissions } from '../../hooks/usePermissions';
import { useAuditLogs } from './hooks/useAuditLogs';
import AuditLogTable from './components/AuditLogTable';

export default function AuditLogsPage() {
  const { hasPermission } = usePermissions();
  const canView = hasPermission('AUDIT_VIEW');
  // const canExport = hasPermission('AUDIT_EXPORT');

  const [searchQuery, setSearchQuery] = useState('');
  const [page, setPage] = useState(1);
  const [selectedLog, setSelectedLog] = useState(null);

  const { logs, totalPages, isLoading } = useAuditLogs(searchQuery, page, canView);

  if (!canView) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-slate-500">
        <Activity size={48} className="mb-4 text-slate-300" />
        <p>Bạn không có quyền xem nhật ký hệ thống.</p>
      </div>
    );
  }

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

      <AuditLogTable 
        logs={logs}
        isLoading={isLoading}
        page={page}
        setPage={setPage}
        totalPages={totalPages}
        setSelectedLog={setSelectedLog}
      />

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
