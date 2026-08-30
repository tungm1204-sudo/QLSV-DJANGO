import { useMemo } from 'react';
import { useSchedules } from '../hooks/useSchedules';

const DAYS = [
  { value: 2, label: 'Thứ 2' },
  { value: 3, label: 'Thứ 3' },
  { value: 4, label: 'Thứ 4' },
  { value: 5, label: 'Thứ 5' },
  { value: 6, label: 'Thứ 6' },
  { value: 7, label: 'Thứ 7' },
  { value: 8, label: 'Chủ nhật' }
];

const PERIODS = Array.from({ length: 15 }, (_, i) => i + 1);

export default function TrainingPlanCalendarTab({ trainingPlanId }) {
  const { data, isLoading } = useSchedules({ 
    training_plan_id: trainingPlanId,
    page_size: 1000 // Lấy hết để vẽ lịch
  });

  const schedules = data?.results || data || [];

  // Tạo một map để tìm nhanh lịch theo thứ và tiết
  const calendarMap = useMemo(() => {
    const map = {};
    schedules.forEach(schedule => {
      const day = schedule.day_of_week;
      const start = schedule.start_period;
      const end = schedule.end_period;
      
      for (let p = start; p <= end; p++) {
        const key = `${day}-${p}`;
        if (!map[key]) {
          map[key] = [];
        }
        map[key].push(schedule);
      }
    });
    return map;
  }, [schedules]);

  if (isLoading) {
    return <div className="text-center py-12 text-slate-500">Đang tải lịch biểu...</div>;
  }

  // Hàm render ô trong bảng
  const renderCell = (day, period) => {
    const key = `${day}-${period}`;
    const cellSchedules = calendarMap[key];

    if (!cellSchedules || cellSchedules.length === 0) {
      return (
        <td key={key} className="border border-slate-200 p-2 h-16 hover:bg-slate-50 transition-colors"></td>
      );
    }

    // Nếu tiết này là tiết bắt đầu của một schedule, ta sẽ render ô đó với rowspan
    // Nhưng để đơn giản grid bằng HTML thuần, ta chỉ hiển thị nội dung ở tiết bắt đầu
    // và gộp nó lại (hoặc render thông tin vào từng ô). 
    // Ở đây ta render vào từng ô với màu sắc nổi bật.
    return (
      <td key={key} className="border border-slate-200 p-1 h-16 align-top">
        <div className="flex flex-col gap-1 h-full">
          {cellSchedules.map((schedule, idx) => {
            const isStart = schedule.start_period === period;
            return (
              <div 
                key={`${schedule.id}-${idx}`}
                className={`text-xs p-1.5 rounded bg-indigo-50 border border-indigo-100 ${!isStart ? 'border-t-0 rounded-t-none opacity-80' : 'rounded-b-none'}`}
              >
                {isStart && (
                  <>
                    <div className="font-semibold text-indigo-700 truncate" title={schedule.course_offering?.course?.name}>
                      {schedule.course_offering?.course?.code}
                    </div>
                    <div className="text-slate-600 truncate" title={schedule.room?.name}>
                      {schedule.room?.name}
                    </div>
                    {schedule.course_offering?.lecturer && (
                      <div className="text-slate-500 truncate mt-0.5 text-[10px]">
                        GV: {schedule.course_offering.lecturer.user?.last_name} {schedule.course_offering.lecturer.user?.first_name}
                      </div>
                    )}
                  </>
                )}
                {!isStart && (
                  <div className="text-transparent">.</div> // Giữ height
                )}
              </div>
            );
          })}
        </div>
      </td>
    );
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
      <div className="p-4 border-b border-slate-200 bg-slate-50">
        <h3 className="font-semibold text-slate-700">Lịch tuần</h3>
      </div>
      <div className="overflow-x-auto p-4">
        <table className="w-full min-w-[800px] border-collapse">
          <thead>
            <tr>
              <th className="border border-slate-200 bg-slate-100 p-2 w-16 text-center text-sm text-slate-600 font-medium">Tiết</th>
              {DAYS.map(day => (
                <th key={day.value} className="border border-slate-200 bg-slate-100 p-2 w-32 text-center text-sm text-slate-600 font-medium">
                  {day.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {PERIODS.map(period => (
              <tr key={period}>
                <td className="border border-slate-200 bg-slate-50 p-2 text-center text-sm font-medium text-slate-500">
                  {period}
                </td>
                {DAYS.map(day => renderCell(day.value, period))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
