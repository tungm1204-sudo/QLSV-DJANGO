import React from 'react';
import { cn } from '../../utils';

export default function StatusBadge({ status, className }) {
  const badgeConfig = {
    // HR & General Statuses
    ACTIVE: { label: 'Đang hoạt động', color: 'bg-green-100 text-green-700 border-green-200' },
    PAUSED: { label: 'Tạm dừng', color: 'bg-yellow-100 text-yellow-700 border-yellow-200' },
    GRADUATED: { label: 'Đã tốt nghiệp', color: 'bg-purple-100 text-purple-700 border-purple-200' },
    DROPPED_OUT: { label: 'Thôi học', color: 'bg-red-100 text-red-700 border-red-200' },
    RETIRED: { label: 'Nghỉ hưu', color: 'bg-slate-100 text-slate-700 border-slate-200' },
    RESIGNED: { label: 'Đã nghỉ việc', color: 'bg-red-50 text-red-600 border-red-100' },
    
    // Approval Statuses
    PENDING: { label: 'Chờ duyệt', color: 'bg-yellow-100 text-yellow-700 border-yellow-200' },
    APPROVED: { label: 'Đã duyệt', color: 'bg-green-100 text-green-700 border-green-200' },
    REJECTED: { label: 'Từ chối', color: 'bg-red-100 text-red-700 border-red-200' },

    // Users Status
    LOCKED: { label: 'Đã khóa', color: 'bg-red-100 text-red-700 border-red-200' },
  };

  const config = badgeConfig[status] || { label: status, color: 'bg-slate-100 text-slate-700 border-slate-200' };

  return (
    <span className={cn('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border', config.color, className)}>
      {config.label}
    </span>
  );
}
