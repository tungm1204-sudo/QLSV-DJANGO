from typing import Optional, List, Tuple
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.enrollment.models import Enrollment
from apps.curriculum.models import CourseOffering
from apps.exams.models import GradeHistory, GradeReview, StudentAcademicRecord, ExamSession, ExamRoom
from apps.hr.models import Student
from apps.master_data.models import Semester
from apps.identity.models import User

def convert_10_to_4(score_10: Decimal) -> Tuple[Decimal, str]:
    """Quy đổi điểm hệ 10 sang hệ 4 và điểm chữ"""
    if score_10 is None:
        return Decimal('0.00'), 'F'
        
    s = float(score_10)
    if s >= 8.5: return Decimal('4.00'), 'A'
    if s >= 8.0: return Decimal('3.50'), 'B+'
    if s >= 7.0: return Decimal('3.00'), 'B'
    if s >= 6.5: return Decimal('2.50'), 'C+'
    if s >= 5.5: return Decimal('2.00'), 'C'
    if s >= 5.0: return Decimal('1.50'), 'D+'
    if s >= 4.0: return Decimal('1.00'), 'D'
    return Decimal('0.00'), 'F'

def calculate_enrollment_total_score(enrollment: Enrollment) -> Optional[Decimal]:
    """Tính điểm tổng kết học phần theo trọng số"""
    co = enrollment.course_offering
    
    # Nếu thiếu bất kỳ cột điểm nào, có thể trả về None hoặc tạm tính theo những gì đã có.
    # Thông thường, môn học chỉ có total_score khi cả 3 cột điểm đều có.
    a = enrollment.attendance_score or Decimal('0.00')
    m = enrollment.midterm_score or Decimal('0.00')
    f = enrollment.final_score or Decimal('0.00')
    
    # Check if final score exists, sometimes students just don't have it yet
    if enrollment.final_score is None:
        return None
        
    total = (a * co.attendance_weight) + (m * co.midterm_weight) + (f * co.final_weight)
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

@transaction.atomic
def update_enrollment_grades(
    enrollment: Enrollment, 
    changed_by: User,
    attendance: Optional[Decimal] = None,
    midterm: Optional[Decimal] = None,
    final: Optional[Decimal] = None,
    reason: str = "Nhập điểm"
) -> Enrollment:
    """Cập nhật điểm và lưu lịch sử"""
    if enrollment.is_locked:
        raise ValidationError("Bản ghi điểm này đã bị khóa.")
        
    history = GradeHistory(
        enrollment=enrollment,
        changed_by=changed_by,
        reason=reason,
        old_attendance=enrollment.attendance_score,
        new_attendance=attendance if attendance is not None else enrollment.attendance_score,
        old_midterm=enrollment.midterm_score,
        new_midterm=midterm if midterm is not None else enrollment.midterm_score,
        old_final=enrollment.final_score,
        new_final=final if final is not None else enrollment.final_score
    )
    
    if attendance is not None: enrollment.attendance_score = attendance
    if midterm is not None: enrollment.midterm_score = midterm
    if final is not None: enrollment.final_score = final
    
    enrollment.total_score = calculate_enrollment_total_score(enrollment)
    enrollment.save()
    history.save()
    
    return enrollment

@transaction.atomic
def lock_course_offering_grades(course_offering_id: str, locked: bool = True):
    """Khóa/Mở khóa toàn bộ điểm của 1 lớp học phần"""
    Enrollment.objects.filter(course_offering_id=course_offering_id).update(is_locked=locked)

