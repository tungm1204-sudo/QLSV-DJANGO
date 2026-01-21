from django import forms
from .models import Course, Classroom

class CourseForm(forms.ModelForm):
    """Form quản lý Môn học"""
    class Meta:
        model = Course
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    """Form quản lý Lớp học"""
    class Meta:
        model = Classroom
        fields = '__all__'
