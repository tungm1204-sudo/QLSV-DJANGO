"""
Curriculum Services
===================
Tầng xử lý Business Logic (Create/Update/Delete) cho Module Đào tạo.
Bảo vệ tính toàn vẹn dữ liệu.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal
from .models import Course, TrainingProgram, Prerequisite, TrainingPlan, CourseOffering, Schedule

class CourseService:
    @staticmethod
    @transaction.atomic
    def delete_course(course: Course) -> None:
        """
        Xóa Môn học.
        Why: Bắt buộc kiểm tra ràng buộc logic xem môn này có đang bị dùng làm 
             môn tiên quyết cho môn khác hay không trước khi xóa.
        """
        if course.prerequisites.exists() or course.required_by.exists():
            raise ValidationError("Không thể xóa môn học đang có ràng buộc làm môn tiên quyết.")
        course.delete()

class TrainingProgramService:
    @staticmethod
    @transaction.atomic
    def delete_training_program(program: TrainingProgram) -> None:
        """Xóa Chương trình đào tạo."""
        program.delete()

class PrerequisiteService:
    @staticmethod
    @transaction.atomic
    def delete_prerequisite(prerequisite: Prerequisite) -> None:
        """Xóa điều kiện tiên quyết."""
        prerequisite.delete()

class TrainingPlanService:
    @staticmethod
    @transaction.atomic
    def clone_plan(source_plan: TrainingPlan, new_name: str, new_semester, created_by) -> TrainingPlan:
        """
        Sao chép kế hoạch đào tạo từ một kế hoạch cũ (bao gồm cả các lớp học phần dự kiến).
        Why: Giúp Giáo vụ tiết kiệm thời gian lập kế hoạch cho học kỳ mới.
        """
        new_plan = TrainingPlan.objects.create(
            name=new_name,
            semester=new_semester,
            department=source_plan.department,
            status='DRAFT',
            created_by=created_by
        )
        
        # Clone các course offerings
        for offering in source_plan.course_offerings.all():
            CourseOffering.objects.create(
                training_plan=new_plan,
                course=offering.course,
                semester=new_semester,
                lecturer=None, # Kế hoạch mới chưa có giảng viên
                min_capacity=offering.min_capacity,
                max_capacity=offering.max_capacity,
                attendance_weight=offering.attendance_weight,
                midterm_weight=offering.midterm_weight,
                final_weight=offering.final_weight,
                status='PLANNED'
            )
        return new_plan

    @staticmethod
    @transaction.atomic
    def approve_plan(plan: TrainingPlan, approved_by) -> TrainingPlan:
        """Phê duyệt kế hoạch."""
        plan.status = 'APPROVED'
        plan.approved_by = approved_by
        plan.save()
        return plan

class CourseOfferingService:
    @staticmethod
    @transaction.atomic
    def create_offering(data: dict) -> CourseOffering:
        """Tạo lớp học phần mới và validate trọng số điểm."""
        att = Decimal(str(data.get('attendance_weight', 0.1)))
        mid = Decimal(str(data.get('midterm_weight', 0.2)))
        fin = Decimal(str(data.get('final_weight', 0.7)))
        if att + mid + fin != Decimal('1.00'):
            raise ValidationError("Tổng trọng số điểm chuyên cần, giữa kỳ, cuối kỳ phải bằng 1.00")
        
        return CourseOffering.objects.create(**data)

    @staticmethod
    @transaction.atomic
    def assign_lecturer(offering: CourseOffering, lecturer) -> CourseOffering:
        """
        Phân công giảng viên.
        Why: Phải kiểm tra xem giảng viên này có bị trùng lịch dạy không.
        """
        if not lecturer:
            offering.lecturer = None
            offering.save()
            return offering

        # Lấy tất cả lịch của lớp hiện tại
        current_schedules = offering.schedules.all()
        if not current_schedules:
            # Nếu lớp chưa có lịch thì cứ phân công thoải mái
            offering.lecturer = lecturer
            offering.save()
            return offering

        # Tìm các lớp khác mà giảng viên này đang dạy trong cùng học kỳ
        other_offerings = CourseOffering.objects.filter(
            lecturer=lecturer, 
            semester=offering.semester
        ).exclude(id=offering.id)

        # Kiểm tra trùng lịch với từng buổi học của lớp hiện tại
        for schedule in current_schedules:
            conflicts = Schedule.objects.filter(
                course_offering__in=other_offerings,
                day_of_week=schedule.day_of_week,
            ).filter(
                # Logic trùng tiết: (start1 <= end2) AND (end1 >= start2)
                Q(start_period__lte=schedule.end_period) & Q(end_period__gte=schedule.start_period)
            )
            if conflicts.exists():
                raise ValidationError(f"Giảng viên bị trùng lịch dạy vào {schedule.get_day_of_week_display()}, tiết {schedule.start_period}-{schedule.end_period}.")
        
        offering.lecturer = lecturer
        offering.save()
        return offering

class ScheduleService:
    @staticmethod
    @transaction.atomic
    def create_schedule(data: dict) -> Schedule:
        """
        Thêm lịch học.
        Why: Phải kiểm tra xem phòng học đã bị chiếm dụng chưa.
        """
        day_of_week = data['day_of_week']
        start_period = data['start_period']
        end_period = data['end_period']
        room = data['room']
        semester_id = data['course_offering'].semester_id

        # Tìm các lịch học cùng phòng, cùng học kỳ
        conflicts = Schedule.objects.filter(
            room=room,
            day_of_week=day_of_week,
            course_offering__semester_id=semester_id
        ).filter(
            Q(start_period__lte=end_period) & Q(end_period__gte=start_period)
        )
        if conflicts.exists():
            raise ValidationError(f"Phòng {room} đã có lớp học vào {day_of_week}, tiết {start_period}-{end_period}.")
            
        return Schedule.objects.create(**data)
