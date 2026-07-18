"""
Module HR Services
Chứa toàn bộ logic nghiệp vụ (Business Logic) cho phân hệ Quản lý Nhân sự.
Nằm ở Service Layer. Mọi thao tác ghi/sửa/xóa (Write) DB BẮT BUỘC phải nằm ở đây và dùng @transaction.atomic.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Student, Lecturer, Staff
from apps.identity.models import User

@transaction.atomic
def create_student(*, user_id: str, student_code: str, major_id: str = None, administrative_class_id: str = None, **kwargs) -> Student:
    """
    WHAT: Tạo hồ sơ sinh viên
    WHY: Bọc transaction.atomic vì tạo sinh viên có thể cần trigger thêm các bảng phụ.
    """
    user = User.objects.get(id=user_id)
    student = Student.objects.create(
        user=user,
        student_code=student_code,
        major_id=major_id,
        administrative_class_id=administrative_class_id,
        **kwargs
    )
    return student

@transaction.atomic
def update_student(student: Student, **data) -> Student:
    """
    WHAT: Cập nhật thông tin sinh viên
    WHY: Tách logic update vào service để View và Serializer mỏng, dễ bảo trì.
    """
    for field, value in data.items():
        setattr(student, field, value)
    student.save()
    return student

@transaction.atomic
def create_lecturer(*, user_id: str, lecturer_code: str, department_id: str, **kwargs) -> Lecturer:
    user = User.objects.get(id=user_id)
    lecturer = Lecturer.objects.create(
        user=user,
        lecturer_code=lecturer_code,
        department_id=department_id,
        **kwargs
    )
    return lecturer

@transaction.atomic
def create_staff(*, user_id: str, staff_code: str, department_id: str, **kwargs) -> Staff:
    user = User.objects.get(id=user_id)
    staff = Staff.objects.create(
        user=user,
        staff_code=staff_code,
        department_id=department_id,
        **kwargs
    )
    return staff
