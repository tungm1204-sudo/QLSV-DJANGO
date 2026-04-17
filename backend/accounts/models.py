from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model — extends Django's AbstractUser.
    Roles are managed via Django Groups (Admin/Giáo vụ/Giáo viên/Sinh viên).
    """

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        ACADEMIC_STAFF = "academic_staff", "Giáo vụ"
        TEACHER = "teacher", "Giáo viên"
        STUDENT = "student", "Sinh viên"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name="Vai trò",
    )
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Ảnh đại diện")

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

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
