from django.contrib import admin
from .models import Semester, Grade, Course, Classroom, CourseAssignment, Attendance, ExamType, ExamResult

# Đăng ký các model vào Django Admin Panel với cấu hình hiển thị cột tuỳ chỉnh

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    # Hiển thị thêm cờ `is_current` để dễ nhận biết học kỳ đang diễn ra
    list_display = ("name", "academic_year", "start_date", "is_current")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Hiển thị mã môn và khối để tra cứu nhanh
    list_display = ("code", "name", "credits", "grade")

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    # Hiển thị giảng viên chủ nhiệm và trạng thái hoạt động để quản trị dễ dàng
    list_display = ("name", "grade", "semester", "homeroom_teacher", "status")

# Các model này chỉ cần giao diện mặc định, chưa cần tuỳ biến admin
admin.site.register(CourseAssignment)
admin.site.register(Attendance)
admin.site.register(ExamType)
admin.site.register(ExamResult)
