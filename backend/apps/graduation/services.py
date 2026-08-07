from django.db import transaction
from .models import GraduationCondition, GraduationSession, GraduationCandidate, Diploma
from apps.hr.models import Student, StudentCertificate
from apps.exams.models import StudentAcademicRecord

@transaction.atomic
def check_graduation_conditions(student_id):
    """
    Hàm kiểm tra sinh viên có đủ điều kiện tốt nghiệp không.
    Trả về dict: {'is_eligible': bool, 'total_credits': int, 'gpa': float, 'missing_conditions': list}
    """
    student = Student.objects.get(id=student_id)
    major = student.major
    cohort = student.administrative_class.cohort if student.administrative_class else None
    
    # 1. Tìm điều kiện tốt nghiệp áp dụng cho ngành và khóa này
    condition = GraduationCondition.objects.filter(major=major, cohort=cohort, is_active=True).first()
    if not condition:
        # Fallback to general condition for the major if cohort specific doesn't exist
        condition = GraduationCondition.objects.filter(major=major, cohort__isnull=True, is_active=True).first()
        
    if not condition:
        return {
            'is_eligible': False,
            'total_credits': 0,
            'gpa': 0.0,
            'missing_conditions': ['Không tìm thấy cấu hình điều kiện tốt nghiệp cho ngành học này.']
        }
        
    missing_conditions = []
    
    # 2. Lấy kết quả học tập mới nhất
    latest_record = StudentAcademicRecord.objects.filter(student=student).order_by('-semester__start_date').first()
    
    total_credits = latest_record.cumulative_credits if latest_record else 0
    gpa = latest_record.cumulative_gpa_4 if latest_record else 0.0
    
    # Check tín chỉ
    if total_credits < condition.total_credits_required:
        missing_conditions.append(f'Thiếu tín chỉ tích lũy (Hiện tại: {total_credits}/{condition.total_credits_required})')
        
    # Check GPA
    if gpa < condition.min_gpa:
        missing_conditions.append(f'GPA chưa đạt yêu cầu (Hiện tại: {gpa}/{condition.min_gpa})')
        
    # 3. Check chứng chỉ
    required_certs = condition.required_certificates
    if required_certs:
        student_certs = StudentCertificate.objects.filter(student=student, status='APPROVED').values_list('certificate_type', flat=True)
        for req_cert in required_certs:
            if req_cert not in student_certs:
                missing_conditions.append(f'Thiếu chứng chỉ bắt buộc: {req_cert}')
                
    is_eligible = len(missing_conditions) == 0
    
    return {
        'is_eligible': is_eligible,
        'total_credits': total_credits,
        'gpa': gpa,
        'missing_conditions': missing_conditions
    }

@transaction.atomic
def process_credit_transfer(student_id, old_program_id, new_program_id):
    """
    Chuyển đổi tín chỉ khi sinh viên đổi ngành/chương trình đào tạo.
    (Giả lập thao tác sao chép dữ liệu Enrollment và Điểm)
    """
    # Logic thực tế sẽ đọc từ bảng curriculum_equivalent_courses
    # Lấy các môn học sinh viên đã qua ở program cũ,
    # Nếu có ánh xạ (EquivalentCourse) sang môn mới ở program mới thì tạo bản ghi.
    
    # Do module này tập trung vào xét tốt nghiệp, hàm này làm placeholder
    # hoặc xử lý logic cơ bản.
    
    return {'status': 'success', 'transferred_courses': 0}
