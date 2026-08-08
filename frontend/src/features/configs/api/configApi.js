import apiClient from '../../../api/client';

export const getSystemConfigsApi = () => apiClient.get('/core/system-configs/');
export const createSystemConfigApi = (data) => apiClient.post('/core/system-configs/', data);
export const updateSystemConfigApi = (id, data) => apiClient.put(`/core/system-configs/${id}/`, data);
export const deleteSystemConfigApi = (id) => apiClient.delete(`/core/system-configs/${id}/`);
