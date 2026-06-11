from django.contrib import admin
from .models import Department, TeacherProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Hiển thị mã và tên khoa để quản trị nhanh."""
    list_display = ("code", "name")

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """Hiển thị thông tin chính của giảng viên, bao gồm khoa và bằng cấp để tra cứu hiệu quả."""
    list_display = ("user", "mgv", "department", "degree", "status")
