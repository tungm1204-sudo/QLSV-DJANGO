import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import academicsApi from "../../api/academics";

// --- Semesters ---
export const useSemesters = () => {
  return useQuery({
    queryKey: ["semesters"],
    queryFn: () => academicsApi.getSemesters().then((res) => res.data),
  });
};

// --- Grades ---
export const useGrades = () => {
  return useQuery({
    queryKey: ["grades"],
    queryFn: () => academicsApi.getGrades().then((res) => res.data),
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
