import { Users, BookOpen, GraduationCap, TrendingUp, Inbox } from 'lucide-react';
import { cn } from '../../utils/index';

// Dữ liệu rỗng khi chưa có API
const stats = [
  { name: 'Tổng sinh viên', value: '0', icon: Users, change: 'Chưa có dữ liệu', changeType: 'neutral' },
  { name: 'Lớp học phần', value: '0', icon: BookOpen, change: 'Chưa có dữ liệu', changeType: 'neutral' },
  { name: 'Giảng viên', value: '0', icon: GraduationCap, change: 'Chưa có dữ liệu', changeType: 'neutral' },
  { name: 'Truy cập hôm nay', value: '1', icon: TrendingUp, change: 'Bạn vừa đăng nhập', changeType: 'positive' },
];

export default function DashboardPage() {
  return (
    <div className="space-y-8 animate-in fade-in duration-500 font-sans">
      {/* Tiêu đề trang */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Tổng quan hệ thống</h1>
          <p className="text-slate-500 text-sm mt-1 font-medium">
            Chào mừng trở lại! Hệ thống hiện đang trống, vui lòng thêm dữ liệu.
          </p>
        </div>
      </div>

      {/* Thẻ thống kê (Stats Grid) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 flex flex-col group hover:border-slate-300 hover:shadow-md transition-all cursor-default relative overflow-hidden">
            <div className="absolute -right-6 -top-6 w-24 h-24 bg-slate-50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
            
            <div className="flex items-center justify-between mb-4 relative z-10">
              <div className="p-3 bg-slate-100 text-slate-700 rounded-xl group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300 shadow-sm border border-slate-200/50">
                <stat.icon size={22} strokeWidth={2.5} />
              </div>
              <span className={cn(
                "text-[11px] font-bold px-3 py-1 rounded-full border",
                stat.changeType === 'positive' 
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200/50' 
                  : 'bg-slate-50 text-slate-500 border-slate-200'
              )}>
                {stat.change}
              </span>
            </div>
            <div className="relative z-10">
              <p className="text-slate-500 text-sm font-bold tracking-wide uppercase">{stat.name}</p>
              <h3 className="text-3xl font-extrabold text-slate-900 mt-2 tracking-tight">{stat.value}</h3>
            </div>
          </div>
        ))}
      </div>

      {/* Khu vực Bảng và Biểu đồ trống */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Biểu đồ (Chiếm 2 cột) */}
        <div className="lg:col-span-2 bg-white rounded-2xl shadow-sm border border-slate-200 p-8 flex flex-col h-[400px]">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-slate-900 tracking-tight">Hoạt động sinh viên</h3>
          </div>
          
          {/* Empty State cho biểu đồ */}
          <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50 hover:bg-slate-50 transition-colors duration-300">
            <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center shadow-sm border border-slate-100 mb-4">
              <TrendingUp className="text-slate-400" size={28} strokeWidth={2} />
            </div>
            <p className="text-slate-700 font-bold text-lg">Chưa có dữ liệu thống kê</p>
            <p className="text-sm text-slate-500 mt-2 max-w-sm text-center font-medium leading-relaxed">
              Biểu đồ sẽ xuất hiện sau khi hệ thống có dữ liệu sinh viên và lịch sử hoạt động.
            </p>
          </div>
        </div>

        {/* Cảnh báo (Chiếm 1 cột) */}
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-8 flex flex-col h-[400px]">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-slate-900 tracking-tight">Cảnh báo hệ thống</h3>
          </div>
          
          {/* Empty State cho cảnh báo */}
          <div className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-slate-200 rounded-2xl bg-slate-50/50 hover:bg-slate-50 transition-colors duration-300">
            <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center shadow-sm border border-slate-100 mb-4">
              <Inbox className="text-slate-400" size={28} strokeWidth={2} />
            </div>
            <p className="text-slate-700 font-bold text-lg">Hệ thống an toàn</p>
            <p className="text-sm text-slate-500 mt-2 text-center font-medium">Không có cảnh báo bảo mật nào.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
