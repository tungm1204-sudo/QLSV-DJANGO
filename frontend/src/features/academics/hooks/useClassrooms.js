import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../api";

// --- Classrooms ---
export const useClassrooms = () => {
  return useQuery({
    queryKey: ["classrooms"],
    queryFn: () => academicsApi.getClassrooms().then((res) => res.data),
  });
};

export const useCreateClassroom = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createClassroom(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["classrooms"] }),
  });
};

export const useUpdateClassroom = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateClassroom(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["classrooms"] }),
  });
};

export const useDeleteClassroom = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteClassroom(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["classrooms"] }),
  });
};

// --- Enrollments ---
export const useEnrollments = (classroomId) => {
  return useQuery({
    queryKey: ["enrollments", classroomId],
    queryFn: () => academicsApi.getEnrollments({ classroom: classroomId }).then(res => res.data),
    enabled: !!classroomId,
  });
};

export const useAddEnrollment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.addEnrollment(data),
    onMutate: async (newEnrollment) => {
      const queryKey = ["enrollments", String(newEnrollment.classroom)];
      await queryClient.cancelQueries({ queryKey });
      const previousEnrollments = queryClient.getQueryData(queryKey);
      
      queryClient.setQueryData(queryKey, (old) => {
        const oldData = Array.isArray(old) ? old : old?.results || [];
        return [...oldData, {
          id: `temp-${Date.now()}`,
          student: newEnrollment.student,
          student_name: "Đang thêm...",
          enrolled_at: new Date().toISOString()
        }];
      });
      return { previousEnrollments, queryKey };
    },
    onError: (err, newEnrollment, context) => {
      if (context?.previousEnrollments) {
        queryClient.setQueryData(context.queryKey, context.previousEnrollments);
      }
    },
    onSettled: (_, __, variables) => {
      queryClient.invalidateQueries({ queryKey: ["enrollments", String(variables.classroom)] });
    },
  });
};

export const useRemoveEnrollment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id }) => academicsApi.removeEnrollment(id),
    onMutate: async ({ id, classroomId }) => {
      const queryKey = ["enrollments", String(classroomId)];
      await queryClient.cancelQueries({ queryKey });
      const previousEnrollments = queryClient.getQueryData(queryKey);

      queryClient.setQueryData(queryKey, (old) => {
        const oldData = Array.isArray(old) ? old : old?.results || [];
        return oldData.filter(enrollment => enrollment.id !== id);
      });
      return { previousEnrollments, queryKey };
    },
    onError: (err, variables, context) => {
      if (context?.previousEnrollments) {
        queryClient.setQueryData(context.queryKey, context.previousEnrollments);
      }
    },
    onSettled: (_, __, variables) => {
      queryClient.invalidateQueries({ queryKey: ["enrollments", String(variables.classroomId)] });
    },
  });
};

// --- Assignments ---
export const useAssignments = (params) => {
  return useQuery({
    queryKey: ["assignments", params],
    queryFn: () => academicsApi.getAssignments(params).then((res) => res.data),
  });
};

export const useCreateAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createAssignment(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assignments"] }),
  });
};

export const useUpdateAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateAssignment(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assignments"] }),
  });
};

export const useDeleteAssignment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteAssignment(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["assignments"] }),
  });
};
