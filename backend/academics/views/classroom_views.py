from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from accounts.permissions import IsAdminOrReadOnly
from ..models import Classroom, ClassroomStudent, CourseAssignment, Attendance
from ..serializers import ClassroomSerializer, ClassroomStudentSerializer, CourseAssignmentSerializer

class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.all().select_related("grade", "semester", "homeroom_teacher__user")
    serializer_class = ClassroomSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'teacher':
            from django.db.models import Q
            return qs.filter(Q(homeroom_teacher__user=user) | Q(assignments__teacher__user=user)).distinct()
        if user.role == 'student':
            return qs.filter(enrollments__student=user).distinct()
        return qs

    @action(detail=True, methods=["get"], url_path="attendance-sheet")
    def attendance_sheet(self, request, pk=None):
        classroom = self.get_object()
        date = request.query_params.get("date")
        if not date:
            return Response({"error": "Vui lòng cung cấp tham số 'date' (YYYY-MM-DD)"}, status=status.HTTP_400_BAD_REQUEST)
        
        enrollments = classroom.enrollments.select_related("student", "student__student_profile").all()
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
    queryset = ClassroomStudent.objects.all().select_related(
        "classroom", "student", "student__student_profile"
    )
    serializer_class = ClassroomStudentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["classroom", "student"]
    search_fields = ["student__first_name", "student__last_name", "student__student_profile__mssv"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'teacher':
            from django.db.models import Q
            return qs.filter(Q(classroom__homeroom_teacher__user=user) | Q(classroom__assignments__teacher__user=user)).distinct()
        if user.role == 'student':
            return qs.filter(classroom__enrollments__student=user).distinct()
        return qs

class CourseAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourseAssignment.objects.all().select_related("classroom", "course", "teacher__user")
    serializer_class = CourseAssignmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["classroom", "course", "teacher"]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_authenticated:
            return qs.none()
        if user.role == 'teacher':
            return qs.filter(teacher__user=user)
        if user.role == 'student':
            return qs.filter(classroom__enrollments__student=user).distinct()
        return qs
