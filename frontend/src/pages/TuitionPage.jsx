import { useTuitionFees, usePayTuitionFee } from '../features/finance/hooks/useTuition';
import { useAuthStore } from '../stores/authStore';

export default function TuitionPage() {
  const { user } = useAuthStore();
  const { data: tuitions = [], isLoading } = useTuitionFees();
  const payMutation = usePayTuitionFee();

  if (isLoading) return <div className="p-4">Đang tải dữ liệu...</div>;

  const handlePay = (id) => {
    if (window.confirm("Xác nhận thu tiền học phí này?")) {
      payMutation.mutate(id);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6 text-gray-800">Quản lý Học Phí</h1>
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Học kỳ</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sinh viên</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tín chỉ</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Số tiền</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng thái</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Môn học</th>
                {user?.role === 'admin' && (
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hành động</th>
                )}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {tuitions.length === 0 ? (
                <tr><td colSpan="7" className="px-6 py-4 text-center text-gray-500">Không có dữ liệu học phí</td></tr>
              ) : (
                tuitions.map((fee) => (
                  <tr key={fee.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{fee.semester}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      <div>{fee.student_name}</div>
                      <div className="text-xs text-gray-500">{fee.mssv}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{fee.total_credits}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900">
                      {Number(fee.total_amount).toLocaleString('vi-VN')} đ
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${fee.status === 'PAID' ? 'bg-green-100 text-green-800' : fee.status === 'OVERDUE' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {fee.status === 'PAID' ? 'Đã nộp' : fee.status === 'OVERDUE' ? 'Nợ' : 'Chưa nộp'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-xs text-gray-500 space-y-1">
                        {fee.details?.length > 0 ? fee.details.map(d => (
                          <div key={d.id}>• {d.course_name} ({d.credits} TC)</div>
                        )) : 'Không có chi tiết môn học'}
                      </div>
                    </td>
                    {user?.role === 'admin' && (
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        {fee.status !== 'PAID' ? (
                          <button
                            onClick={() => handlePay(fee.id)}
                            disabled={payMutation.isPending}
                            className="text-indigo-600 hover:text-indigo-900 disabled:opacity-50"
                          >
                            Xác nhận nộp
                          </button>
                        ) : (
                          <span className="text-gray-400">Đã hoàn thành</span>
                        )}
                      </td>
                    )}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
