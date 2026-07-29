import apiClient from './client';

const ENDPOINTS = {
  departments: '/master-data/department/',
  majors: '/master-data/major/',
  specializations: '/master-data/specialization/',
  campuses: '/master-data/campus/',
  buildings: '/master-data/building/',
  rooms: '/master-data/room/',
  priorityCategories: '/master-data/priority-category/',
  examTypes: '/master-data/exam-type/',
  cohorts: '/master-data/cohort/',
  academicYears: '/master-data/academic-year/',
  semesters: '/master-data/semester/',
  administrativeClasses: '/master-data/administrative-class/',
  educationSystems: '/master-data/education-system/',
  degrees: '/master-data/degree/',
  academicTitles: '/master-data/academic-title/',
  admissionTypes: '/master-data/admission-type/',
  ethnicities: '/master-data/ethnicity/',
  religions: '/master-data/religion/',
  nationalities: '/master-data/nationality/',
  courseTypes: '/master-data/course-type/',
  positions: '/master-data/position/',
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
export const specializationApi = createCrudApi(ENDPOINTS.specializations);
export const campusApi = createCrudApi(ENDPOINTS.campuses);
export const buildingApi = createCrudApi(ENDPOINTS.buildings);
export const roomApi = createCrudApi(ENDPOINTS.rooms);
export const priorityCategoryApi = createCrudApi(ENDPOINTS.priorityCategories);
export const examTypeApi = createCrudApi(ENDPOINTS.examTypes);
export const cohortApi = createCrudApi(ENDPOINTS.cohorts);
export const academicYearApi = createCrudApi(ENDPOINTS.academicYears);
export const semesterApi = createCrudApi(ENDPOINTS.semesters);
export const administrativeClassApi = createCrudApi(ENDPOINTS.administrativeClasses);
export const educationSystemApi = createCrudApi(ENDPOINTS.educationSystems);
export const degreeApi = createCrudApi(ENDPOINTS.degrees);
export const academicTitleApi = createCrudApi(ENDPOINTS.academicTitles);
export const admissionTypeApi = createCrudApi(ENDPOINTS.admissionTypes);
export const ethnicityApi = createCrudApi(ENDPOINTS.ethnicities);
export const religionApi = createCrudApi(ENDPOINTS.religions);
export const nationalityApi = createCrudApi(ENDPOINTS.nationalities);
export const courseTypeApi = createCrudApi(ENDPOINTS.courseTypes);
export const positionApi = createCrudApi(ENDPOINTS.positions);
