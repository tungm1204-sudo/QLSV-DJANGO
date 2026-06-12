from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import (
    Semester, Grade, Course, Classroom, CourseAssignment,
    Attendance, ExamType, ExamResult
)
from .serializers import (
    SemesterSerializer, GradeSerializer, CourseSerializer,
    ClassroomSerializer, CourseAssignmentSerializer,
    AttendanceSerializer, ExamTypeSerializer, ExamResultSerializer,
    BulkAttendanceSerializer
)


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
