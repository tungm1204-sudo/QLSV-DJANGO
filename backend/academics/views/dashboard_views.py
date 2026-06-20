from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from ..models import Semester, Course, Classroom, ClassroomStudent, CourseAssignment, Attendance

class DashboardView(APIView):
    """
    API tổng hợp thống kê cho Dashboard.
    Trả về số liệu tổng quan của toàn hệ thống.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        # Đếm số lượng tổng quan
        total_students = User.objects.filter(role="student").count()
        total_teachers = User.objects.filter(role="teacher").count()
        total_classrooms = Classroom.objects.filter(status=True).count()
        total_courses = Course.objects.count()
        total_enrollments = ClassroomStudent.objects.count()
        total_assignments = CourseAssignment.objects.count()

        # Học kỳ hiện tại
        current_semester = Semester.objects.filter(is_current=True).first()
        current_semester_data = None
        if current_semester:
            current_semester_data = {
                "id": current_semester.id,
                "name": current_semester.name,
                "academic_year": current_semester.academic_year,
                "start_date": str(current_semester.start_date),
                "end_date": str(current_semester.end_date),
            }

        # Thống kê điểm danh 7 ngày gần nhất
        today = timezone.now().date()
        week_ago = today - timedelta(days=6)
        attendance_by_day = []
        for i in range(7):
            day = week_ago + timedelta(days=i)
            total_att = Attendance.objects.filter(date=day).count()
            present = Attendance.objects.filter(date=day, status="present").count()
            absent = Attendance.objects.filter(date=day, status="absent").count()
            late = Attendance.objects.filter(date=day, status="late").count()
            attendance_by_day.append({
                "date": str(day),
                "day_label": day.strftime("%d/%m"),
                "total": total_att,
                "present": present,
                "absent": absent,
                "late": late,
            })

        # Top 5 lớp có nhiều SV nhất
        top_classrooms = (
            ClassroomStudent.objects
            .values("classroom__id", "classroom__name")
            .annotate(student_count=Count("student"))
            .order_by("-student_count")[:5]
        )

        # Tỉ lệ điểm danh theo trạng thái (toàn hệ thống)
        att_stats = Attendance.objects.values("status").annotate(count=Count("id"))
        attendance_distribution = {item["status"]: item["count"] for item in att_stats}

        return Response({
            "overview": {
                "total_students": total_students,
                "total_teachers": total_teachers,
                "total_classrooms": total_classrooms,
                "total_courses": total_courses,
                "total_enrollments": total_enrollments,
                "total_assignments": total_assignments,
            },
            "current_semester": current_semester_data,
            "attendance_7days": attendance_by_day,
            "top_classrooms": list(top_classrooms),
            "attendance_distribution": attendance_distribution,
        })
