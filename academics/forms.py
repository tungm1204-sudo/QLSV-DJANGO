from django import forms
from .models import Course, Classroom

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
