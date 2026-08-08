"""
Module HR Selectors
Xử lý các logic truy vấn (Query) đọc dữ liệu từ DB.
Bắt buộc dùng select_related/prefetch_related cho ForeignKey.
"""
from django.db.models import QuerySet
from .models import Student, Lecturer, Staff, StudentCertificate

class StudentSelector:
    @staticmethod
    def get_students() -> QuerySet[Student]:
        return Student.objects.select_related(
            'user', 'major', 'administrative_class', 'education_system', 'priority_category',
            'ethnicity', 'religion', 'nationality', 'admission_type', 'cohort'
        ).all()

    @staticmethod
    def get_student(student_id: str) -> Student:
        return Student.objects.select_related(
            'user', 'major', 'administrative_class', 'education_system', 'priority_category',
            'ethnicity', 'religion', 'nationality', 'admission_type', 'cohort'
        ).get(pk=student_id)

class LecturerSelector:
    @staticmethod
    def get_lecturers() -> QuerySet[Lecturer]:
        return Lecturer.objects.select_related(
            'user', 'department', 'degree', 'academic_title', 'ethnicity', 'religion', 'nationality'
        ).all()

    @staticmethod
    def get_lecturer(lecturer_id: str) -> Lecturer:
        return Lecturer.objects.select_related(
            'user', 'department', 'degree', 'academic_title', 'ethnicity', 'religion', 'nationality'
        ).get(pk=lecturer_id)

class StaffSelector:
    @staticmethod
    def get_staffs() -> QuerySet[Staff]:
        return Staff.objects.select_related(
            'user', 'department', 'position', 'degree', 'ethnicity', 'religion', 'nationality'
        ).all()

    @staticmethod
    def get_staff(staff_id: str) -> Staff:
        return Staff.objects.select_related(
            'user', 'department', 'position', 'degree', 'ethnicity', 'religion', 'nationality'
        ).get(pk=staff_id)

class StudentCertificateSelector:
    @staticmethod
    def get_certificates() -> QuerySet[StudentCertificate]:
        return StudentCertificate.objects.select_related('student__user').all()

    @staticmethod
    def get_certificate(certificate_id: str) -> StudentCertificate:
        return StudentCertificate.objects.select_related('student__user').get(pk=certificate_id)
