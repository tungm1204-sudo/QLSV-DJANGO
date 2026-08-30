import apiClient from '../../../api/client';

export const getTrainingPlansApi = (params) => apiClient.get('/curriculum/training-plan/', { params });
export const getTrainingPlanApi = (id) => apiClient.get(`/curriculum/training-plan/${id}/`);
export const createTrainingPlanApi = (data) => apiClient.post('/curriculum/training-plan/', data);
export const updateTrainingPlanApi = ({ id, data }) => apiClient.patch(`/curriculum/training-plan/${id}/`, data);
export const deleteTrainingPlanApi = (id) => apiClient.delete(`/curriculum/training-plan/${id}/`);
export const approveTrainingPlanApi = ({ id, status }) => apiClient.post(`/curriculum/training-plan/${id}/approve/`, { status });
export const duplicateTrainingPlanApi = ({ id, new_semester_id, new_name }) => apiClient.post(`/curriculum/training-plan/${id}/duplicate/`, { new_semester_id, new_name });
