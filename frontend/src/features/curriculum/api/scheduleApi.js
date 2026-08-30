import apiClient from '../../../api/client';

export const getSchedulesApi = (params) => apiClient.get('/curriculum/schedule/', { params });
export const getScheduleApi = (id) => apiClient.get(`/curriculum/schedule/${id}/`);
export const createScheduleApi = (data) => apiClient.post('/curriculum/schedule/', data);
export const updateScheduleApi = ({ id, data }) => apiClient.patch(`/curriculum/schedule/${id}/`, data);
export const deleteScheduleApi = (id) => apiClient.delete(`/curriculum/schedule/${id}/`);
export const validateScheduleApi = (data) => apiClient.post('/curriculum/schedule/validate/', data);
