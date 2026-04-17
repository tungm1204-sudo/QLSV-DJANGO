from django.db import models
from django.conf import settings


class Department(models.Model):
    """Khoa / Bộ môn."""
    name = models.CharField(max_length=100, verbose_name="Tên khoa")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã khoa")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Khoa / Bộ môn"
        verbose_name_plural = "Khoa / Bộ môn"

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    """
    Hồ sơ giảng viên — OneToOne với User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        verbose_name="Tài khoản",
    )
    mgv = models.CharField(max_length=20, unique=True, verbose_name="Mã số giảng viên")
    dob = models.DateField(verbose_name="Ngày sinh")
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Nam"), ("female", "Nữ"), ("other", "Khác")],
        default="male",
        verbose_name="Giới tính",
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Khoa"
    )
    degree = models.CharField(
        max_length=50,
        choices=[("bachelor", "Cử nhân"), ("master", "Thạc sĩ"), ("phd", "Tiến sĩ")],
        default="bachelor",
        verbose_name="Bằng cấp",
    )
    specialization = models.CharField(max_length=200, blank=True, null=True, verbose_name="Chuyên môn")
    status = models.BooleanField(default=True, verbose_name="Đang dạy")

    class Meta:
        verbose_name = "Hồ sơ giảng viên"
        verbose_name_plural = "Hồ sơ giảng viên"

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.mgv})"
