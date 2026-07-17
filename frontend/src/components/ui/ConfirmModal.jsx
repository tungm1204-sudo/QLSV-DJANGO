import React from 'react';
import { AlertTriangle, X } from 'lucide-react';
import { cn } from '../../utils';

export default function ConfirmModal({ isOpen, onClose, onConfirm, title, message, isDanger = true }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-900/50 backdrop-blur-sm" onClick={onClose} />
      <div className="relative bg-white rounded-2xl shadow-xl w-full max-w-md overflow-hidden animate-in zoom-in-95 duration-200">
        <div className="p-6">
          <div className="flex items-start gap-4">
            <div className={cn(
              "p-3 rounded-full shrink-0",
              isDanger ? "bg-red-100 text-red-600" : "bg-blue-100 text-blue-600"
            )}>
              <AlertTriangle size={24} />
            </div>
            <div className="flex-1 pt-1">
              <h3 className="text-lg font-bold text-slate-900 mb-2">{title}</h3>
              <p className="text-slate-500 text-sm leading-relaxed">{message}</p>
            </div>
          </div>
        </div>
        
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-end gap-3">
          <button 
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-sm font-semibold text-slate-600 hover:bg-slate-200 transition-colors"
          >
            Hủy bỏ
          </button>
          <button 
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className={cn(
              "px-4 py-2 rounded-xl text-sm font-semibold text-white transition-colors shadow-sm",
              isDanger ? "bg-red-600 hover:bg-red-700 shadow-red-600/20" : "bg-blue-600 hover:bg-blue-700 shadow-blue-600/20"
            )}
          >
            Xác nhận
          </button>
        </div>
      </div>
    </div>
  );
}
