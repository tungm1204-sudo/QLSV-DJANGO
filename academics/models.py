from django.db import models
from teachers.models import Teacher
from students.models import Student

class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    classroom_id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    section = models.CharField(max_length=2)
    status = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.grade.name}-{self.section}"

class ClassroomStudent(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('classroom', 'student')

class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField()
    remark = models.TextField(blank=True, null=True)

class ExamType(models.Model):
    exam_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()

    def __str__(self):
        return self.name

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.CharField(max_length=45)
