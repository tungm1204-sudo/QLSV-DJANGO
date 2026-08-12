import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'sonner';
import { 
  getCertificatesApi, 
  getCertificateApi,
  createCertificateApi, 
  updateCertificateApi, 
  deleteCertificateApi
} from '../api/certificateApi';

const handleError = (err) => {
  if (err.response?.data) {
    const data = err.response.data;
    if (data.detail) return toast.error(data.detail);
    const firstErrorKey = Object.keys(data)[0];
    if (firstErrorKey && Array.isArray(data[firstErrorKey])) {
      return toast.error(`${firstErrorKey}: ${data[firstErrorKey][0]}`);
    }
  }
  toast.error('Có lỗi xảy ra');
};

export const useStudentCertificates = (studentId) => {
  return useQuery({
    queryKey: ['student_certificates', studentId],
    queryFn: async () => {
      const res = await getCertificatesApi({ student: studentId });
      return res.data;
    },
    enabled: !!studentId,
  });
};

export const useCertificateMutations = (studentId, onSuccessCallback) => {
  const queryClient = useQueryClient();

  const createMutation = useMutation({
    mutationFn: createCertificateApi,
    onSuccess: () => {
      toast.success('Thêm chứng chỉ thành công');
      queryClient.invalidateQueries(['student_certificates', studentId]);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const updateMutation = useMutation({
    mutationFn: updateCertificateApi,
    onSuccess: () => {
      toast.success('Cập nhật chứng chỉ thành công');
      queryClient.invalidateQueries(['student_certificates', studentId]);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCertificateApi,
    onSuccess: () => {
      toast.success('Xóa chứng chỉ thành công');
      queryClient.invalidateQueries(['student_certificates', studentId]);
      if (onSuccessCallback) onSuccessCallback();
    },
    onError: handleError
  });

  return {
    createMutation,
    updateMutation,
    deleteMutation
  };
};
