from django import forms
from .models import Course, Classroom

class CourseForm(forms.ModelForm):
    """
    Class: CourseForm
    Mục đích: Form tự động sinh từ model Course để thao tác tạo/sửa môn học (dùng ở Django Admin hoặc template).
    """
    class Meta:
        model = Course
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    """
    Class: ClassroomForm
    Mục đích: Form tự động sinh từ model Classroom để thao tác tạo/sửa lớp học.
    """
    class Meta:
        model = Classroom
        fields = '__all__'
