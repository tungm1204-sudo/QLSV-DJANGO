import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../api";

export const useExamTypes = () => {
  return useQuery({
    queryKey: ["examTypes"],
    queryFn: () => academicsApi.getExamTypes().then(res => res.data),
  });
};

export const useCreateExamType = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createExamType(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["examTypes"] }),
  });
};

export const useUpdateExamType = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateExamType(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["examTypes"] }),
  });
};

export const useDeleteExamType = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteExamType(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["examTypes"] }),
  });
};

export const useGradeSheet = (params) => {
  return useQuery({
    queryKey: ["gradeSheet", params],
    queryFn: () => academicsApi.getGradeSheet(params).then(res => res.data),
    enabled: !!params.classroom && !!params.course && !!params.semester && !!params.exam_type,
  });
};

export const useBulkUpdateGrades = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.bulkUpdateGrades(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["gradeSheet"] });
    },
  });
};

export const useStudentGPA = (studentId) => {
  return useQuery({
    queryKey: ["studentGPA", studentId],
    queryFn: () => academicsApi.getStudentGPA(studentId).then(res => res.data),
    // enabled always for student (studentId=undefined means fetch for self)
    // enabled when studentId is provided for admin/teacher views
    enabled: true,
  });
};
