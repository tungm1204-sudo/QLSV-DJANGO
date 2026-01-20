from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from academics.models import Course, Classroom

@login_required
def dashboard(request):
    try:
        student_count = Student.objects.count()
    except:
        student_count = 0
        
    try:
        teacher_count = Teacher.objects.count()
    except:
        teacher_count = 0
        
    try:
        course_count = Course.objects.count()
    except:
        course_count = 0
        
    try:
        classroom_count = Classroom.objects.count()
    except:
        classroom_count = 0

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'classroom_count': classroom_count,
    }
    return render(request, 'core/dashboard.html', context)

