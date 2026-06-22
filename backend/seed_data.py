import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qlsv.settings')
django.setup()

from accounts.models import User
from students.models import StudentProfile
from teachers.models import TeacherProfile, Department
from academics.models import Course, Semester, Classroom, Grade, ClassroomStudent
from finance.models import TuitionFee, TuitionFeeDetail

def run():
    print("Xóa dữ liệu cũ (nếu có)...")
    User.objects.all().delete()
    Department.objects.all().delete()
    Grade.objects.all().delete()
    Semester.objects.all().delete()

    print("Tạo Khoa...")
    d_it = Department.objects.create(name="Công nghệ thông tin", code="CNTT")
    d_ec = Department.objects.create(name="Kinh tế", code="KT")

    print("Tạo Năm học & Học kỳ...")
    grade_1 = Grade.objects.create(name="Năm 1")
    sem_1 = Semester.objects.create(name="HK1", academic_year="2026-2027", start_date="2026-09-01", end_date="2027-01-30", is_current=True)

    print("Tạo Giảng viên...")
    def create_teacher(username, first_name, last_name, dept, mgv):
        user = User.objects.create_user(username=username, password='123456', role='teacher', first_name=first_name, last_name=last_name)
        TeacherProfile.objects.create(
            user=user, 
            department=dept, 
            mgv=mgv,
            dob='1980-01-01',
            degree='phd'
        )
        return user
    
    t1 = create_teacher('gv_nguyen', 'Nguyễn Văn', 'Giảng', d_it, 'GV001')
    t2 = create_teacher('gv_tran', 'Trần Thị', 'Viên', d_ec, 'GV002')

    print("Tạo Admin...")
    User.objects.create_superuser('admin', 'admin@example.com', '123456', role='admin')

    print("Tạo Môn học...")
    c_math = Course.objects.create(code="MATH101", name="Toán cao cấp", credits=3, grade=grade_1)
    c_cpp = Course.objects.create(code="IT102", name="Lập trình C++", credits=4, grade=grade_1)

    print("Tạo Lớp sinh hoạt...")
    class_1 = Classroom.objects.create(name="10IT1", grade=grade_1, semester=sem_1, homeroom_teacher=t1.teacher_profile)

    print("Tạo Sinh viên...")
    def create_student(username, first_name, last_name, mssv):
        user = User.objects.create_user(username=username, password='123456', role='student', first_name=first_name, last_name=last_name)
        StudentProfile.objects.create(
            user=user,
            mssv=mssv,
            dob='2005-01-01',
            status=True
        )
        # Gán sinh viên vào lớp
        ClassroomStudent.objects.create(classroom=class_1, student=user)
        return user

    s1 = create_student('sv_tuan', 'Lê Anh', 'Tuấn', 'SV001')
    s2 = create_student('sv_mai', 'Phạm Ngọc', 'Mai', 'SV002')
    s3 = create_student('sv_hung', 'Vũ Đức', 'Hùng', 'SV003')

    print("Tạo Dữ liệu Học phí...")
    students = [s1, s2, s3]
    for user in students:
        st_profile = user.student_profile
        fee = TuitionFee.objects.create(
            student=st_profile,
            semester='HK1 - 2026',
            total_credits=7,
            total_amount=3500000,
            status='UNPAID'
        )
        TuitionFeeDetail.objects.create(tuition_fee=fee, course_name=c_math.name, course_code=c_math.code, credits=c_math.credits, amount=1500000)
        TuitionFeeDetail.objects.create(tuition_fee=fee, course_name=c_cpp.name, course_code=c_cpp.code, credits=c_cpp.credits, amount=2000000)

    print("Đã tạo dữ liệu mẫu thành công!")

if __name__ == '__main__':
    run()
