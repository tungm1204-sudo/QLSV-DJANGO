import apiClient from '../../../api/client';

export const getCourseOfferingsApi = (params) => apiClient.get('/curriculum/course-offering/', { params });
export const getCourseOfferingApi = (id) => apiClient.get(`/curriculum/course-offering/${id}/`);
export const createCourseOfferingApi = (data) => apiClient.post('/curriculum/course-offering/', data);
export const updateCourseOfferingApi = ({ id, data }) => apiClient.patch(`/curriculum/course-offering/${id}/`, data);
export const deleteCourseOfferingApi = (id) => apiClient.delete(`/curriculum/course-offering/${id}/`);
