from django.contrib import admin
from .models import Student

# Đăng ký model Student vào trang quản trị Django Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'dob', 'email', 'status', 'parent')
    search_fields = ('fname', 'lname', 'email', 'phone', 'mobile')
    list_filter = ('status',)
    list_per_page = 20



