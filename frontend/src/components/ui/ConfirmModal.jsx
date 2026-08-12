import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export default function ConfirmModal({ 
  isOpen, 
  onClose, 
  onCancel, // Alias for onClose
  onConfirm, 
  title, 
  message, 
  content, // Alias for message
  isDanger = true,
  isLoading = false 
}) {
  const handleClose = onClose || onCancel;
  const displayMessage = message || content;
  return (
    <Dialog open={isOpen} onOpenChange={(open) => {
      if (!open && handleClose) handleClose();
    }}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-start gap-4">
            <div className={cn(
              "p-3 rounded-full shrink-0",
              isDanger ? "bg-red-100 text-red-600" : "bg-blue-100 text-blue-600"
            )}>
              <AlertTriangle size={24} />
            </div>
            <div className="flex-1 pt-1">
              <DialogTitle className="text-lg font-bold text-slate-900 mb-2">{title}</DialogTitle>
              <DialogDescription className="text-slate-500 text-sm leading-relaxed">
                {displayMessage}
              </DialogDescription>
            </div>
          </div>
        </DialogHeader>
        <DialogFooter className="sm:justify-end gap-2">
          <Button 
            type="button" 
            variant="outline"
            onClick={handleClose}
            disabled={isLoading}
          >
            Hủy bỏ
          </Button>
          <Button 
            type="button"
            variant={isDanger ? "destructive" : "default"}
            disabled={isLoading}
            onClick={() => {
              onConfirm();
              // Nếu không có isLoading (dùng theo kiểu cũ), đóng modal ngay lập tức
              if (!isLoading && handleClose) {
                handleClose();
              }
            }}
          >
            {isLoading ? 'Đang xử lý...' : 'Xác nhận'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
