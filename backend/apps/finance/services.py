from django.db import transaction
from django.utils import timezone
from datetime import date
from django.db.models import Sum

from apps.finance.models import StudentDebt, Receipt, TuitionRule, TuitionExemption
from apps.enrollment.models import Enrollment
from apps.hr.models import Student
from apps.master_data.models import Semester
import logging

logger = logging.getLogger(__name__)

@transaction.atomic
def calculate_student_debt(student_id, semester_id, due_date: date):
    """
    Tự động sinh hoặc cập nhật công nợ học phí cho sinh viên trong học kỳ.
    """
    student = Student.objects.get(id=student_id)
    semester = Semester.objects.get(id=semester_id)
    
    # 1. Tính tổng tín chỉ đã đăng ký
    enrollments = Enrollment.objects.filter(
        student_id=student_id,
        course_offering__semester_id=semester_id,
        is_locked=False
    )
    
    total_credits = 0
    for enr in enrollments:
        total_credits += enr.course_offering.course.credits
        
    if total_credits == 0:
        return None

    # 2. Tìm đơn giá học phí (TuitionRule)
    # Ưu tiên rule theo major, nếu không có lấy rule chung (major is null)
    rule = TuitionRule.objects.filter(
        academic_year=semester.academic_year,
        major=student.major
    ).first()
    
    if not rule:
        rule = TuitionRule.objects.filter(
            academic_year=semester.academic_year,
            major__isnull=True
        ).first()
        
    if not rule:
        raise ValueError("Chưa cấu hình đơn giá học phí cho năm học này.")
        
    tuition_fee = total_credits * rule.credit_price
    
    # 3. Tính toán miễn giảm
    discount_amount = 0
    exemption = TuitionExemption.objects.filter(
        student_id=student_id,
        semester_id=semester_id,
        status='APPROVED'
    ).first()
    
    if exemption:
        discount_amount = (tuition_fee * exemption.discount_percentage) / 100
        
    final_amount = tuition_fee - discount_amount
    
    # 4. Ghi nhận vào StudentDebt
    debt, created = StudentDebt.objects.get_or_create(
        student_id=student_id,
        semester_id=semester_id,
        defaults={
            'total_credits': total_credits,
            'tuition_fee': tuition_fee,
            'discount_amount': discount_amount,
            'final_amount': final_amount,
            'due_date': due_date,
            'status': 'UNPAID'
        }
    )
    
    if not created:
        debt.total_credits = total_credits
        debt.tuition_fee = tuition_fee
        debt.discount_amount = discount_amount
        debt.final_amount = final_amount
        
        # Cập nhật trạng thái
        if debt.paid_amount >= debt.final_amount:
            debt.status = 'PAID'
        elif debt.paid_amount > 0:
            debt.status = 'PARTIAL'
        else:
            debt.status = 'UNPAID'
            
        debt.save()
        
    return debt

@transaction.atomic
def process_payment(debt_id, amount, method, reference_code=None, staff_id=None):
    """
    Xử lý thanh toán công nợ (có khóa select_for_update để chống race condition)
    """
    debt = StudentDebt.objects.select_for_update().get(id=debt_id)
    
    if debt.status == 'PAID':
        raise ValueError("Công nợ này đã được thanh toán đủ.")
        
    if amount <= 0:
        raise ValueError("Số tiền thanh toán phải lớn hơn 0.")
        
    # Tạo phiếu thu
    receipt = Receipt.objects.create(
        student_id=debt.student_id,
        semester_id=debt.semester_id,
        debt=debt,
        amount=amount,
        payment_method=method,
        status='COMPLETED',
        reference_code=reference_code,
        created_by_id=staff_id
    )
    
    # Cập nhật công nợ
    debt.paid_amount += amount
    
    if debt.paid_amount >= debt.final_amount:
        debt.status = 'PAID'
    else:
        debt.status = 'PARTIAL'
        
    debt.save()
    return receipt

