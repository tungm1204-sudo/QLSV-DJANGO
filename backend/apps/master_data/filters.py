import django_filters
from .models import (
    Department, Major, Specialization, Campus, Building, Room,
    PriorityCategory, ExamType, Cohort, AcademicYear, Semester,
    AdministrativeClass, Degree, AcademicTitle, AdmissionType,
    Ethnicity, Religion, Nationality, EducationSystem, CourseType, Position
)

class DepartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Department
        fields = ['type', 'parent', 'is_active']

class MajorFilter(django_filters.FilterSet):
    class Meta:
        model = Major
        fields = ['department', 'level', 'is_active']

class SpecializationFilter(django_filters.FilterSet):
    class Meta:
        model = Specialization
        fields = ['major', 'is_active']

class BuildingFilter(django_filters.FilterSet):
    class Meta:
        model = Building
        fields = ['campus', 'is_active']

class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = ['building', 'type', 'status', 'floor', 'building__campus']

class SemesterFilter(django_filters.FilterSet):
    class Meta:
        model = Semester
        fields = ['academic_year', 'season', 'is_current']

class AdministrativeClassFilter(django_filters.FilterSet):
    class Meta:
        model = AdministrativeClass
        fields = ['major', 'cohort', 'education_system', 'advisor', 'is_active']
