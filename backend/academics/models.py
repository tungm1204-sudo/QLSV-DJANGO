from django.db import models
from django.conf import settings
from teachers.models import TeacherProfile


class Semester(models.Model):
    """Học kỳ (VD: HK1 2024-2025)."""
    name = models.CharField(max_length=50, verbose_name="Tên học kỳ")
    academic_year = models.CharField(max_length=20, verbose_name="Năm học")  # VD: "2024-2025"
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    is_current = models.BooleanField(default=False, verbose_name="Học kỳ hiện tại")

    class Meta:
        verbose_name = "Học kỳ"
        verbose_name_plural = "Học kỳ"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.academic_year})"


class Grade(models.Model):
    """Khóa / Năm học (VD: K20, Năm 1)."""
    name = models.CharField(max_length=50, verbose_name="Tên khóa/năm")
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Khóa / Năm học"
        verbose_name_plural = "Khóa / Năm học"

    def __str__(self):
        return self.name


class Course(models.Model):
    """Môn học (VD: Toán, Lập trình Python)."""
    name = models.CharField(max_length=100, verbose_name="Tên môn")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã môn")
    description = models.TextField(blank=True, null=True)
    credits = models.PositiveSmallIntegerField(default=3, verbose_name="Số tín chỉ")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="courses", verbose_name="Khối")

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"

    def __str__(self):
        return f"{self.code} — {self.name}"


class Classroom(models.Model):
    """Lớp sinh hoạt (VD: 20CNTT1 — HK1 2024-2025)."""
    name = models.CharField(max_length=20, verbose_name="Tên lớp")
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, verbose_name="Khóa/Năm")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="classrooms", verbose_name="Học kỳ")
    homeroom_teacher = models.ForeignKey(
        TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="homeroom_classes", verbose_name="Giảng viên chủ nhiệm"
    )
    max_students = models.PositiveSmallIntegerField(default=40, verbose_name="Sĩ số tối đa")
    status = models.BooleanField(default=True, verbose_name="Hoạt động")
    remarks = models.TextField(blank=True, null=True, verbose_name="Ghi chú")

    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
        unique_together = ("name", "semester")

    def __str__(self):
        return f"{self.name} ({self.semester.name})"


class ClassroomStudent(models.Model):
    """Bảng trung gian: Sinh viên trong Lớp."""
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sinh viên trong lớp"
        verbose_name_plural = "Sinh viên trong lớp"
        unique_together = ("classroom", "student")

    def __str__(self):
        return f"{self.student} → {self.classroom}"


class CourseAssignment(models.Model):
    """Phân công giáo viên dạy môn trong lớp."""
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="assignments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name="assignments")

    class Meta:
        verbose_name = "Phân công dạy"
        verbose_name_plural = "Phân công dạy"
        unique_together = ("classroom", "course")

    def __str__(self):
        return f"{self.teacher} dạy {self.course} lớp {self.classroom}"


class Attendance(models.Model):
    """Điểm danh theo buổi học."""
    class Status(models.TextChoices):
        PRESENT = "present", "Có mặt"
        ABSENT = "absent", "Vắng"
        LATE = "late", "Đi muộn"
        EXCUSED = "excused", "Có phép"

    date = models.DateField(verbose_name="Ngày")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendances")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="attendances")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Điểm danh"
        verbose_name_plural = "Điểm danh"
        unique_together = ("date", "student", "classroom")

    def __str__(self):
        return f"{self.student} — {self.date} — {self.status}"


class ExamType(models.Model):
    """Loại kỳ thi: Giữa kỳ, Cuối kỳ, Kiểm tra thường xuyên..."""
    name = models.CharField(max_length=50, verbose_name="Tên loại")
    weight = models.FloatField(default=1.0, verbose_name="Hệ số")

    class Meta:
        verbose_name = "Loại thi"
        verbose_name_plural = "Loại thi"

    def __str__(self):
        return self.name


class ExamResult(models.Model):
    """Kết quả thi / Điểm số của sinh viên."""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exam_results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="exam_results")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="exam_results")
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name="exam_results")
    marks = models.FloatField(verbose_name="Điểm")
    max_marks = models.FloatField(default=10.0, verbose_name="Điểm tối đa")
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kết quả thi"
        verbose_name_plural = "Kết quả thi"
        unique_together = ("student", "course", "semester", "exam_type")

    def __str__(self):
        return f"{self.student} — {self.course} — {self.marks}/{self.max_marks}"

    @property
    def percentage(self):
        return round((self.marks / self.max_marks) * 100, 2) if self.max_marks else 0
