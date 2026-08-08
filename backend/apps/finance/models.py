"""
Các Model liên quan đến Module 7: Tài chính & Học phí
Bao gồm: TuitionRule, TuitionExemption, TuitionExtension, StudentDebt, Receipt.
"""
from django.db import models
import uuid

class TuitionRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_year = models.ForeignKey('master_data.AcademicYear', on_delete=models.CASCADE, related_name='tuition_rules')
    major = models.ForeignKey('master_data.Major', on_delete=models.CASCADE, null=True, blank=True, related_name='tuition_rules')
    credit_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Đơn giá 1 tín chỉ")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tuition_rules'
        unique_together = ('academic_year', 'major')
        ordering = ['-created_at']

class TuitionExemption(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='tuition_exemptions')
    priority_category = models.ForeignKey('master_data.PriorityCategory', on_delete=models.CASCADE, related_name='tuition_exemptions')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='tuition_exemptions')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tỷ lệ giảm giá (%)")
    document_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tuition_exemptions'
        ordering = ['-created_at']

class TuitionExtension(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='tuition_extensions')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='tuition_extensions')
    new_due_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    approved_by = models.ForeignKey('hr.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_extensions')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tuition_extensions'
        ordering = ['-created_at']

class StudentDebt(models.Model):
    STATUS_CHOICES = (
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partial'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='debts')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='debts')
    
    total_credits = models.IntegerField(default=0)
    tuition_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Học phí gốc")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Số tiền được giảm")
    final_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Số tiền phải đóng (gốc - giảm)")
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Số tiền đã đóng")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNPAID')
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'student_debts'
        unique_together = ('student', 'semester')
        ordering = ['-created_at']

class Receipt(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('ONLINE', 'Online Gateway'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('hr.Student', on_delete=models.CASCADE, related_name='receipts')
    semester = models.ForeignKey('master_data.Semester', on_delete=models.CASCADE, related_name='receipts')
    debt = models.ForeignKey(StudentDebt, on_delete=models.CASCADE, related_name='receipts')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reference_code = models.CharField(max_length=100, null=True, blank=True, help_text="Mã giao dịch / Mã cổng thanh toán")
    
    payment_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('hr.Staff', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_receipts', help_text="Cán bộ thu tiền (nếu đóng tiền mặt)")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'receipts'
        ordering = ['-payment_date']
