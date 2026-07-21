"""
Curriculum Serializers
======================
Chuyển đổi Dữ liệu JSON <-> Model cho Module Đào tạo.
"""
from rest_framework import serializers
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, TrainingPlan, CourseOffering, Schedule

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

class EquivalentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquivalentCourse
        fields = '__all__'

class TrainingPlanSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = TrainingPlan
        fields = '__all__'
        read_only_fields = ('status', 'approved_by')

class CourseOfferingSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    lecturer_name = serializers.CharField(source='lecturer.get_full_name', read_only=True)
    
    class Meta:
        model = CourseOffering
        fields = '__all__'

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
