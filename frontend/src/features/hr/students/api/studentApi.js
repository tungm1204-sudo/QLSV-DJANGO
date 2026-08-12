import apiClient from '../../../../api/client';

export const getStudentsApi = (params) => apiClient.get('/hr/students/', { params });

export const getStudentApi = (id) => apiClient.get(`/hr/students/${id}/`);

export const createStudentApi = (data) => apiClient.post('/hr/students/', data);

export const updateStudentApi = ({ id, data }) => apiClient.patch(`/hr/students/${id}/`, data);

export const deleteStudentApi = (id) => apiClient.delete(`/hr/students/${id}/`);

export const printIdCardApi = (id) => apiClient.get(`/hr/students/${id}/print-id-card/`, { responseType: 'blob' });

export const importStudentsApi = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/hr/students/import/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const exportStudentsApi = (params) => apiClient.get('/hr/students/export/', { 
    params,
    responseType: 'blob'
});
