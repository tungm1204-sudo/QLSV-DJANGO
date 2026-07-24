"""
Master Data Serializers
"""
from rest_framework import serializers
from .models import (
    EducationSystem, Department, Major, Specialization, Room, PriorityCategory, ExamType, 
    Cohort, AcademicYear, Semester, AdministrativeClass,
    Campus, Building, Degree, AcademicTitle, AdmissionType, Ethnicity, Religion, Nationality
)

class EducationSystemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationSystem
        fields = '__all__'

class EducationSystemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationSystem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class DepartmentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class MajorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

class MajorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SpecializationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class SpecializationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class RoomReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PriorityCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityCategory
        fields = '__all__'

class PriorityCategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityCategory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'

class ExamTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class CohortReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'

class CohortWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AcademicYearReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class AcademicYearWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SemesterReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SemesterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AdministrativeClassReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeClass
        fields = '__all__'

class AdministrativeClassWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministrativeClass
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class CampusReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'

class CampusWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class BuildingReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'

class BuildingWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class DegreeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'

class DegreeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Degree
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AcademicTitleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTitle
        fields = '__all__'

class AcademicTitleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicTitle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AdmissionTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionType
        fields = '__all__'

class AdmissionTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class EthnicityReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ethnicity
        fields = '__all__'

class EthnicityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ethnicity
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class ReligionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = '__all__'

class ReligionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Religion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class NationalityReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'

class NationalityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

