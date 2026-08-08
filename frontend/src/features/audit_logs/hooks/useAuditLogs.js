import { useQuery } from '@tanstack/react-query';
import { getAuditLogsApi } from '../api/auditLogApi';

export function useAuditLogs(searchQuery, page, canView) {
  const { data: logsData, isLoading } = useQuery({
    queryKey: ['auditLogs', searchQuery, page],
    queryFn: () => getAuditLogsApi({ search: searchQuery, page }),
    enabled: canView,
    keepPreviousData: true,
  });

  const logs = logsData?.data?.results || [];
  const totalPages = logsData?.data?.total_pages || 1;

  return { logs, totalPages, isLoading };
}
