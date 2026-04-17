import api from '@/api/axiosClient';

export const getTeachers = async (params) => {
  const { data } = await api.get('/teachers/profiles/', { params });
  return data;
};

export const getTeacher = async (mgv) => {
  const { data } = await api.get(`/teachers/profiles/${mgv}/`);
  return data;
};

export const createTeacher = async (payload) => {
  const { data } = await api.post('/teachers/profiles/', payload);
  return data;
};

export const updateTeacher = async ({ mgv, data: payload }) => {
  const { data } = await api.patch(`/teachers/profiles/${mgv}/`, payload);
  return data;
};

export const deleteTeacher = async (mgv) => {
  const { data } = await api.delete(`/teachers/profiles/${mgv}/`);
  return data;
};
