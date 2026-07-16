import apiClient from './client';

export const getUsersApi = (params) => apiClient.get('/identity/users/', { params });

export const getUserApi = (id) => apiClient.get(`/identity/users/${id}/`);

export const createUserApi = (data) => apiClient.post('/identity/users/', data);

export const updateUserApi = ({ id, data }) => apiClient.patch(`/identity/users/${id}/`, data);

export const deleteUserApi = (id) => apiClient.delete(`/identity/users/${id}/`);

export const lockUserApi = (id) => apiClient.patch(`/identity/users/${id}/`, { status: 'LOCKED', is_active: false });

export const unlockUserApi = (id) => apiClient.patch(`/identity/users/${id}/`, { status: 'ACTIVE', is_active: true });

export const resetPasswordApi = ({ id, new_password }) => apiClient.post(`/identity/users/${id}/force_reset_password/`, { password: new_password });

export const importExcelApi = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/identity/users/import_excel/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};
