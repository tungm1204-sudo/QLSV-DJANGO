"""
Enrollment Services
===================
Chứa logic nghiệp vụ lõi (Thêm/Sửa/Xóa Đăng ký, Đổi lớp, Phê duyệt).
BẮT BUỘC sử dụng `@transaction.atomic` và `select_for_update` khi cập nhật.
"""
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import F

from apps.enrollment.models import Enrollment
from apps.curriculum.models import CourseOffering, Schedule, Prerequisite
from apps.identity.models import AuditLog

def _create_audit_log(user, action: str, module: str, record_id: str, payload: dict):
    """
    Helper function để ghi log hành động người dùng.
    """
    AuditLog.objects.create(
        user=user,
        action=action,
        module=module,
        record_id=str(record_id),
        payload=payload
    )

def _check_schedule_overlap(student, new_course_offering):
    """
    Kiểm tra xem sinh viên có bị trùng lịch học khi đăng ký lớp mới không.
    Trả về True nếu bị trùng, ngược lại False.
    """
    # Lấy các lịch học của các lớp sinh viên đã đăng ký
    existing_schedules = Schedule.objects.filter(
        course_offering__enrollments__student=student,
        course_offering__semester=new_course_offering.semester
    )
    
    new_schedules = new_course_offering.schedules.all()
    
    for new_s in new_schedules:
        for ext_s in existing_schedules:
            if new_s.day_of_week == ext_s.day_of_week:
                # Công thức giao nhau của 2 khoảng [start1, end1] và [start2, end2]
                # Giao nhau khi: start1 <= end2 và end1 >= start2
                if new_s.start_period <= ext_s.end_period and new_s.end_period >= ext_s.start_period:
                    return True
    return False

def _check_prerequisites(student, course, bypass_prerequisite=False):
    """
    Kiểm tra môn tiên quyết (Hiện tại chỉ là mockup vì chưa có Module điểm số).
    Nếu bypass_prerequisite=True thì bỏ qua kiểm tra (dùng cho môi trường dev/test).
    """
    if bypass_prerequisite:
        return True
    
    # Lấy danh sách các môn bắt buộc
    prerequisites = Prerequisite.objects.filter(course=course).select_related('required_course')
    if not prerequisites.exists():
        return True
        
    # TODO: Ở Module 5, cần lấy bảng điểm của sinh viên (đã học và có điểm pass)
    # rồi so khớp với danh sách prerequisites này. Hiện tại ta return True để test.
    return True


@transaction.atomic
def enroll_student(student, course_offering_id: str, enrollment_type: str, user, bypass_prerequisite=False) -> Enrollment:
    """
    Xử lý nghiệp vụ đăng ký lớp học phần của sinh viên.
    1. Lock CourseOffering để tránh race condition khi tăng current_enrollment.
    2. Validate các quy tắc nghiệp vụ.
    3. Tạo bản ghi Enrollment.
    """
    try:
        # 1. Lock dòng CourseOffering để tính toán an toàn
        offering = CourseOffering.objects.select_for_update().get(id=course_offering_id)
    except CourseOffering.DoesNotExist:
        raise ValidationError("Lớp học phần không tồn tại.")
        
    # 2. Validate Trạng thái và Hạn đăng ký
    if offering.status not in ['OPEN']:
        raise ValidationError("Lớp học phần hiện không mở đăng ký.")
        
    if offering.registration_deadline and timezone.now() > offering.registration_deadline:
        raise ValidationError("Đã hết hạn đăng ký lớp học phần này.")

    # 3. Validate Sĩ số
    if offering.current_enrollment >= offering.max_capacity:
        raise ValidationError("Lớp học phần đã đạt sĩ số tối đa.")

    # 4. Kiểm tra đã đăng ký chưa
    if Enrollment.objects.filter(student=student, course_offering=offering).exists():
        raise ValidationError("Sinh viên đã đăng ký lớp học phần này.")
        
    # 5. Kiểm tra môn tiên quyết
    if not _check_prerequisites(student, offering.course, bypass_prerequisite):
        raise ValidationError(f"Sinh viên chưa đạt điều kiện tiên quyết cho môn {offering.course.code}.")

    # 6. Kiểm tra trùng lịch học
    if _check_schedule_overlap(student, offering):
        raise ValidationError("Lịch học của lớp học phần mới bị trùng với thời khóa biểu hiện tại.")

    # 7. Quyết định trạng thái dựa vào loại đăng ký
    # Nếu là học lại/học cải thiện/học vượt -> Cần phê duyệt (PENDING)
    status = Enrollment.StatusChoices.APPROVED
    if enrollment_type in [Enrollment.EnrollmentTypeChoices.RETAKE, 
                           Enrollment.EnrollmentTypeChoices.IMPROVEMENT, 
                           Enrollment.EnrollmentTypeChoices.ADVANCED]:
        status = Enrollment.StatusChoices.PENDING

    # 8. Cập nhật current_enrollment và Tạo Enrollment
    offering.current_enrollment = F('current_enrollment') + 1
    offering.save(update_fields=['current_enrollment'])

    enrollment = Enrollment.objects.create(
        student=student,
        course_offering=offering,
        enrollment_type=enrollment_type,
        status=status
    )
    
    # Reload để cập nhật giá trị F()
    offering.refresh_from_db()

    # 9. Ghi Audit Log
    _create_audit_log(
        user=user,
        action="ENROLL",
        module="Enrollment",
        record_id=enrollment.id,
        payload={"student_id": str(student.id), "course_offering_id": str(offering.id), "type": enrollment_type}
    )

    return enrollment


