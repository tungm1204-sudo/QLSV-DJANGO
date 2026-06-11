from django.db import models
from django.conf import settings


class Parent(models.Model):
    """
    Class: Parent (Phụ huynh / Người liên hệ khẩn cấp)
    Mục đích: Lưu thông tin người giám hộ hoặc liên hệ khẩn cấp của sinh viên.
    Business logic: Tách thành model riêng thay vì nhúng trực tiếp vào StudentProfile để
    một phụ huynh có thể liên kết với nhiều sinh viên (anh chị em ruột cùng trường).
    """
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
    Class: StudentProfile (Hồ sơ sinh viên)
    Mục đích: Lưu thông tin học vụ và cá nhân của sinh viên.
    Business logic:
    - Quan hệ OneToOne với User để tách logic đăng nhập (accounts app) khỏi dữ liệu học vụ.
    - `mssv` (Mã số sinh viên) là định danh nghiệp vụ chính, được dùng làm `lookup_field` trong API.
    - `date_of_join` tự động ghi ngày tạo hồ sơ, không cho phép sửa.
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
    # Khi xóa phụ huynh, sinh viên vẫn được giữ lại (SET_NULL) để tránh mất dữ liệu học vụ
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
