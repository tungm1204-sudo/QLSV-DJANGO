"""
Master Data Serializers
"""
from rest_framework import serializers
from .models import (
    EducationSystem, Department, Major, Specialization, Room, PriorityCategory, ExamType, 
    Cohort, AcademicYear, Semester, AdministrativeClass,
    Campus, Building, Degree, AcademicTitle, AdmissionType, Ethnicity, Religion, Nationality,
    CourseType, Position
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
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = '__all__'

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

class DepartmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class MajorReadSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Major
        fields = '__all__'

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

class MajorWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class SpecializationReadSerializer(serializers.ModelSerializer):
    major_name = serializers.SerializerMethodField()

    class Meta:
        model = Specialization
        fields = '__all__'

    def get_major_name(self, obj):
        return obj.major.name if obj.major else None

class SpecializationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
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
    academic_year_name = serializers.SerializerMethodField()

    class Meta:
        model = Semester
        fields = '__all__'

    def get_academic_year_name(self, obj):
        return obj.academic_year.name if obj.academic_year else None

class SemesterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class AdministrativeClassReadSerializer(serializers.ModelSerializer):
    major_details = MajorReadSerializer(source='major', read_only=True)
    cohort_details = CohortReadSerializer(source='cohort', read_only=True)
    education_system_details = EducationSystemReadSerializer(source='education_system', read_only=True)

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
    campus_details = CampusReadSerializer(source='campus', read_only=True)

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


class RoomReadSerializer(serializers.ModelSerializer):
    building_details = BuildingReadSerializer(source='building', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']



class CourseTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'

class CourseTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseType
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class PositionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
