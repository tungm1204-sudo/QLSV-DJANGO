from django.contrib import admin
from .models import Parent, StudentProfile

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    """Hiển thị danh sách phụ huynh với thông tin liên lạc để tra cứu nhanh."""
    list_display = ("fname", "lname", "mobile", "status")

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """Hiển thị danh sách sinh viên — mssv dùng để tra cứu và phân biệt."""
    list_display = ("user", "mssv", "dob", "gender", "status")
