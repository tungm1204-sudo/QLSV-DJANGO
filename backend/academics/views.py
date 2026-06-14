from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import (
    Semester, Grade, Course, Classroom, ClassroomStudent, CourseAssignment,
    Attendance, ExamType, ExamResult
)
from .serializers import (
    SemesterSerializer, GradeSerializer, CourseSerializer,
    ClassroomSerializer, ClassroomStudentSerializer, CourseAssignmentSerializer,
    AttendanceSerializer, ExamTypeSerializer, ExamResultSerializer,
    BulkAttendanceSerializer, BulkExamResultSerializer
)


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



class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [permissions.IsAuthenticated]


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related("grade")
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all().select_related("grade", "semester", "homeroom_teacher__user")
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="attendance-sheet")
    def attendance_sheet(self, request, pk=None):
        classroom = self.get_object()
        date = request.query_params.get("date")
        if not date:
            return Response({"error": "Vui lòng cung cấp tham số 'date' (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Lấy danh sách học sinh qua related_name 'enrollments'
        enrollments = classroom.enrollments.select_related("student", "student__student_profile").all()
        # Lấy điểm danh ngày đó
        attendances = Attendance.objects.filter(classroom=classroom, date=date)
        attendance_map = {att.student_id: att for att in attendances}
        
        result = []
        for enrollment in enrollments:
            student = enrollment.student
            att = attendance_map.get(student.id)
            student_profile = getattr(student, "student_profile", None)
            result.append({
                "student_id": student.id,
                "student_name": student.get_full_name(),
                "mssv": student_profile.mssv if student_profile else "",
                "status": att.status if att else Attendance.Status.PRESENT,
                "remark": att.remark if att else "",
                "is_recorded": bool(att)
            })
        
        return Response(result)


class ClassroomStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet quản lý việc Enrollment (ghi danh sinh viên vào lớp học).
    Hỗ trợ thêm/xóa sinh viên khỏi lớp, và xem danh sách sinh viên theo lớp.
    """
    queryset = ClassroomStudent.objects.all().select_related(
        "classroom", "student", "student__student_profile"
    )
    serializer_class = ClassroomStudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["classroom", "student"]
    search_fields = ["student__first_name", "student__last_name", "student__student_profile__mssv"]


class CourseAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourseAssignment.objects.all().select_related("classroom", "course", "teacher__user")
    serializer_class = CourseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["classroom", "course", "teacher"]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().select_related("student", "classroom")
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["date", "student", "classroom", "status"]

    @action(detail=False, methods=["post"], url_path="bulk-update")
    def bulk_update_attendance(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            attendances_data = serializer.validated_data.get('attendances', [])
            updated_count = 0
            created_count = 0
            
            for att_data in attendances_data:
                student = att_data.get('student')
                classroom = att_data.get('classroom')
                date = att_data.get('date')
                status_val = att_data.get('status')
                remark = att_data.get('remark', '')
                
                obj, created = Attendance.objects.update_or_create(
                    student=student,
                    classroom=classroom,
                    date=date,
                    defaults={'status': status_val, 'remark': remark}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            return Response({
                "message": f"Đã lưu điểm danh. Tạo mới {created_count}, cập nhật {updated_count}.",
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamTypeViewSet(viewsets.ModelViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all().select_related("student", "course", "semester", "exam_type")
    serializer_class = ExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="grade-sheet")
    def grade_sheet(self, request):
        classroom_id = request.query_params.get("classroom")
        course_id = request.query_params.get("course")
        semester_id = request.query_params.get("semester")
        exam_type_id = request.query_params.get("exam_type")
        
        if not all([classroom_id, course_id, semester_id, exam_type_id]):
            return Response({"error": "Vui lòng cung cấp đủ classroom, course, semester, exam_type"}, status=status.HTTP_400_BAD_REQUEST)
        
        from .models import ClassroomStudent
        enrollments = ClassroomStudent.objects.filter(classroom_id=classroom_id).select_related("student", "student__student_profile")
        
        results = ExamResult.objects.filter(
            course_id=course_id,
            semester_id=semester_id,
            exam_type_id=exam_type_id,
            student__in=[e.student for e in enrollments]
        )
        result_map = {res.student_id: res for res in results}
        
        data = []
        for enrollment in enrollments:
            student = enrollment.student
            res = result_map.get(student.id)
            student_profile = getattr(student, "student_profile", None)
            data.append({
                "student_id": student.id,
                "student_name": student.get_full_name(),
                "mssv": student_profile.mssv if student_profile else "",
                "marks": res.marks if res else "",
                "max_marks": res.max_marks if res else 10.0,
                "remarks": res.remarks if res else "",
                "is_recorded": bool(res)
            })
            
        return Response(data)

    @action(detail=False, methods=["post"], url_path="bulk-update")
    def bulk_update_grades(self, request):
        serializer = BulkExamResultSerializer(data=request.data)
        if serializer.is_valid():
            results_data = serializer.validated_data.get('results', [])
            updated_count = 0
            created_count = 0
            
            for res_data in results_data:
                student = res_data.get('student')
                course = res_data.get('course')
                semester = res_data.get('semester')
                exam_type = res_data.get('exam_type')
                marks = res_data.get('marks')
                max_marks = res_data.get('max_marks', 10.0)
                remarks = res_data.get('remarks', '')
                
                obj, created = ExamResult.objects.update_or_create(
                    student=student,
                    course=course,
                    semester=semester,
                    exam_type=exam_type,
                    defaults={'marks': marks, 'max_marks': max_marks, 'remarks': remarks}
                )
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                    
            return Response({
                "message": f"Đã lưu điểm. Tạo mới {created_count}, cập nhật {updated_count}.",
            }, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], url_path="student-gpa")
    def student_gpa(self, request):
        """
        Lấy điểm GPA của một sinh viên (có thể truyền student_id, hoặc mặc định lấy của user hiện tại).
        Chỉ tính GPA dựa trên những môn đã có kết quả.
        """
        student_id = request.query_params.get("student_id")
        if not student_id:
            if request.user.role == "student":
                student_id = request.user.id
            else:
                return Response({"error": "Vui lòng cung cấp student_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        from django.db.models import F, Sum, ExpressionWrapper, FloatField
        
        results = ExamResult.objects.filter(student_id=student_id).select_related('course', 'exam_type')
        
        course_scores = {}
        for r in results:
            c_id = r.course.id
            if c_id not in course_scores:
                course_scores[c_id] = {'credits': r.course.credits, 'total_weight': 0, 'weighted_score': 0}
            
            w = r.exam_type.weight
            score_10 = (r.marks / r.max_marks) * 10
            course_scores[c_id]['total_weight'] += w
            course_scores[c_id]['weighted_score'] += score_10 * w
            
        total_credits = 0
        total_gpa_score = 0
        
        course_details = []
        for c_id, data in course_scores.items():
            if data['total_weight'] > 0:
                final_score = data['weighted_score'] / data['total_weight']
                total_credits += data['credits']
                total_gpa_score += final_score * data['credits']
                course_details.append({
                    "course_id": c_id,
                    "credits": data['credits'],
                    "final_score": round(final_score, 2)
                })
                
        gpa_10 = total_gpa_score / total_credits if total_credits > 0 else 0
        gpa_4 = gpa_10 * 0.4  # Đơn giản hóa hệ 4
        
        return Response({
            "student_id": student_id,
            "total_credits": total_credits,
            "gpa_10": round(gpa_10, 2),
            "gpa_4": round(gpa_4, 2),
            "course_details": course_details
        })
