from rest_framework import permissions

class IsAdminUserRole(permissions.BasePermission):
    """
    Chỉ cho phép những user có role là 'admin' (Academic Staff).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')

class IsTeacherRole(permissions.BasePermission):
    """
    Chỉ cho phép những user có role là 'teacher'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'teacher')

class IsStudentRole(permissions.BasePermission):
    """
    Chỉ cho phép những user có role là 'student'.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Tất cả user đã xác thực có quyền xem (GET, HEAD, OPTIONS).
    Chỉ có 'admin' mới có quyền tạo/sửa/xoá (POST, PUT, PATCH, DELETE).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'

class IsAdminOrTeacher(permissions.BasePermission):
    """
    Cho phép Admin hoặc Giảng viên truy cập. Thích hợp cho việc nhập điểm, điểm danh.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'teacher']
