import axiosClient from "../../../api/axiosClient";

export const coreApi = {
  getDashboardStats: () => axiosClient.get("academics/dashboard/"),

  getSemesters: () => axiosClient.get("academics/semesters/"),
  createSemester: (data) => axiosClient.post("academics/semesters/", data),
  updateSemester: (id, data) => axiosClient.patch(`academics/semesters/${id}/`, data),
  deleteSemester: (id) => axiosClient.delete(`academics/semesters/${id}/`),
  
  getGrades: () => axiosClient.get("academics/grades/"),
  createGrade: (data) => axiosClient.post("academics/grades/", data),
  updateGrade: (id, data) => axiosClient.patch(`academics/grades/${id}/`, data),
  deleteGrade: (id) => axiosClient.delete(`academics/grades/${id}/`),

  getCourses: () => axiosClient.get("academics/courses/"),
  createCourse: (data) => axiosClient.post("academics/courses/", data),
  updateCourse: (id, data) => axiosClient.patch(`academics/courses/${id}/`, data),
  deleteCourse: (id) => axiosClient.delete(`academics/courses/${id}/`),
};
