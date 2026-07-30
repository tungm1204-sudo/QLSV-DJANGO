"""
Curriculum Services
"""
from django.db import transaction
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, TrainingPlan, CourseOffering, Schedule
from django.core.exceptions import ValidationError
from django.db.models import Q

@transaction.atomic
def create_course(**data) -> Course:
    obj = Course(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_course(obj: Course, **data) -> Course:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_course(obj: Course):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_training_program(**data) -> TrainingProgram:
    obj = TrainingProgram(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_training_program(obj: TrainingProgram, **data) -> TrainingProgram:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_training_program(obj: TrainingProgram):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_prerequisite(**data) -> Prerequisite:
    obj = Prerequisite(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_prerequisite(obj: Prerequisite, **data) -> Prerequisite:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_prerequisite(obj: Prerequisite):
    obj.delete()

@transaction.atomic
def create_equivalent_course(**data) -> EquivalentCourse:
    obj = EquivalentCourse(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_equivalent_course(obj: EquivalentCourse, **data) -> EquivalentCourse:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_equivalent_course(obj: EquivalentCourse):
    obj.delete()

# --- Training Plan Services ---
@transaction.atomic
def create_training_plan(**data) -> TrainingPlan:
    obj = TrainingPlan(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_training_plan(obj: TrainingPlan, **data) -> TrainingPlan:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_training_plan(obj: TrainingPlan):
    obj.delete()

@transaction.atomic
def duplicate_training_plan(plan: TrainingPlan, new_semester_id: str, new_name: str, user) -> TrainingPlan:
    """Sao chép toàn bộ Kế hoạch đào tạo và các Lớp học phần bên trong sang học kỳ mới"""
    new_plan = TrainingPlan.objects.create(
        name=new_name,
        semester_id=new_semester_id,
        department=plan.department,
        status='DRAFT',
        created_by=user
    )
    
    # Sao chép các Course Offering
    for offering in plan.course_offerings.all():
        CourseOffering.objects.create(
            training_plan=new_plan,
            course=offering.course,
            semester_id=new_semester_id,
            min_capacity=offering.min_capacity,
            max_capacity=offering.max_capacity,
            attendance_weight=offering.attendance_weight,
            midterm_weight=offering.midterm_weight,
            final_weight=offering.final_weight,
            status='PLANNED'
        )
    return new_plan

@transaction.atomic
def approve_training_plan(plan: TrainingPlan, approver, status: str) -> TrainingPlan:
    if status not in ['PENDING', 'APPROVED', 'REJECTED']:
        raise ValidationError("Trạng thái không hợp lệ")
    plan.status = status
    if status == 'APPROVED':
        plan.approved_by = approver
    plan.save(update_fields=['status', 'approved_by'])
    return plan

# --- Course Offering Services ---
@transaction.atomic
def create_course_offering(**data) -> CourseOffering:
    obj = CourseOffering(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_course_offering(obj: CourseOffering, **data) -> CourseOffering:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_course_offering(obj: CourseOffering):
    # Dùng status CANCELLED thay vì xóa cứng
    obj.status = 'CANCELLED'
    obj.save(update_fields=['status'])

# --- Schedule Services ---
@transaction.atomic
def create_schedule(course_offering: CourseOffering, **data) -> Schedule:
    room = data.get('room')
    day_of_week = data.get('day_of_week')
    start_period = data.get('start_period')
    end_period = data.get('end_period')

    if start_period > end_period:
        raise ValidationError("Tiết bắt đầu không thể lớn hơn tiết kết thúc")

    # 1. Kiểm tra trùng lịch Phòng học
    overlap_room = Schedule.objects.filter(
        room=room,
        day_of_week=day_of_week,
        course_offering__semester=course_offering.semester
    ).filter(
        Q(start_period__lte=end_period) & Q(end_period__gte=start_period)
    ).exists()

    if overlap_room:
        raise ValidationError(f"Phòng {room.name} đã có lịch học trùng vào thời gian này")

    # 2. Kiểm tra trùng lịch Giảng viên
    if course_offering.lecturer:
        overlap_lecturer = Schedule.objects.filter(
            course_offering__lecturer=course_offering.lecturer,
            day_of_week=day_of_week,
            course_offering__semester=course_offering.semester
        ).filter(
            Q(start_period__lte=end_period) & Q(end_period__gte=start_period)
        ).exists()

        if overlap_lecturer:
            raise ValidationError(f"Giảng viên {course_offering.lecturer.user.get_full_name()} đã có lịch dạy trùng vào thời gian này")

    obj = Schedule(course_offering=course_offering, **data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_schedule(obj: Schedule):
    obj.delete()


