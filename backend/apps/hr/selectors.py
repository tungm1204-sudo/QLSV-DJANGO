"""
Module HR Selectors
Chứa toàn bộ logic truy vấn (Read) cho phân hệ Quản lý Nhân sự.
Nằm ở Service Layer. Tuyệt đối không chứa logic Write.
BẤT CỨ KHI NÀO query có khóa ngoại (ForeignKey), BẮT BUỘC dùng .select_related() hoặc .prefetch_related() để chống N+1.
"""
from django.db.models import QuerySet
from .models import Student, Lecturer, Staff

def get_students() -> QuerySet[Student]:
    # WHY: Dùng select_related để lấy luôn thông tin User, Major, Class trong 1 query duy nhất, tránh N+1.
    return Student.objects.select_related(
        'user', 'major', 'administrative_class', 'education_system', 'priority_category'
    ).all()

def get_student(student_id: str) -> Student:
    # WHAT: Lấy chi tiết 1 sinh viên.
    return Student.objects.select_related(
        'user', 'major', 'administrative_class', 'education_system', 'priority_category'
    ).get(id=student_id)

def get_lecturers() -> QuerySet[Lecturer]:
    # WHY: Tương tự sinh viên, cần lấy thông tin user và department.
    return Lecturer.objects.select_related(
        'user', 'department'
    ).all()

def get_staffs() -> QuerySet[Staff]:
    return Staff.objects.select_related(
        'user', 'department'
    ).all()
