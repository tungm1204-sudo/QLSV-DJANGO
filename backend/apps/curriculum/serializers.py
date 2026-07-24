"""
Curriculum Serializers
"""
from rest_framework import serializers
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse

class CourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class TrainingProgramReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'

class TrainingProgramWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PrerequisiteReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'

class PrerequisiteWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prerequisite
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class EquivalentCourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquivalentCourse
        fields = '__all__'

class EquivalentCourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquivalentCourse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

from .models import CourseOffering
class CourseOfferingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOffering
        fields = '__all__'


