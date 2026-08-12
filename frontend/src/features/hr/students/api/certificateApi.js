import apiClient from '../../../../api/client';

export const getCertificatesApi = (params) => apiClient.get('/hr/certificates/', { params });

export const getCertificateApi = (id) => apiClient.get(`/hr/certificates/${id}/`);

export const createCertificateApi = (data) => {
    // Nếu có upload file thì dùng FormData
    if (data.file_proof instanceof File) {
        const formData = new FormData();
        for (const key in data) {
            formData.append(key, data[key]);
        }
        return apiClient.post('/hr/certificates/', formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    }
    return apiClient.post('/hr/certificates/', data);
};

export const updateCertificateApi = ({ id, data }) => {
    if (data.file_proof instanceof File) {
        const formData = new FormData();
        for (const key in data) {
            formData.append(key, data[key]);
        }
        return apiClient.patch(`/hr/certificates/${id}/`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    }
    return apiClient.patch(`/hr/certificates/${id}/`, data);
};

export const deleteCertificateApi = (id) => apiClient.delete(`/hr/certificates/${id}/`);
