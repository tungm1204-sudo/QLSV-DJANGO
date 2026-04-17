from rest_framework import viewsets, permissions
from .models import Department, TeacherProfile
from .serializers import DepartmentSerializer, TeacherProfileSerializer, TeacherCreateSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all().select_related("user", "department")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "mgv"

    def get_serializer_class(self):
        if self.action == "create":
            return TeacherCreateSerializer
        return TeacherProfileSerializer
