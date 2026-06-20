import axiosClient from "../../../api/axiosClient";

export const classroomsApi = {
  getClassrooms: () => axiosClient.get("academics/classrooms/"),
  createClassroom: (data) => axiosClient.post("academics/classrooms/", data),
  updateClassroom: (id, data) => axiosClient.patch(`academics/classrooms/${id}/`, data),
  deleteClassroom: (id) => axiosClient.delete(`academics/classrooms/${id}/`),

  getEnrollments: (params) => axiosClient.get("academics/enrollments/", { params }),
  addEnrollment: (data) => axiosClient.post("academics/enrollments/", data),
  removeEnrollment: (id) => axiosClient.delete(`academics/enrollments/${id}/`),

  getAssignments: (params) => axiosClient.get("academics/assignments/", { params }),
  createAssignment: (data) => axiosClient.post("academics/assignments/", data),
  updateAssignment: (id, data) => axiosClient.patch(`academics/assignments/${id}/`, data),
  deleteAssignment: (id) => axiosClient.delete(`academics/assignments/${id}/`),
};
