from rest_framework import viewsets, permissions
from .models import Department, TeacherProfile
from .serializers import DepartmentSerializer, TeacherProfileSerializer, TeacherCreateSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """API CRUD cho Khoa / Bộ môn."""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeacherProfileViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho Hồ sơ Giảng viên.
    Business logic:
    - Dùng `lookup_field = 'mgv'` thay vì ID để URL thân thiện (VD: /api/teachers/profiles/GV001/).
    - Tương tự StudentProfileViewSet, phân biệt serializer theo action:
      create -> TeacherCreateSerializer (có user fields), còn lại -> TeacherProfileSerializer.
    """
    # select_related để tránh N+1 query khi serialize user và department
    queryset = TeacherProfile.objects.all().select_related("user", "department")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "mgv"  # Tìm kiếm theo Mã giảng viên thay vì ID

    def get_serializer_class(self):
        """
        Chức năng: Chọn serializer phù hợp theo action.
        Output: TeacherCreateSerializer khi tạo mới, TeacherProfileSerializer cho các action còn lại.
        """
        if self.action == "create":
            return TeacherCreateSerializer
        return TeacherProfileSerializer
