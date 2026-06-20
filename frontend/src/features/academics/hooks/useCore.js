import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../api";

// --- Dashboard ---
export const useDashboardStats = () => {
  return useQuery({
    queryKey: ["dashboardStats"],
    queryFn: () => academicsApi.getDashboardStats().then(res => res.data),
    staleTime: 60 * 1000,
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
