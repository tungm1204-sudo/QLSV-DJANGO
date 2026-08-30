import apiClient from '../../../api/client';

export const getTrainingProgramsApi = (params) => apiClient.get('/curriculum/training-program/', { params });

export const getTrainingProgramApi = (id) => apiClient.get(`/curriculum/training-program/${id}/`);

export const createTrainingProgramApi = (data) => apiClient.post('/curriculum/training-program/', data);

export const updateTrainingProgramApi = ({ id, data }) => apiClient.patch(`/curriculum/training-program/${id}/`, data);

export const deleteTrainingProgramApi = (id) => apiClient.delete(`/curriculum/training-program/${id}/`);

// --- Knowledge Block ---
export const getKnowledgeBlocksApi = (params) => apiClient.get('/curriculum/knowledge-block/', { params });
export const createKnowledgeBlockApi = (data) => apiClient.post('/curriculum/knowledge-block/', data);
export const updateKnowledgeBlockApi = ({ id, data }) => apiClient.patch(`/curriculum/knowledge-block/${id}/`, data);
export const deleteKnowledgeBlockApi = (id) => apiClient.delete(`/curriculum/knowledge-block/${id}/`);

// --- Training Program Course ---
export const getTrainingProgramCoursesApi = (params) => apiClient.get('/curriculum/training-program-course/', { params });
export const createTrainingProgramCourseApi = (data) => apiClient.post('/curriculum/training-program-course/', data);
export const updateTrainingProgramCourseApi = ({ id, data }) => apiClient.patch(`/curriculum/training-program-course/${id}/`, data);
export const deleteTrainingProgramCourseApi = (id) => apiClient.delete(`/curriculum/training-program-course/${id}/`);