@transaction.atomic
def import_grades_from_excel(course_offering_id: str, file_obj, changed_by: User):
    """Import điểm từ file Excel (chứa StudentCode, Attendance, Midterm, Final)"""
    try:
        df = pd.read_excel(file_obj)
    except Exception as e:
        raise ValidationError(f"Lỗi đọc file Excel: {e}")
        
    # Validation file structure
    required_cols = ['StudentCode']
    for col in required_cols:
        if col not in df.columns:
            raise ValidationError(f"File thiếu cột bắt buộc: {col}")
            
    for index, row in df.iterrows():
        student_code = str(row['StudentCode']).strip()
        try:
            enrollment = Enrollment.objects.get(
                course_offering_id=course_offering_id, 
                student__student_code=student_code
            )
            
            attendance = Decimal(str(row['Attendance'])) if 'Attendance' in df.columns and pd.notna(row['Attendance']) else None
            midterm = Decimal(str(row['Midterm'])) if 'Midterm' in df.columns and pd.notna(row['Midterm']) else None
            final = Decimal(str(row['Final'])) if 'Final' in df.columns and pd.notna(row['Final']) else None
            
            update_enrollment_grades(
                enrollment=enrollment,
                changed_by=changed_by,
                attendance=attendance,
                midterm=midterm,
                final=final,
                reason="Import từ Excel"
            )
        except Enrollment.DoesNotExist:
            continue # Bỏ qua sinh viên không có trong lớp
        except Exception as e:
            raise ValidationError(f"Lỗi xử lý sinh viên {student_code}: {e}")

