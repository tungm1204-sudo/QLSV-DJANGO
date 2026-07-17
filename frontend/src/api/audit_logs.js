import apiClient from './client';

export const getAuditLogsApi = (params) => apiClient.get('/identity/audit-logs/', { params });
