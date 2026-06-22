import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../api";

export const useAttendances = (params) => {
  return useQuery({
    queryKey: ["attendances", params],
    queryFn: () => academicsApi.getAttendances(params).then(res => res.data),
  });
};

export const useAttendanceSheet = (classroomId, date) => {
  return useQuery({
    queryKey: ["attendanceSheet", classroomId, date],
    queryFn: () => academicsApi.getAttendanceSheet(classroomId, date).then(res => res.data),
    enabled: !!classroomId && !!date,
  });
};

export const useBulkUpdateAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.bulkUpdateAttendance(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["attendanceSheet"] });
    },
  });
};
