import { useDashboardStats } from "../features/academics/hooks";
import { useAuthStore } from "../stores/authStore";
import { Link } from "react-router-dom";
import {
  Users, GraduationCap, BookOpen, CalendarDays,
  UserCheck, ClipboardList, TrendingUp, ArrowRight,
  CheckCircle2, XCircle, Clock, AlertCircle
} from "lucide-react";

// ─── Stat Card ────────────────────────────────────────────────────────────────
function StatCard({ title, value, icon: Icon, color, href }) {
  const content = (
    <div className={`bg-white rounded-xl border shadow-sm p-6 flex items-center gap-4 hover:shadow-md transition-shadow ${href ? "cursor-pointer group" : ""}`}>
      <div className={`p-3 rounded-xl ${color}`}>
        <Icon className="h-6 w-6 text-white" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-muted-foreground font-medium">{title}</p>
        <p className="text-3xl font-bold mt-0.5 tabular-nums">{value ?? "—"}</p>
      </div>
      {href && <ArrowRight className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />}
    </div>
  );
  return href ? <Link to={href}>{content}</Link> : <div>{content}</div>;
}

// ─── Mini Bar Chart (CSS-only, no lib) ───────────────────────────────────────
function AttendanceChart({ data }) {
  if (!data || data.length === 0) return null;
  const maxTotal = Math.max(...data.map(d => d.present + d.absent + d.late), 1);

  return (
    <div className="bg-white rounded-xl border shadow-sm p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-gray-900">Điểm Danh 7 Ngày Gần Nhất</h2>
        <div className="flex gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500 inline-block"></span>Có mặt</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-amber-400 inline-block"></span>Đi muộn</span>
          <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-red-400 inline-block"></span>Vắng</span>
        </div>
      </div>
      <div className="flex items-end gap-3 h-36">
        {data.map((day, i) => {
          const total = day.present + day.absent + day.late;
          const pctPresent = total > 0 ? (day.present / maxTotal) * 100 : 0;
          const pctLate    = total > 0 ? (day.late    / maxTotal) * 100 : 0;
          const pctAbsent  = total > 0 ? (day.absent  / maxTotal) * 100 : 0;
          return (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div className="w-full flex flex-col justify-end gap-0.5" style={{ height: "110px" }}>
                {pctPresent > 0 && (
                  <div className="w-full bg-emerald-500 rounded-sm" style={{ height: `${pctPresent}%` }} title={`Có mặt: ${day.present}`} />
                )}
                {pctLate > 0 && (
                  <div className="w-full bg-amber-400 rounded-sm" style={{ height: `${pctLate}%` }} title={`Đi muộn: ${day.late}`} />
                )}
                {pctAbsent > 0 && (
                  <div className="w-full bg-red-400 rounded-sm" style={{ height: `${pctAbsent}%` }} title={`Vắng: ${day.absent}`} />
                )}
                {total === 0 && (
                  <div className="w-full bg-gray-100 rounded-sm" style={{ height: "4px" }} />
                )}
              </div>
              <span className="text-xs text-muted-foreground">{day.day_label}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─── Attendance Distribution Donut (CSS only) ────────────────────────────────
function AttendanceDistribution({ dist }) {
  if (!dist) return null;
  const present = dist.present || 0;
  const absent  = dist.absent  || 0;
  const late    = dist.late    || 0;
  const excused = dist.excused || 0;
  const total   = present + absent + late + excused;

  const items = [
    { label: "Có mặt",  count: present, color: "bg-emerald-500", icon: CheckCircle2, iconColor: "text-emerald-500" },
    { label: "Vắng mặt", count: absent, color: "bg-red-400",     icon: XCircle,     iconColor: "text-red-400" },
    { label: "Đi muộn", count: late,    color: "bg-amber-400",   icon: Clock,       iconColor: "text-amber-400" },
    { label: "Có phép", count: excused, color: "bg-blue-400",    icon: AlertCircle, iconColor: "text-blue-400" },
  ];

  return (
    <div className="bg-white rounded-xl border shadow-sm p-6">
      <h2 className="font-semibold text-gray-900 mb-4">Phân Bố Điểm Danh (Tổng)</h2>
      {total === 0 ? (
        <p className="text-center text-muted-foreground py-8">Chưa có dữ liệu điểm danh.</p>
      ) : (
        <>
          {/* Progress bar */}
          <div className="flex rounded-full overflow-hidden h-3 mb-5 gap-px">
            {items.map((item, i) => (
              item.count > 0 && (
                <div
                  key={i}
                  className={item.color}
                  style={{ width: `${(item.count / total) * 100}%` }}
                  title={`${item.label}: ${item.count}`}
                />
              )
            ))}
          </div>
          <div className="space-y-2">
            {items.map((item, i) => {
              const Icon = item.icon;
              const pct = total > 0 ? ((item.count / total) * 100).toFixed(1) : 0;
              return (
                <div key={i} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Icon className={`h-4 w-4 ${item.iconColor}`} />
                    <span className="text-sm text-gray-700">{item.label}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold tabular-nums">{item.count}</span>
                    <span className="text-xs text-muted-foreground w-12 text-right">{pct}%</span>
                  </div>
                </div>
              );
            })}
          </div>
        </>
      )}
    </div>
  );
}

// ─── Top Classrooms ───────────────────────────────────────────────────────────
function TopClassrooms({ data }) {
  if (!data || data.length === 0) return null;
  const max = Math.max(...data.map(c => c.student_count), 1);

  return (
    <div className="bg-white rounded-xl border shadow-sm p-6">
      <h2 className="font-semibold text-gray-900 mb-4">Top Lớp Nhiều Sinh Viên Nhất</h2>
      <div className="space-y-3">
        {data.map((c, i) => (
          <div key={c["classroom__id"]} className="flex items-center gap-3">
            <span className="text-xs font-bold text-muted-foreground w-4">{i + 1}</span>
            <div className="flex-1">
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-medium text-gray-800">{c["classroom__name"]}</span>
                <span className="text-xs font-semibold text-primary">{c.student_count} SV</span>
              </div>
              <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary/70 rounded-full transition-all"
                  style={{ width: `${(c.student_count / max) * 100}%` }}
                />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── MAIN DASHBOARD ───────────────────────────────────────────────────────────
export default function Dashboard() {
  const user = useAuthStore(state => state.user);
  const { data, isLoading } = useDashboardStats();

  const overview = data?.overview || {};
  const semester = data?.current_semester;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Xin chào, <span className="font-medium text-gray-800">{user?.fullName}</span> 👋
          </p>
        </div>
        {semester && (
          <div className="hidden sm:block text-right">
            <p className="text-xs text-muted-foreground">Học kỳ hiện tại</p>
            <p className="font-semibold text-primary">{semester.name}</p>
            <p className="text-xs text-muted-foreground">{semester.academic_year}</p>
          </div>
        )}
      </div>

      {/* Stat cards */}
      {isLoading ? (
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="bg-white rounded-xl border shadow-sm p-6 h-24 animate-pulse bg-gray-100" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          <StatCard title="Sinh Viên" value={overview.total_students} icon={GraduationCap} color="bg-violet-500" href="/students" />
          <StatCard title="Giảng Viên" value={overview.total_teachers} icon={Users} color="bg-blue-500" href="/teachers" />
          <StatCard title="Lớp Học Đang Hoạt Động" value={overview.total_classrooms} icon={CalendarDays} color="bg-emerald-500" href="/classrooms" />
          <StatCard title="Học Phần" value={overview.total_courses} icon={BookOpen} color="bg-amber-500" href="/courses" />
          <StatCard title="Ghi Danh (Enrollment)" value={overview.total_enrollments} icon={UserCheck} color="bg-pink-500" href="/enrollments" />
          <StatCard title="Phân Công Giảng Dạy" value={overview.total_assignments} icon={ClipboardList} color="bg-teal-500" href="/assignments" />
        </div>
      )}

      {/* Charts & Lists */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <AttendanceChart data={data?.attendance_7days} />
        </div>
        <div className="space-y-6">
          <AttendanceDistribution dist={data?.attendance_distribution} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TopClassrooms data={data?.top_classrooms} />

        {/* Quick links */}
        <div className="bg-white rounded-xl border shadow-sm p-6">
          <h2 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-primary" /> Truy Cập Nhanh
          </h2>
          <div className="grid grid-cols-2 gap-3">
            {[
              { label: "Điểm danh hôm nay", href: "/attendance", icon: UserCheck, color: "text-emerald-600 bg-emerald-50 hover:bg-emerald-100" },
              { label: "Nhập điểm", href: "/enter-grades", icon: ClipboardList, color: "text-blue-600 bg-blue-50 hover:bg-blue-100" },
              { label: "Quản lý lớp", href: "/classrooms", icon: CalendarDays, color: "text-violet-600 bg-violet-50 hover:bg-violet-100" },
              { label: "Cấu hình HT", href: "/config", icon: BookOpen, color: "text-amber-600 bg-amber-50 hover:bg-amber-100" },
            ].map(item => {
              const Icon = item.icon;
              return (
                <Link
                  key={item.href}
                  to={item.href}
                  className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${item.color}`}
                >
                  <Icon className="h-5 w-5 shrink-0" />
                  <span className="text-sm font-medium leading-tight">{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
