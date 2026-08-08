import apiClient from '../../../api/client';

export const getRolesApi = () => apiClient.get('/identity/roles/');

export const getRoleApi = (id) => apiClient.get(`/identity/roles/${id}/`);

export const createRoleApi = (data) => apiClient.post('/identity/roles/', data);

export const updateRoleApi = ({ id, data }) => apiClient.patch(`/identity/roles/${id}/`, data);

export const deleteRoleApi = (id) => apiClient.delete(`/identity/roles/${id}/`);

export const getAvailablePermissionsApi = () => apiClient.get('/identity/roles/available_permissions/');
