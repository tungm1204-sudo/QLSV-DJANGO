import axiosClient from "./axiosClient";

const academicsApi = {
  // Semesters
  getSemesters: () => axiosClient.get("academics/semesters/"),
  
  // Grades
  getGrades: () => axiosClient.get("academics/grades/"),
  
  // Courses
  getCourses: () => axiosClient.get("academics/courses/"),
  createCourse: (data) => axiosClient.post("academics/courses/", data),
  updateCourse: (id, data) => axiosClient.patch(`academics/courses/${id}/`, data),
  deleteCourse: (id) => axiosClient.delete(`academics/courses/${id}/`),

  // Classrooms
  getClassrooms: () => axiosClient.get("academics/classrooms/"),
  createClassroom: (data) => axiosClient.post("academics/classrooms/", data),
  updateClassroom: (id, data) => axiosClient.patch(`academics/classrooms/${id}/`, data),
  deleteClassroom: (id) => axiosClient.delete(`academics/classrooms/${id}/`),
};

export default academicsApi;
