import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../../api/academics";

// --- Dashboard ---
export const useDashboardStats = () => {
  return useQuery({
    queryKey: ["dashboardStats"],
    queryFn: () => academicsApi.getDashboardStats().then(res => res.data),
    staleTime: 60 * 1000, // Cache 60 giây
  });
};

// --- Semesters ---
export const useSemesters = () => {
  return useQuery({
    queryKey: ["semesters"],
    queryFn: () => academicsApi.getSemesters().then((res) => res.data),
  });
};

export const useCreateSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createSemester(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["semesters"] }),
  });
};

export const useUpdateSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateSemester(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["semesters"] }),
  });
};

export const useDeleteSemester = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteSemester(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["semesters"] }),
  });
};

// --- Grades ---
export const useGrades = () => {
  return useQuery({
    queryKey: ["grades"],
    queryFn: () => academicsApi.getGrades().then((res) => res.data),
  });
};

export const useCreateGrade = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createGrade(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["grades"] }),
  });
};

export const useUpdateGrade = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateGrade(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["grades"] }),
  });
};

export const useDeleteGrade = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteGrade(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["grades"] }),
  });
};

// --- Courses ---
export const useCourses = () => {
  return useQuery({
    queryKey: ["courses"],
    queryFn: () => academicsApi.getCourses().then((res) => res.data),
  });
};

export const useCreateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data) => academicsApi.createCourse(data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["courses"] }),
  });
};

export const useUpdateCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }) => academicsApi.updateCourse(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["courses"] }),
  });
};

export const useDeleteCourse = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id) => academicsApi.deleteCourse(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["courses"] }),
  });
};

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
      
      // Optimistically update the UI by pushing a temporary object
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
      // Rollback if failed
      if (context?.previousEnrollments) {
        queryClient.setQueryData(context.queryKey, context.previousEnrollments);
      }
    },
    onSettled: (_, __, variables) => {
      // Refresh in background to get real IDs and names
      queryClient.invalidateQueries({ queryKey: ["enrollments", String(variables.classroom)] });
    },
  });
};

export const useRemoveEnrollment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, classroomId }) => academicsApi.removeEnrollment(id),
    onMutate: async ({ id, classroomId }) => {
      const queryKey = ["enrollments", String(classroomId)];
      await queryClient.cancelQueries({ queryKey });
      const previousEnrollments = queryClient.getQueryData(queryKey);

      // Optimistically remove from UI
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

// --- Attendances ---
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
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ["attendanceSheet"] });
    },
  });
};

// --- Exams ---
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
