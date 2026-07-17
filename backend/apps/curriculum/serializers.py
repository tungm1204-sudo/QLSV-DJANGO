"""
Curriculum Serializers
======================
Chuyển đổi Dữ liệu JSON <-> Model cho Module Đào tạo.
"""
from rest_framework import serializers
from .models import Course, TrainingProgram, Prerequisite

class CourseSerializer(serializers.ModelSerializer):
    """Serializer cho Môn học"""
    class Meta:
        model = Course
        fields = '__all__'

class TrainingProgramSerializer(serializers.ModelSerializer):
    """Serializer cho Khung chương trình"""
    class Meta:
        model = TrainingProgram
        fields = '__all__'

class PrerequisiteSerializer(serializers.ModelSerializer):
    """Serializer cho Môn tiên quyết"""
    class Meta:
        model = Prerequisite
        fields = '__all__'
