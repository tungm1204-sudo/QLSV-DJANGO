import apiClient from './client';

export const getSystemConfigsApi = () => apiClient.get('/identity/system-configs/');
export const createSystemConfigApi = (data) => apiClient.post('/identity/system-configs/', data);
export const updateSystemConfigApi = (id, data) => apiClient.put(`/identity/system-configs/${id}/`, data);
export const deleteSystemConfigApi = (id) => apiClient.delete(`/identity/system-configs/${id}/`);
