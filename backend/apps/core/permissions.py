from rest_framework import permissions

class IsAdminOrStaff(permissions.BasePermission):
    """
    Cho phép truy cập nếu user là Admin hoặc Staff.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )

class IsStudent(permissions.BasePermission):
    """
    Cho phép truy cập nếu user là Sinh viên.
    Kiểm tra bằng cách xem user có student_profile không.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'student_profile')
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Cho phép đọc cho mọi user đã xác thực, nhưng chỉ cho phép ghi (POST/PUT/PATCH/DELETE) đối với Admin/Staff.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )
