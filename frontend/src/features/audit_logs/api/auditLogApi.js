import apiClient from '../../../api/client';

export const getAuditLogsApi = (params) => apiClient.get('/core/audit-logs/', { params });
