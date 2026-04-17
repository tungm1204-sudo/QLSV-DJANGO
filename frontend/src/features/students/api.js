import api from '@/api/axiosClient';

export const getStudents = async (params) => {
  const { data } = await api.get('/students/profiles/', { params });
  return data;
};

export const getStudent = async (mssv) => {
  const { data } = await api.get(`/students/profiles/${mssv}/`);
  return data;
};

export const createStudent = async (payload) => {
  const { data } = await api.post('/students/profiles/', payload);
  return data;
};

export const updateStudent = async ({ mssv, data: payload }) => {
  const { data } = await api.patch(`/students/profiles/${mssv}/`, payload);
  return data;
};

export const deleteStudent = async (mssv) => {
  const { data } = await api.delete(`/students/profiles/${mssv}/`);
  return data;
};

export const exportStudents = async () => {
    const response = await api.get('/students/profiles/export_excel/', {
        responseType: 'blob',
    });
    return response.data;
};

export const importStudents = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.post('/students/profiles/import_excel/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return data;
};
