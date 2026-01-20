from django.contrib import admin
from .models import Grade, Course, Classroom, ClassroomStudent, Attendance, ExamType, Exam, ExamResult

admin.site.register(Grade)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(ClassroomStudent)
admin.site.register(Attendance)
admin.site.register(ExamType)
admin.site.register(Exam)
admin.site.register(ExamResult)

