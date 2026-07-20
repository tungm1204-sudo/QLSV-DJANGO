import apiClient from './client';

const ENDPOINTS = {
  departments: '/master-data/departments/',
  majors: '/master-data/majors/',
  rooms: '/master-data/rooms/',
  priorityCategories: '/master-data/priority-categories/',
  examTypes: '/master-data/exam-types/',
  cohorts: '/master-data/cohorts/',
  semesters: '/master-data/semesters/',
  specializations: '/master-data/specializations/',
  educationSystems: '/master-data/education-systems/',
  academicYears: '/master-data/academic-years/',
};

// Generic CRUD API generator
const createCrudApi = (endpoint) => ({
  getAll: (params) => apiClient.get(endpoint, { params }),
  getById: (id) => apiClient.get(`${endpoint}${id}/`),
  create: (data) => apiClient.post(endpoint, data),
  update: (id, data) => apiClient.put(`${endpoint}${id}/`, data),
  patch: (id, data) => apiClient.patch(`${endpoint}${id}/`, data),
  delete: (id) => apiClient.delete(`${endpoint}${id}/`),
});

export const departmentApi = createCrudApi(ENDPOINTS.departments);
export const majorApi = createCrudApi(ENDPOINTS.majors);
export const roomApi = createCrudApi(ENDPOINTS.rooms);
export const priorityCategoryApi = createCrudApi(ENDPOINTS.priorityCategories);
export const examTypeApi = createCrudApi(ENDPOINTS.examTypes);
export const cohortApi = createCrudApi(ENDPOINTS.cohorts);
export const semesterApi = createCrudApi(ENDPOINTS.semesters);
export const specializationApi = createCrudApi(ENDPOINTS.specializations);
export const educationSystemApi = createCrudApi(ENDPOINTS.educationSystems);
export const academicYearApi = createCrudApi(ENDPOINTS.academicYears);
