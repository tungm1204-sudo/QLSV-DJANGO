"""
Enrollment Selectors
====================
Chứa logic truy vấn dữ liệu, chống N+1 bằng select_related/prefetch_related.
Chỉ chứa các hàm read-only.
"""
from django.db.models import QuerySet
from apps.curriculum.models import CourseOffering
from apps.enrollment.models import Enrollment

def get_available_course_offerings(semester_id: str = None) -> QuerySet[CourseOffering]:
    """
    Lấy danh sách các lớp học phần đang mở đăng ký.
    """
    queryset = CourseOffering.objects.filter(status='OPEN')
    if semester_id:
        queryset = queryset.filter(semester_id=semester_id)
        
    return queryset.select_related(
        'course', 
        'semester', 
        'lecturer', 
        'training_plan'
    ).prefetch_related('schedules')

def get_student_enrollments(student_id: str, semester_id: str = None) -> QuerySet[Enrollment]:
    """
    Lấy danh sách các lớp sinh viên đã đăng ký (hoặc đang chờ duyệt).
    """
    queryset = Enrollment.objects.filter(student_id=student_id)
    if semester_id:
        queryset = queryset.filter(course_offering__semester_id=semester_id)
        
    return queryset.select_related(
        'student',
        'course_offering',
        'course_offering__course',
        'course_offering__semester',
        'course_offering__lecturer',
        'course_offering__training_plan'
    ).prefetch_related('course_offering__schedules')

def get_course_offering_students(course_offering_id: str) -> QuerySet[Enrollment]:
    """
    Lấy danh sách sinh viên của một lớp học phần.
    """
    return Enrollment.objects.filter(
        course_offering_id=course_offering_id
    ).select_related(
        'student',
        'student__user',
        'student__major'
    )

def get_student_schedule(student_id: str, semester_id: str = None) -> list:
    """
    Lấy danh sách các buổi học (Schedule) của sinh viên trong một học kỳ.
    """
    enrollments = get_student_enrollments(student_id, semester_id)
    
    # Extract schedules from enrolled course offerings
    schedules = []
    for enrollment in enrollments:
        if enrollment.status in {Enrollment.StatusChoices.APPROVED, Enrollment.StatusChoices.PENDING}:
            # prefetch_related('course_offering__schedules') was used
            for schedule in enrollment.course_offering.schedules.all():
                schedules.append(schedule)
                
    return schedules
