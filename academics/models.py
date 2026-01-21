from django.db import models
from teachers.models import Teacher
from students.models import Student

class Grade(models.Model):
    """
    Model đại diện cho Khối lớp (VD: Khối 10, Khối 11).
    """
    grade_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)        # Tên khối
    description = models.CharField(max_length=255, blank=True, null=True) # Mô tả

    def __str__(self):
        return self.name

class Course(models.Model):
    """
    Model đại diện cho Môn học (VD: Toán, Lý, Hóa).
    """
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)       # Tên môn học
    description = models.CharField(max_length=255, blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE) # Thuộc khối nào

    def __str__(self):
        return self.name

class Classroom(models.Model):
    """
    Model đại diện cho Lớp học cụ thể (VD: 10A1, 11B2).
    """
    classroom_id = models.AutoField(primary_key=True)
    year = models.IntegerField()                  # Năm học
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE) # Khối
    section = models.CharField(max_length=2)      # Tên lớp (A1, B2...)
    status = models.BooleanField(default=True)    # Trạng thái
    remarks = models.CharField(max_length=255, blank=True, null=True) # Ghi chú
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True) # Giáo viên chủ nhiệm

    def __str__(self):
        return f"{self.grade.name}-{self.section}"

class ClassroomStudent(models.Model):
    """
    Bảng trung gian liên kết Sinh viên vào Lớp học.
    """
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('classroom', 'student') # Một sinh viên chỉ học 1 lớp (trong bảng này)

class Attendance(models.Model):
    """
    Model Điểm danh (Tương lai).
    """
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField()
    remark = models.TextField(blank=True, null=True)

class ExamType(models.Model):
    """
    Model Loại kỳ thi (Giữa kỳ, Cuối kỳ...).
    """
    exam_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    """
    Model Kỳ thi cụ thể.
    """
    exam_id = models.AutoField(primary_key=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class ExamResult(models.Model):
    """
    Model Kết quả thi (Điểm số).
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.CharField(max_length=45) # Điểm số
