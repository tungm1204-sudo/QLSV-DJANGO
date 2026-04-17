from django.contrib import admin
from .models import Semester, Grade, Course, Classroom, CourseAssignment, Attendance, ExamType, ExamResult

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("name", "academic_year", "start_date", "is_current")

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "credits", "grade")

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ("name", "grade", "semester", "homeroom_teacher", "status")

admin.site.register(CourseAssignment)
admin.site.register(Attendance)
admin.site.register(ExamType)
admin.site.register(ExamResult)
