import React from 'react';
import { Edit2, Trash2, FileText, Download } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import StatusBadge from '@/components/ui/StatusBadge';
import { format } from 'date-fns';

export default function CertificateTable({
  certificates,
  isLoading,
  canUpdate,
  canDelete,
  onEdit,
  onDelete
}) {
  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mt-4">
      <Table>
        <TableHeader className="bg-slate-50">
          <TableRow>
            <TableHead className="font-semibold px-4 py-3">Chứng chỉ</TableHead>
            <TableHead className="font-semibold px-4 py-3">Ngày cấp</TableHead>
            <TableHead className="font-semibold px-4 py-3">Điểm/Xếp loại</TableHead>
            <TableHead className="font-semibold px-4 py-3">Trạng thái</TableHead>
            <TableHead className="font-semibold px-4 py-3">Minh chứng</TableHead>
            <TableHead className="font-semibold text-right px-4 py-3">Hành động</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {isLoading ? (
            Array.from({ length: 3 }).map((_, idx) => (
              <TableRow key={idx}>
                <TableCell className="px-4 py-3"><Skeleton className="w-32 h-4" /></TableCell>
                <TableCell className="px-4 py-3"><Skeleton className="w-24 h-4" /></TableCell>
                <TableCell className="px-4 py-3"><Skeleton className="w-16 h-4" /></TableCell>
                <TableCell className="px-4 py-3"><Skeleton className="w-20 h-5 rounded-full" /></TableCell>
                <TableCell className="px-4 py-3"><Skeleton className="w-8 h-8 rounded" /></TableCell>
                <TableCell className="px-4 py-3 text-right"><Skeleton className="w-8 h-8 rounded ml-auto" /></TableCell>
              </TableRow>
            ))
          ) : certificates.length === 0 ? (
            <TableRow>
              <TableCell colSpan={6} className="px-4 py-8 text-center text-slate-500">
                Chưa có chứng chỉ nào được ghi nhận.
              </TableCell>
            </TableRow>
          ) : (
            certificates.map((cert) => (
              <TableRow key={cert.id} className="hover:bg-slate-50/50">
                <TableCell className="px-4 py-3">
                  <div className="font-medium text-slate-900">{cert.certificate_name}</div>
                  <div className="text-xs text-slate-500">{cert.provider || cert.certificate_type}</div>
                </TableCell>
                <TableCell className="px-4 py-3">
                  <div className="text-sm text-slate-900">{cert.issue_date ? format(new Date(cert.issue_date), 'dd/MM/yyyy') : 'N/A'}</div>
                  {cert.expiration_date && (
                    <div className="text-xs text-slate-500">Hết hạn: {format(new Date(cert.expiration_date), 'dd/MM/yyyy')}</div>
                  )}
                </TableCell>
                <TableCell className="px-4 py-3 text-sm">{cert.score || 'N/A'}</TableCell>
                <TableCell className="px-4 py-3">
                  <StatusBadge status={cert.status} />
                </TableCell>
                <TableCell className="px-4 py-3">
                  {cert.file_proof ? (
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-blue-600 hover:bg-blue-50" title="Tải xuống minh chứng" onClick={() => window.open(cert.file_proof, '_blank')}>
                      <FileText className="h-4 w-4" />
                    </Button>
                  ) : (
                    <span className="text-xs text-slate-400">Không có</span>
                  )}
                </TableCell>
                <TableCell className="px-4 py-3 text-right">
                  <div className="flex justify-end gap-1">
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-indigo-50"
                      disabled={!canUpdate} onClick={() => onEdit(cert)}
                    >
                      <Edit2 className="h-4 w-4 text-indigo-600" />
                    </Button>
                    <Button 
                      variant="ghost" size="icon" className="h-8 w-8 hover:bg-red-50"
                      disabled={!canDelete} onClick={() => onDelete(cert.id)}
                    >
                      <Trash2 className="h-4 w-4 text-red-600" />
                    </Button>
                  </div>
                </TableCell>
              </TableRow>
            ))
          )}
        </TableBody>
      </Table>
    </div>
  );
}
