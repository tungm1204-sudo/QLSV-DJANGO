"""
Master Data Serializers
=======================
Thực hiện Serialize/Deserialize dữ liệu cho Master Data.
Tuyệt đối không chứa business logic ở đây theo chuẩn rules.md.
"""
from rest_framework import serializers
from .models import (
    Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester,
    Specialization, EducationSystem, AcademicYear
)

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer cho Khoa/Bộ môn"""
    parent_name = serializers.CharField(source='parent.name', read_only=True)
    manager_full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        fields = '__all__'

    def get_manager_full_name(self, obj):
        if obj.manager_id:
            from apps.identity.models import User
            try:
                user = User.objects.get(id=obj.manager_id)
                return user.full_name
            except User.DoesNotExist:
                return None
        return None

class MajorSerializer(serializers.ModelSerializer):
    """Serializer cho Ngành học"""
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Major
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    """Serializer cho Phòng học"""
    class Meta:
        model = Room
        fields = '__all__'

class PriorityCategorySerializer(serializers.ModelSerializer):
    """Serializer cho Đối tượng ưu tiên"""
    class Meta:
        model = PriorityCategory
        fields = '__all__'

class ExamTypeSerializer(serializers.ModelSerializer):
    """Serializer cho Hình thức thi"""
    class Meta:
        model = ExamType
        fields = '__all__'

class CohortSerializer(serializers.ModelSerializer):
    """Serializer cho Khóa học"""
    class Meta:
        model = Cohort
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    """Serializer cho Học kỳ"""
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)

    class Meta:
        model = Semester
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    major_name = serializers.CharField(source='major.name', read_only=True)

    class Meta:
        model = Specialization
        fields = '__all__'

class EducationSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationSystem
        fields = '__all__'

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'
