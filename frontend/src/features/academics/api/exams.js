import axiosClient from "../../../api/axiosClient";

export const examsApi = {
  getExamTypes: () => axiosClient.get("academics/exam-types/"),
  createExamType: (data) => axiosClient.post("academics/exam-types/", data),
  updateExamType: (id, data) => axiosClient.patch(`academics/exam-types/${id}/`, data),
  deleteExamType: (id) => axiosClient.delete(`academics/exam-types/${id}/`),

  getGradeSheet: (params) => axiosClient.get("academics/exam-results/grade-sheet/", { params }),
  bulkUpdateGrades: (data) => axiosClient.post("academics/exam-results/bulk-update/", data),
  getStudentGPA: (studentId) => axiosClient.get("academics/exam-results/student-gpa/", { params: { student_id: studentId } }),
};
