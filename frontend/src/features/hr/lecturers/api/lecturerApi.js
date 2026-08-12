import apiClient from '../../../../api/client';

export const getLecturersApi = (params) => apiClient.get('/hr/lecturers/', { params });

export const getLecturerApi = (id) => apiClient.get(`/hr/lecturers/${id}/`);

export const createLecturerApi = (data) => apiClient.post('/hr/lecturers/', data);

export const updateLecturerApi = ({ id, data }) => apiClient.patch(`/hr/lecturers/${id}/`, data);

export const deleteLecturerApi = (id) => apiClient.delete(`/hr/lecturers/${id}/`);

export const importLecturersApi = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return apiClient.post('/hr/lecturers/import/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const exportLecturersApi = (params) => apiClient.get('/hr/lecturers/export/', { 
    params,
    responseType: 'blob'
});
