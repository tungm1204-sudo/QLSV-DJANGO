import { coreApi } from "./core";
import { classroomsApi } from "./classrooms";
import { attendanceApi } from "./attendance";
import { examsApi } from "./exams";

const academicsApi = {
  ...coreApi,
  ...classroomsApi,
  ...attendanceApi,
  ...examsApi,
};

export default academicsApi;
