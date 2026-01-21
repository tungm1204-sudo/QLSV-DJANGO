from django.contrib import admin
from .models import Grade, Course, Classroom, ClassroomStudent, Attendance, ExamType, Exam, ExamResult

# Đăng ký các model của academics vào admin
admin.site.register(Grade)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade', 'description')
    search_fields = ('name',)
    list_filter = ('grade',)

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('section', 'grade', 'teacher', 'year', 'status')
    search_fields = ('section', 'teacher__fname', 'teacher__lname')
    list_filter = ('grade', 'year', 'status')
    raw_id_fields = ('teacher',)

@admin.register(ClassroomStudent)
class ClassroomStudentAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'student')
    search_fields = ('classroom__section', 'student__fname', 'student__lname')
    raw_id_fields = ('classroom', 'student')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'remark')
    list_filter = ('status', 'date')
    search_fields = ('student__fname', 'student__lname')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'start_date')
    list_filter = ('exam_type', 'start_date')
    search_fields = ('name',)

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'course', 'marks')
    search_fields = ('exam__name', 'student__fname', 'student__lname', 'course__name')
    list_filter = ('exam', 'course')

admin.site.register(ExamType)



