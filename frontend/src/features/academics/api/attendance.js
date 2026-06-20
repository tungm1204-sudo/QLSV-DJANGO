import axiosClient from "../../../api/axiosClient";

export const attendanceApi = {
  getAttendances: (params) => axiosClient.get("academics/attendances/", { params }),
  getAttendanceSheet: (classroomId, date) => axiosClient.get(`academics/classrooms/${classroomId}/attendance-sheet/`, { params: { date } }),
  bulkUpdateAttendance: (data) => axiosClient.post("academics/attendances/bulk-update/", data),
};
