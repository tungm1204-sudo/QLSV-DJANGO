"""
Master Data Serializers
=======================
Thực hiện Serialize/Deserialize dữ liệu cho Master Data.
Tuyệt đối không chứa business logic ở đây theo chuẩn rules.md.
"""
from rest_framework import serializers
from .models import Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer cho Khoa/Bộ môn"""
    class Meta:
        model = Department
        fields = '__all__'

class MajorSerializer(serializers.ModelSerializer):
    """Serializer cho Ngành học"""
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
    class Meta:
        model = Semester
        fields = '__all__'
