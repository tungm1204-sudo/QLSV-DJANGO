import axiosClient from "./axiosClient";

const academicsApi = {
  // Dashboard
  getDashboardStats: () => axiosClient.get("academics/dashboard/"),

  // Semesters
  getSemesters: () => axiosClient.get("academics/semesters/"),
  createSemester: (data) => axiosClient.post("academics/semesters/", data),
  updateSemester: (id, data) => axiosClient.patch(`academics/semesters/${id}/`, data),
  deleteSemester: (id) => axiosClient.delete(`academics/semesters/${id}/`),
  
  // Grades
  getGrades: () => axiosClient.get("academics/grades/"),
  createGrade: (data) => axiosClient.post("academics/grades/", data),
  updateGrade: (id, data) => axiosClient.patch(`academics/grades/${id}/`, data),
  deleteGrade: (id) => axiosClient.delete(`academics/grades/${id}/`),

  // ExamTypes
  getExamTypes: () => axiosClient.get("academics/exam-types/"),
  createExamType: (data) => axiosClient.post("academics/exam-types/", data),
  updateExamType: (id, data) => axiosClient.patch(`academics/exam-types/${id}/`, data),
  deleteExamType: (id) => axiosClient.delete(`academics/exam-types/${id}/`),
  
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

  // Enrollments (ClassroomStudent)
  getEnrollments: (params) => axiosClient.get("academics/enrollments/", { params }),
  addEnrollment: (data) => axiosClient.post("academics/enrollments/", data),
  removeEnrollment: (id) => axiosClient.delete(`academics/enrollments/${id}/`),
  // Assignments
  getAssignments: (params) => axiosClient.get("academics/assignments/", { params }),
  createAssignment: (data) => axiosClient.post("academics/assignments/", data),
  updateAssignment: (id, data) => axiosClient.patch(`academics/assignments/${id}/`, data),
  deleteAssignment: (id) => axiosClient.delete(`academics/assignments/${id}/`),

  // Attendances
  getAttendances: (params) => axiosClient.get("academics/attendances/", { params }),
  getAttendanceSheet: (classroomId, date) => axiosClient.get(`academics/classrooms/${classroomId}/attendance-sheet/`, { params: { date } }),
  bulkUpdateAttendance: (data) => axiosClient.post("academics/attendances/bulk-update/", data),

  // Exams
  getExamTypes: () => axiosClient.get("academics/exam-types/"),
  getGradeSheet: (params) => axiosClient.get("academics/exam-results/grade-sheet/", { params }),
  bulkUpdateGrades: (data) => axiosClient.post("academics/exam-results/bulk-update/", data),
  getStudentGPA: (studentId) => axiosClient.get("academics/exam-results/student-gpa/", { params: { student_id: studentId } }),
};

export default academicsApi;
