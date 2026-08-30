"""
Curriculum Serializers
"""
from rest_framework import serializers
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, KnowledgeBlock, TrainingProgramCourse

class CourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'credits', 'theory_credits', 'practical_credits', 'department', 'course_type', 'is_active', 'created_at', 'updated_at']

class TrainingProgramReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'

class TrainingProgramWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = ['id', 'code', 'name', 'major', 'specialization', 'cohort', 'total_credits', 'is_active', 'created_at', 'updated_at']

class KnowledgeBlockReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBlock
        fields = '__all__'

class KnowledgeBlockWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBlock
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class TrainingProgramCourseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgramCourse
        fields = '__all__'

class TrainingProgramCourseWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgramCourse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class TrainingProgramDetailReadSerializer(serializers.ModelSerializer):
    knowledge_blocks = KnowledgeBlockReadSerializer(many=True, read_only=True)
    
    class Meta:
        model = TrainingProgram
        fields = ['id', 'code', 'name', 'major', 'specialization', 'cohort', 'total_credits', 'is_active', 'knowledge_blocks', 'created_at', 'updated_at']

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
