import apiClient from '../../../../api/client';

export const staffApi = {
  // Lấy danh sách CBNV (có phân trang, filter, search)
  getAll: (params) => {
    return apiClient.get('/hr/staffs/', { params });
  },

  // Lấy chi tiết CBNV theo ID
  getById: (id) => {
    return apiClient.get(`/hr/staffs/${id}/`);
  },

  // Thêm mới CBNV
  create: (data) => {
    return apiClient.post('/hr/staffs/', data);
  },

  // Cập nhật thông tin CBNV (chỉ cập nhật các trường được gửi lên)
  update: (id, data) => {
    return apiClient.patch(`/hr/staffs/${id}/`, data);
  },

  // Xóa CBNV
  delete: (id) => {
    return apiClient.delete(`/hr/staffs/${id}/`);
  },

  // Tải file template Excel
  getExcelTemplate: () => {
    return apiClient.get('/hr/staffs/excel-template/', {
      responseType: 'blob', // Quan trọng để tải file
    });
  },

  // Import từ file Excel
  importExcel: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return apiClient.post('/hr/staffs/import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Export danh sách ra Excel
  exportExcel: (params) => {
    return apiClient.get('/hr/staffs/export/', {
      params,
      responseType: 'blob',
    });
  }
};
