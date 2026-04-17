from django.db import models
from django.conf import settings


class Parent(models.Model):
    """Phụ huynh / Người giám hộ của sinh viên."""
    fname = models.CharField(max_length=50, verbose_name="Tên")
    lname = models.CharField(max_length=50, verbose_name="Họ")
    dob = models.DateField(verbose_name="Ngày sinh")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Điện thoại")
    mobile = models.CharField(max_length=20, verbose_name="Di động")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    status = models.BooleanField(default=True, verbose_name="Hoạt động")

    class Meta:
        verbose_name = "Liên hệ khẩn cấp"
        verbose_name_plural = "Liên hệ khẩn cấp"

    def __str__(self):
        return f"{self.fname} {self.lname}"


class StudentProfile(models.Model):
    """
    Hồ sơ sinh viên — OneToOne với User.
    Chứa thông tin học vụ của sinh viên.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
        verbose_name="Tài khoản",
    )
    mssv = models.CharField(max_length=20, unique=True, verbose_name="Mã số sinh viên")
    dob = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Nam"), ("female", "Nữ"), ("other", "Khác")],
        default="male",
        verbose_name="Giới tính",
    )
    address = models.TextField(blank=True, null=True, verbose_name="Địa chỉ")
    parent = models.ForeignKey(
        Parent, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người liên hệ khẩn cấp"
    )
    date_of_join = models.DateField(auto_now_add=True, verbose_name="Ngày nhập học")
    status = models.BooleanField(default=True, verbose_name="Đang học")

    class Meta:
        verbose_name = "Hồ sơ sinh viên"
        verbose_name_plural = "Hồ sơ sinh viên"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.mssv})"
