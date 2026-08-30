import apiClient from '../../../api/client';

export const getCoursesApi = (params) => apiClient.get('/curriculum/course/', { params });

export const getCourseApi = (id) => apiClient.get(`/curriculum/course/${id}/`);

export const createCourseApi = (data) => apiClient.post('/curriculum/course/', data);

export const updateCourseApi = ({ id, data }) => apiClient.patch(`/curriculum/course/${id}/`, data);

export const deleteCourseApi = (id) => apiClient.delete(`/curriculum/course/${id}/`);
