from rest_framework import viewsets
from accounts.permissions import IsAdminOrReadOnly
from ..models import Semester, Grade, Course
from ..serializers import SemesterSerializer, GradeSerializer, CourseSerializer

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    permission_classes = [IsAdminOrReadOnly]

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrReadOnly]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().select_related("grade")
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