@transaction.atomic
def refund_tuition_for_cancelled_course(student_id, course_offering):
    """
    Hoàn tiền/giảm trừ công nợ khi lớp học phần bị hủy
    """
    debt = StudentDebt.objects.select_for_update().filter(
        student_id=student_id, 
        semester_id=course_offering.semester_id
    ).first()
    
    if not debt:
        return
        
    credits = course_offering.course.credits
    rule = TuitionRule.objects.filter(
        academic_year=course_offering.semester.academic_year,
        major=debt.student.major
    ).first() or TuitionRule.objects.filter(
        academic_year=course_offering.semester.academic_year,
        major__isnull=True
    ).first()
    
    if not rule:
        return
        
    reduce_amount = credits * rule.credit_price
    
    # Cập nhật lại công nợ
    debt.total_credits -= credits
    debt.tuition_fee -= reduce_amount
    
    if debt.discount_amount > 0:
        # Tính lại discount nếu có
        exemption = TuitionExemption.objects.filter(
            student_id=student_id,
            semester_id=course_offering.semester_id,
            status='APPROVED'
        ).first()
        if exemption:
            debt.discount_amount = (debt.tuition_fee * exemption.discount_percentage) / 100
            
    debt.final_amount = debt.tuition_fee - debt.discount_amount
    
    if debt.paid_amount >= debt.final_amount:
        debt.status = 'PAID'
        # Sinh phiếu hoàn tiền (REFUNDED) nếu paid > final
        refund_amount = debt.paid_amount - debt.final_amount
        if refund_amount > 0:
            Receipt.objects.create(
                student_id=student_id,
                semester_id=course_offering.semester_id,
                debt=debt,
                amount=refund_amount,
                payment_method='ONLINE', # Hoặc chuyển khoản
                status='REFUNDED',
                reference_code=f"REFUND_CO_{course_offering.id}"
            )
            debt.paid_amount = debt.final_amount
            
    elif debt.paid_amount > 0:
        debt.status = 'PARTIAL'
    else:
        debt.status = 'UNPAID'
        
    debt.save()

@transaction.atomic
def send_overdue_reminders():
    """
    Quét và gửi thông báo nhắc nợ (Job định kỳ)
    """
    from apps.notifications.models import Notification
    
    overdue_debts = StudentDebt.objects.select_for_update().filter(
        due_date__lt=timezone.now().date(),
        status__in=['UNPAID', 'PARTIAL']
    )
    
    count = 0
    for debt in overdue_debts:
        debt.status = 'OVERDUE'
        debt.save(update_fields=['status'])
        count += 1
        
        # Tạo thông báo
        Notification.objects.create(
            user=debt.student.user,
            title="Nhắc nhở công nợ học phí quá hạn",
            message=f"Công nợ học kỳ {debt.semester.semester_code} của bạn đã quá hạn. Số tiền còn nợ: {debt.final_amount - debt.paid_amount} VNĐ. Vui lòng thanh toán sớm nhất có thể.",
            type=Notification.TypeChoices.WARNING
        )
        
    return count


# ─── Miễn giảm & Gia hạn ──────────────────────────────────────────────────

@transaction.atomic
def approve_tuition_exemption(exemption_id: str, actor_id: str) -> TuitionExemption:
    """
    Phê duyệt hồ sơ miễn giảm học phí.
    WHY: Tránh viết logic approve trực tiếp trong View — giữ View mỏng.
    Nếu cần tính lại công nợ sau khi duyệt, logic nằm ở đây, không phải View.
    """
    exemption = TuitionExemption.objects.select_for_update().get(id=exemption_id)
    if exemption.status != 'PENDING':
        raise ValueError(f"Hồ sơ không ở trạng thái PENDING (hiện: {exemption.status}).")
    exemption.status = 'APPROVED'
    exemption.save(update_fields=['status'])
    logger.info("TuitionExemption %s approved by actor %s", exemption_id, actor_id)
    return exemption


