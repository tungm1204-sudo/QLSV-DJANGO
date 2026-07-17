"""
Master Data Services
====================
Chứa toàn bộ Business Logic liên quan đến thao tác (Create/Update/Delete) danh mục.
Tuyệt đối tuân thủ Service Layer: Validate rules, dùng @transaction.atomic để đảm bảo an toàn.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester

class DepartmentService:
    @staticmethod
    @transaction.atomic
    def delete_department(department: Department) -> None:
        """
        Xóa Khoa/Bộ môn.
        Why: Đảm bảo không xóa cứng đơn vị nếu đơn vị đó đang có đơn vị con, 
             hoặc đang quản lý một Ngành học (bảo vệ toàn vẹn dữ liệu).
        """
        if department.children.exists():
            raise ValidationError("Không thể xóa Khoa/Đơn vị đang có đơn vị con.")
        if department.majors.exists():
            raise ValidationError("Không thể xóa Khoa/Đơn vị đang quản lý Ngành học.")
        department.delete()

class MajorService:
    @staticmethod
    @transaction.atomic
    def delete_major(major: Major) -> None:
        """
        Xóa Ngành học.
        Why: Phải kiểm tra ràng buộc xem ngành này đã được gán môn học nào chưa 
             trước khi cho phép xóa (đảm bảo integrity).
        """
        if major.courses.exists():
            raise ValidationError("Không thể xóa Ngành học đã có Môn học thuộc Chương trình đào tạo.")
        major.delete()

class RoomService:
    @staticmethod
    @transaction.atomic
    def delete_room(room: Room) -> None:
        """
        Xóa Phòng học.
        Why: Bọc transaction để chuẩn bị cho việc sau này kiểm tra xem phòng 
             đã được gán vào Thời khóa biểu (schedules) nào chưa.
        """
        room.delete()

class PriorityCategoryService:
    @staticmethod
    @transaction.atomic
    def delete_category(category: PriorityCategory) -> None:
        """Xóa danh mục Đối tượng ưu tiên."""
        category.delete()

class ExamTypeService:
    @staticmethod
    @transaction.atomic
    def delete_exam_type(exam_type: ExamType) -> None:
        """Xóa danh mục Hình thức thi."""
        exam_type.delete()

class CohortService:
    @staticmethod
    @transaction.atomic
    def delete_cohort(cohort: Cohort) -> None:
        """Xóa Khóa học."""
        cohort.delete()

class SemesterService:
    @staticmethod
    @transaction.atomic
    def delete_semester(semester: Semester) -> None:
        """Xóa Học kỳ."""
        semester.delete()
