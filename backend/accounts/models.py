from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Class: User (Custom User Model)
    Mục đích: Mở rộng model User mặc định của Django để thêm trường `role`, `phone`, `avatar`.
    Business logic:
    - Sử dụng AbstractUser giúp kế thừa toàn bộ chức năng xác thực của Django (login, password, permissions...).
    - Vai trò (`role`) được lưu trực tiếp trên user để phân quyền nhanh mà không cần join bảng Group mỗi lần.
    - Cần khai báo AUTH_USER_MODEL = 'accounts.User' trong settings.py để Django dùng model này.
    """

    class Role(models.TextChoices):
        """Enum các vai trò trong hệ thống, dùng TextChoices để Django Admin hiển thị label tiếng Việt."""
        ADMIN = "admin", "Admin"
        ACADEMIC_STAFF = "academic_staff", "Giáo vụ"
        TEACHER = "teacher", "Giáo viên"
        STUDENT = "student", "Sinh viên"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT, # Mặc định là Sinh viên, vì đây là nhóm người dùng phổ biến nhất
        verbose_name="Vai trò",
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Ảnh đại diện")

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    # --- Các property tiện ích để kiểm tra vai trò ---
    # Dùng property thay vì gọi trực tiếp `user.role == 'admin'` để code dễ đọc hơn và
    # tránh hardcode string ở nhiều nơi.

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_academic_staff(self):
        return self.role == self.Role.ACADEMIC_STAFF

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT
