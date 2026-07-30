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

from .models import CourseOffering, TrainingPlan, Schedule

class TrainingPlanReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = '__all__'

class TrainingPlanWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class CourseOfferingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOffering
        fields = '__all__'

class CourseOfferingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseOffering
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ScheduleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'

class ScheduleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
