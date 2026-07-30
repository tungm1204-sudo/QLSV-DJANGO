import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.exceptions import ValidationError
from apps.curriculum.models import Course, CourseOffering, Schedule, TrainingPlan
from apps.enrollment.models import Enrollment
from apps.hr.models import Student, Lecturer
from apps.master_data.models import Room, Semester, Department, Major
from apps.enrollment.services import enroll_student, change_course_offering
from django.contrib.auth import get_user_model
User = get_user_model()

def run_tests():
    print("--- Bắt đầu test Module 4 ---")
    
    # 1. Setup Data
    user, _ = User.objects.get_or_create(email='test@example.com', defaults={'full_name': 'Test User'})
    department, _ = Department.objects.get_or_create(code='DIT', name='Khoa CNTT')
    major, _ = Major.objects.get_or_create(code='IT', name='Công nghệ thông tin', defaults={'department': department})
    from apps.master_data.models import AcademicYear, Building, Campus
    academic_year, _ = AcademicYear.objects.get_or_create(code='2627')
    from datetime import date
    semester, _ = Semester.objects.get_or_create(code='HK1_2627', defaults={'academic_year': academic_year, 'season': 'HK1', 'is_current': True, 'start_date': date(2026, 9, 1), 'end_date': date(2027, 1, 31)})
    campus, _ = Campus.objects.get_or_create(code='CS1', defaults={'name': 'Cơ sở 1'})
    building, _ = Building.objects.get_or_create(code='A1', defaults={'name': 'Tòa A1', 'campus': campus})
    room, _ = Room.objects.get_or_create(code='P101', defaults={'building': building, 'type': 'THEORY', 'capacity': 50, 'floor': 1})
    course, _ = Course.objects.get_or_create(code='IT101', defaults={'name': 'Lập trình cơ bản', 'credits': 3, 'major': major})
    department, _ = Department.objects.get_or_create(code='DIT', defaults={'name': 'Khoa CNTT'})
    student, _ = Student.objects.get_or_create(student_code='SV001', defaults={'user': user, 'status': 'STUDYING', 'major': major})
    lecturer, _ = Lecturer.objects.get_or_create(lecturer_code='GV001', defaults={'user': user, 'department': department})
    
    plan, _ = TrainingPlan.objects.get_or_create(name='Kế hoạch IT HK1', semester=semester, status='APPROVED', defaults={'department': department})
    
    offering, _ = CourseOffering.objects.get_or_create(
        training_plan=plan,
        course=course,
        semester=semester,
        lecturer=lecturer,
        min_capacity=10,
        max_capacity=50,
        status='OPEN',
        current_enrollment=0
    )
    
    offering_full, _ = CourseOffering.objects.get_or_create(
        training_plan=plan,
        course=course,
        semester=semester,
        lecturer=lecturer,
        min_capacity=10,
        max_capacity=1, # Max 1
        status='OPEN',
        current_enrollment=1 # Đã full
    )

    # Xóa schedule cũ nếu có
    Schedule.objects.filter(course_offering=offering).delete()
    
    # Tạo schedule
    from apps.curriculum.services import create_schedule
    
    # Test tạo lịch trùng phòng
    try:
        sch1 = create_schedule(offering, room=room, day_of_week='MONDAY', start_period=1, end_period=3)
        print("[PASS] Tạo lịch học 1 thành công")
        
        # Tạo lịch 2 trùng phòng và thời gian
        create_schedule(offering, room=room, day_of_week='MONDAY', start_period=2, end_period=4)
        print("[FAIL] Cho phép tạo lịch học trùng phòng!")
    except ValidationError as e:
        print("[PASS] Đã block tạo lịch học trùng phòng:", e.messages)

    # Cleanup Enrollments
    Enrollment.objects.filter(student=student).delete()
    
    # Test đăng ký lớp
    try:
        enr = enroll_student(student, offering.id, 'NORMAL', user, bypass_prerequisite=True)
        print("[PASS] Đăng ký học phần thành công")
    except ValidationError as e:
        print("[FAIL] Đăng ký thất bại:", e)
        
    # Test đăng ký quá sĩ số
    try:
        enr_fail = enroll_student(student, offering_full.id, 'NORMAL', user, bypass_prerequisite=True)
        print("[FAIL] Cho phép đăng ký khi đã full!")
    except ValidationError as e:
        print("[PASS] Đã block đăng ký khi lớp full:", e.messages)
        
    print("--- Hoàn tất test ---")

if __name__ == '__main__':
    run_tests()
