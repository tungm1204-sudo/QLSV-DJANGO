from rest_framework import viewsets, permissions
from .models import (
    Semester, Grade, Course, Classroom, CourseAssignment,
    Attendance, ExamType, ExamResult
)
from .serializers import (
    SemesterSerializer, GradeSerializer, CourseSerializer,
    ClassroomSerializer, CourseAssignmentSerializer,
    AttendanceSerializer, ExamTypeSerializer, ExamResultSerializer
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


class CourseAssignmentViewSet(viewsets.ModelViewSet):
    queryset = CourseAssignment.objects.all().select_related("classroom", "course", "teacher__user")
    serializer_class = CourseAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all().select_related("student", "classroom")
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamTypeViewSet(viewsets.ModelViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all().select_related("student", "course", "semester", "exam_type")
    serializer_class = ExamResultSerializer
    permission_classes = [permissions.IsAuthenticated]