@transaction.atomic
def reject_tuition_exemption(exemption_id: str, actor_id: str) -> TuitionExemption:
    """Từ chối hồ sơ miễn giảm học phí."""
    exemption = TuitionExemption.objects.select_for_update().get(id=exemption_id)
    if exemption.status != 'PENDING':
        raise ValueError(f"Hồ sơ không ở trạng thái PENDING (hiện: {exemption.status}).")
    exemption.status = 'REJECTED'
    exemption.save(update_fields=['status'])
    logger.info("TuitionExemption %s rejected by actor %s", exemption_id, actor_id)
    return exemption


from apps.finance.models import TuitionExtension  # noqa – import muộn để tránh circular

@transaction.atomic
def approve_tuition_extension(extension_id: str, approved_by_staff) -> TuitionExtension:
    """
    Phê duyệt gia hạn thời gian đóng học phí.
    Cập nhật due_date trên StudentDebt tương ứng.
    """
    ext = TuitionExtension.objects.select_for_update().get(id=extension_id)
    if ext.status != 'PENDING':
        raise ValueError(f"Yêu cầu không ở trạng thái PENDING (hiện: {ext.status}).")
    ext.status = 'APPROVED'
    ext.approved_by = approved_by_staff
    ext.save(update_fields=['status', 'approved_by'])

    # Cập nhật due_date của công nợ liên quan
    StudentDebt.objects.filter(
        student_id=ext.student_id,
        semester_id=ext.semester_id,
        status__in=['UNPAID', 'PARTIAL'],
    ).update(due_date=ext.new_due_date)

    logger.info("TuitionExtension %s approved, new due_date=%s", extension_id, ext.new_due_date)
    return ext


# ─── In biên lai ──────────────────────────────────────────────────────────

def build_receipt_html(receipt_id: str) -> str:
    """
    Tạo nội dung HTML biên lai thu học phí để in hoặc convert sang PDF.
    WHY: Logic render nằm ở Service, View chỉ wrap vào HttpResponse.
    """
    receipt = (
        Receipt.objects
        .select_related('student__user', 'student__major', 'processed_by__user')
        .get(id=receipt_id)
    )
    student = receipt.student
    processed_by = receipt.processed_by

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Biên lai học phí #{receipt.receipt_code}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h2 {{ text-align: center; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        td, th {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background: #f5f5f5; text-align: left; }}
        .footer {{ margin-top: 40px; display: flex; justify-content: space-between; }}
        .amount {{ font-size: 1.2em; font-weight: bold; color: #2c7a2c; }}
    </style>
</head>
<body>
    <h2>BIÊN LAI THU HỌC PHÍ</h2>
    <p style="text-align:center">Số biên lai: <strong>{receipt.receipt_code}</strong></p>
    <table>
        <tr><th>Họ và tên</th><td>{student.user.full_name}</td></tr>
        <tr><th>Mã sinh viên</th><td>{student.student_code}</td></tr>
        <tr><th>Ngành</th><td>{student.major.name if student.major else '—'}</td></tr>
        <tr><th>Số tiền</th><td class="amount">{receipt.amount:,.0f} VNĐ</td></tr>
        <tr><th>Hình thức thanh toán</th><td>{receipt.get_payment_method_display()}</td></tr>
        <tr><th>Ghi chú</th><td>{receipt.notes or '—'}</td></tr>
        <tr><th>Ngày thu</th><td>{receipt.created_at.strftime('%d/%m/%Y %H:%M')}</td></tr>
        <tr><th>Thu ngân</th><td>{processed_by.user.full_name if processed_by else '—'}</td></tr>
    </table>
    <div class="footer">
        <div><p>Người nộp</p><br><br><br><i>(Ký, ghi rõ họ tên)</i></div>
        <div style="text-align:center"><p>Thu ngân</p><br><br><br><i>(Ký, ghi rõ họ tên)</i></div>
    </div>
</body>
</html>"""
    return html