@transaction.atomic
def cancel_enrollment(enrollment_id: str, user) -> None:
    """
    Hủy đăng ký học phần (trong thời gian cho phép).
    """
    try:
        # Lock enrollment và offering
        enrollment = Enrollment.objects.select_for_update().select_related('course_offering').get(id=enrollment_id)
        offering = CourseOffering.objects.select_for_update().get(id=enrollment.course_offering_id)
    except Enrollment.DoesNotExist:
        raise ValidationError("Bản ghi đăng ký không tồn tại.")
        
    if enrollment.is_locked:
        raise ValidationError("Bản ghi đăng ký đã bị khóa, không thể hủy.")
        
    if offering.status == 'CLOSED':
        raise ValidationError("Lớp học phần đã chốt danh sách, không thể hủy đăng ký.")
        
    if offering.registration_deadline and timezone.now() > offering.registration_deadline:
        raise ValidationError("Đã hết hạn điều chỉnh lớp học phần này.")

    # Giảm sĩ số
    offering.current_enrollment = F('current_enrollment') - 1
    offering.save(update_fields=['current_enrollment'])
    
    student_id = enrollment.student_id
    offering_id = offering.id
    enrollment.delete()

    # Ghi log
    _create_audit_log(
        user=user,
        action="CANCEL_ENROLLMENT",
        module="Enrollment",
        record_id=enrollment_id,
        payload={"student_id": str(student_id), "course_offering_id": str(offering_id)}
    )

@transaction.atomic
def change_course_offering(enrollment_id: str, new_course_offering_id: str, user, bypass_prerequisite=False) -> Enrollment:
    """
    Đổi lớp học phần.
    Xóa đăng ký cũ, tạo đăng ký mới trong cùng một transaction.
    """
    try:
        enrollment = Enrollment.objects.select_related('student', 'course_offering').get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        raise ValidationError("Bản ghi đăng ký không tồn tại.")
        
    student = enrollment.student
    enrollment_type = enrollment.enrollment_type
    
    if enrollment.is_locked:
        raise ValidationError("Bản ghi đăng ký đã bị khóa, không thể đổi lớp.")
        
    # Hủy lớp cũ
    cancel_enrollment(enrollment_id, user)
    
    # Đăng ký lớp mới (sẽ thực hiện validate logic ở trong hàm này)
    try:
        new_enrollment = enroll_student(student, new_course_offering_id, enrollment_type, user, bypass_prerequisite)
    except ValidationError as e:
        # Reraise exception, transaction sẽ bị rollback (trả lại trạng thái cũ)
        raise e
        
    _create_audit_log(
        user=user,
        action="CHANGE_CLASS",
        module="Enrollment",
        record_id=new_enrollment.id,
        payload={
            'old_enrollment_id': str(enrollment.id),
            'new_enrollment_id': str(new_enrollment.id),
            'old_course_offering_id': str(enrollment.course_offering.id),
            'new_course_offering_id': str(new_course_offering_id)
        }
    )
        
    return new_enrollment

@transaction.atomic
def approve_enrollment(enrollment_id: str, is_approved: bool, user) -> Enrollment:
    """
    Duyệt các trường hợp đăng ký đặc biệt.
    """
    try:
        enrollment = Enrollment.objects.select_for_update().get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        raise ValidationError("Bản ghi đăng ký không tồn tại.")
        
    if enrollment.status != Enrollment.StatusChoices.PENDING:
        raise ValidationError("Chỉ có thể phê duyệt bản ghi ở trạng thái PENDING.")
        
    enrollment.status = Enrollment.StatusChoices.APPROVED if is_approved else Enrollment.StatusChoices.REJECTED
    enrollment.save(update_fields=['status'])
    
    # Nếu từ chối, ta có cần giảm sĩ số không?
    # Việc ghi nhận PENDING đã cộng sĩ số rồi (để xí chỗ). Nếu REJECTED thì phải giảm sĩ số lại.
    if not is_approved:
        offering = CourseOffering.objects.select_for_update().get(id=enrollment.course_offering_id)
        offering.current_enrollment = F('current_enrollment') - 1
        offering.save(update_fields=['current_enrollment'])
        
    _create_audit_log(
        user=user,
        action="APPROVE_ENROLLMENT",
        module="Enrollment",
        record_id=enrollment_id,
        payload={"is_approved": is_approved}
    )
    
    return enrollment

@transaction.atomic
def lock_enrollment_list(course_offering_id: str, user) -> CourseOffering:
    """
    Chốt danh sách lớp học phần.
    """
    try:
        offering = CourseOffering.objects.get(id=course_offering_id)
    except CourseOffering.DoesNotExist:
        raise ValidationError("Lớp học phần không tồn tại.")
        
    if offering.status != 'OPEN':
        raise ValidationError("Lớp học phần chưa mở, không thể chốt.")
        
    offering.status = 'CLOSED'
    offering.save(update_fields=['status'])
    
    _create_audit_log(
        user=user,
        action="LOCK_LIST",
        module="Enrollment",
        record_id=course_offering_id,
        payload={"action": "CLOSED"}
    )
    
    return offering
