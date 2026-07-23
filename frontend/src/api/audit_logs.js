import apiClient from './client';

export const getAuditLogsApi = (params) => apiClient.get('/core/audit-logs/', { params });
