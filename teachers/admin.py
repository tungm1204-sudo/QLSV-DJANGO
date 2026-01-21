from django.contrib import admin
from .models import Teacher

# Đăng ký model Teacher vào Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'mobile', 'dob', 'status')
    search_fields = ('fname', 'lname', 'email', 'phone', 'mobile')
    list_filter = ('status',)
    list_per_page = 20