@transaction.atomic
def calculate_student_semester_gpa(student_id: str, semester_id: str) -> StudentAcademicRecord:
    """Tính toán GPA học kỳ cho sinh viên"""
    enrollments = Enrollment.objects.filter(
        student_id=student_id,
        course_offering__semester_id=semester_id,
        total_score__isnull=False
    ).select_related('course_offering__course')
    
    total_10 = Decimal('0.00')
    total_4 = Decimal('0.00')
    total_credits = 0
    passed_credits = 0
    
    for enr in enrollments:
        score_10 = enr.total_score
        score_4, letter = convert_10_to_4(score_10)
        credits = enr.course_offering.course.credits
        
        total_10 += score_10 * credits
        total_4 += score_4 * credits
        total_credits += credits
        
        if score_4 > 0: # Điểm > F
            passed_credits += credits
            
    gpa_10 = (total_10 / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if total_credits > 0 else Decimal('0.00')
    gpa_4 = (total_4 / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if total_credits > 0 else Decimal('0.00')
    
    record, created = StudentAcademicRecord.objects.get_or_create(
        student_id=student_id,
        semester_id=semester_id
    )
    
    record.semester_gpa = gpa_10
    record.semester_gpa_4 = gpa_4
    record.semester_credits = passed_credits
    record.save()
    
    return record

@transaction.atomic
def calculate_student_cumulative_gpa(student_id: str) -> None:
    """Tính toán CPA (Cumulative GPA) toàn khóa cho sinh viên"""
    # Lấy tất cả hồ sơ học kỳ để cộng dồn
    records = StudentAcademicRecord.objects.filter(student_id=student_id).order_by('semester__start_date')
    
    # Tính từ các enrollments để chính xác hơn (chọn điểm cao nhất nếu học lại)
    # Tuy nhiên để đơn giản, ta tính trực tiếp từ tất cả các lớp đã học có điểm
    enrollments = Enrollment.objects.filter(
        student_id=student_id,
        total_score__isnull=False
    ).select_related('course_offering__course')
    
    # Dict lưu điểm cao nhất của từng môn
    best_scores = {} # course_id -> (score_10, score_4, credits)
    for enr in enrollments:
        course_id = enr.course_offering.course_id
        score_10 = enr.total_score
        score_4, _ = convert_10_to_4(score_10)
        credits = enr.course_offering.course.credits
        
        if course_id not in best_scores or best_scores[course_id][0] < score_10:
            best_scores[course_id] = (score_10, score_4, credits)
            
    total_10 = sum(val[0] * val[2] for val in best_scores.values())
    total_4 = sum(val[1] * val[2] for val in best_scores.values())
    total_credits = sum(val[2] for val in best_scores.values())
    
    cpa_10 = (total_10 / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if total_credits > 0 else Decimal('0.00')
    cpa_4 = (total_4 / total_credits).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if total_credits > 0 else Decimal('0.00')
    passed_credits = sum(val[2] for val in best_scores.values() if val[1] > 0)
    
    # Cập nhật CPA vào bản ghi học thuật mới nhất của sinh viên
    if records.exists():
        latest_record = records.last()
        latest_record.cumulative_gpa = cpa_10
        latest_record.cumulative_gpa_4 = cpa_4
        latest_record.cumulative_credits = passed_credits
        
        # Xếp loại học lực dựa trên CPA hệ 4
        standing = StudentAcademicRecord.AcademicStanding.AVERAGE
        if cpa_4 >= 3.6: standing = StudentAcademicRecord.AcademicStanding.EXCELLENT
        elif cpa_4 >= 3.2: standing = StudentAcademicRecord.AcademicStanding.GOOD
        elif cpa_4 >= 2.5: standing = StudentAcademicRecord.AcademicStanding.FAIR
        elif cpa_4 >= 2.0: standing = StudentAcademicRecord.AcademicStanding.AVERAGE
        elif cpa_4 >= 1.0: standing = StudentAcademicRecord.AcademicStanding.WEAK
        else: standing = StudentAcademicRecord.AcademicStanding.POOR
        
        latest_record.academic_standing = standing
        latest_record.save()

@transaction.atomic
def process_grade_review(grade_review: GradeReview, new_score: Decimal, staff_id: str) -> GradeReview:
    """Xử lý đơn phúc khảo, cập nhật điểm thi cuối kỳ (final_score) nếu được duyệt"""
    grade_review.status = GradeReview.StatusChoices.APPROVED
    grade_review.new_score = new_score
    grade_review.reviewed_by_id = staff_id
    grade_review.save()
    
    # Sinh GradeHistory và update Enrollment
    staff_user = grade_review.reviewed_by.user if grade_review.reviewed_by else None
    
    # Phúc khảo thường chỉ thay đổi điểm thi cuối kỳ
    update_enrollment_grades(
        enrollment=grade_review.enrollment,
        changed_by=staff_user,
        final=new_score,
        reason=f"Kết quả phúc khảo (Đơn ID: {grade_review.id})"
    )
    
    return grade_review

@transaction.atomic
def generate_exam_rooms(course_offering_id: str, exam_session_id: str, students_per_room: int, exam_date, start_time, end_time) -> List[ExamRoom]:
    """Tự động sinh phòng thi (ExamRoom) cho một lớp học phần dựa trên sĩ số thực tế"""
    course_offering = CourseOffering.objects.get(id=course_offering_id)
    exam_session = ExamSession.objects.get(id=exam_session_id)
    
    # Lấy danh sách SV có trong lớp
    enrollments = Enrollment.objects.filter(course_offering_id=course_offering_id).order_by('student__student_code').select_related('student')
    students = [e.student for e in enrollments]
    total_students = len(students)
    
    if total_students == 0:
        return []
        
    num_rooms = (total_students + students_per_room - 1) // students_per_room
    
    created_rooms = []
    student_idx = 0
    from apps.exams.models import StudentExamRoom
    
    for i in range(num_rooms):
        room = ExamRoom.objects.create(
            exam_session=exam_session,
            course_offering=course_offering,
            exam_date=exam_date,
            start_time=start_time,
            end_time=end_time,
            capacity=students_per_room
        )
        created_rooms.append(room)
        
        # Gán sinh viên vào phòng
        room_students = students[student_idx : student_idx + students_per_room]
        StudentExamRoom.objects.bulk_create([
            StudentExamRoom(exam_room=room, student=s) for s in room_students
        ])
        student_idx += students_per_room
    
    return created_rooms

def process_academic_warnings(semester_id: str):
    """Xử lý cảnh báo học vụ cho kỳ học được chỉ định"""
    # Lấy sinh viên có CPA dưới ngưỡng (ví dụ: < 1.0)
    records = StudentAcademicRecord.objects.filter(
        semester_id=semester_id,
        cumulative_gpa_4__lt=1.0
    ).select_related('student')
    
    from apps.notifications.services import create_notification
    
    for record in records:
        student = record.student
        msg = f"Cảnh báo học vụ: Điểm trung bình tích lũy của bạn hiện tại là {record.cumulative_gpa_4} (Dưới mức 1.0). Vui lòng liên hệ CVHT để được tư vấn."
        create_notification(
            user=student.user,
            title="CẢNH BÁO HỌC VỤ",
            message=msg,
            type='WARNING',
            related_link=None
        )
        
        # Nếu SV có cố vấn học tập trong kỳ này thì báo cho cố vấn
        from apps.affairs.models import AdvisingSession
        # Lấy CVHT của sv (Giả sử ta không lưu cứng Cố vấn trên Sinh viên, mà quản lý qua lớp hoặc có the record AdvisingSession)
        # Tạm thời chỉ gửi cho sinh viên.
        
    return len(records)
