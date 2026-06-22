from django.db import models
from students.models import StudentProfile

class TuitionConfig(models.Model):
    cost_per_credit = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Đơn giá/tín chỉ")
    effective_date = models.DateField(auto_now_add=True, verbose_name="Ngày áp dụng")

    class Meta:
        verbose_name = "Cấu hình học phí"
        verbose_name_plural = "Cấu hình học phí"

    def __str__(self):
        return f"{self.cost_per_credit} đ (từ {self.effective_date})"


class TuitionFee(models.Model):
    STATUS_CHOICES = [
        ('UNPAID', 'Chưa nộp'),
        ('PAID', 'Đã nộp'),
        ('OVERDUE', 'Nợ'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='tuition_fees', verbose_name="Sinh viên")
    semester = models.CharField(max_length=20, verbose_name="Học kỳ")
    total_credits = models.IntegerField(verbose_name="Tổng tín chỉ")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng tiền")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID', verbose_name="Trạng thái")
    due_date = models.DateField(verbose_name="Hạn nộp", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Học phí"
        verbose_name_plural = "Học phí"
        unique_together = ('student', 'semester')

    def __str__(self):
        return f"Học phí {self.semester} - {self.student.mssv}"


class TuitionFeeDetail(models.Model):
    tuition_fee = models.ForeignKey(TuitionFee, on_delete=models.CASCADE, related_name='details', verbose_name="Học phí")
    course_name = models.CharField(max_length=100, verbose_name="Tên môn học")
    course_code = models.CharField(max_length=20, verbose_name="Mã môn")
    credits = models.IntegerField(verbose_name="Tín chỉ")
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Thành tiền")

    class Meta:
        verbose_name = "Chi tiết học phí"
        verbose_name_plural = "Chi tiết học phí"

    def __str__(self):
        return f"{self.course_code} - {self.amount}đ"

