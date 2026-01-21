from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from teachers.models import Teacher
from academics.models import Course, Classroom

@login_required # Yêu cầu user phải đăng nhập mới xem được view này
def dashboard(request):
    """
    View Dashboard (Trang chủ sau khi đăng nhập).
    Hiển thị thống kê tổng quan của hệ thống.
    """
    try:
        student_count = Student.objects.count() # Đếm tổng sinh viên
    except:
        student_count = 0
        
    try:
        teacher_count = Teacher.objects.count() # Đếm tổng giáo viên
    except:
        teacher_count = 0
        
    try:
        course_count = Course.objects.count()   # Đếm tổng môn học
    except:
        course_count = 0
        
    try:
        classroom_count = Classroom.objects.count() # Đếm tổng lớp học
    except:
        classroom_count = 0

    context = {
        'student_count': student_count,
        'teacher_count': teacher_count,
        'course_count': course_count,
        'classroom_count': classroom_count,
    }
    return render(request, 'core/dashboard.html', context)

