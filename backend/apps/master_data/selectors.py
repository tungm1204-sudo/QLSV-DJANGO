"""
Master Data Selectors
"""
from typing import Iterable
from .models import EducationSystem, Department, Major, Specialization, Room, PriorityCategory, ExamType, Cohort, AcademicYear, Semester, AdministrativeClass, Campus, Building, Degree, AcademicTitle, AdmissionType, Ethnicity, Religion, Nationality

def get_education_systems(*, is_active: bool = None) -> Iterable[EducationSystem]:
    qs = EducationSystem.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_education_system_by_id(id: str) -> EducationSystem:
    return EducationSystem.objects.get(id=id)

def get_departments(*, is_active: bool = None) -> Iterable[Department]:
    qs = Department.objects.all()
    qs = qs.select_related('parent', 'manager')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_department_by_id(id: str) -> Department:
    return Department.objects.get(id=id)

def get_majors(*, is_active: bool = None) -> Iterable[Major]:
    qs = Major.objects.all()
    qs = qs.select_related('department')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_major_by_id(id: str) -> Major:
    return Major.objects.get(id=id)

def get_specializations(*, is_active: bool = None) -> Iterable[Specialization]:
    qs = Specialization.objects.all()
    qs = qs.select_related('major')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_specialization_by_id(id: str) -> Specialization:
    return Specialization.objects.get(id=id)

def get_rooms(*, is_active: bool = None) -> Iterable[Room]:
    qs = Room.objects.all()
    if is_active is not None:
        if is_active:
            qs = qs.filter(status=Room.StatusChoices.ACTIVE)
        else:
            qs = qs.filter(status=Room.StatusChoices.MAINTENANCE)
    return qs

def get_room_by_id(id: str) -> Room:
    return Room.objects.get(id=id)

def get_priority_categorys(*, is_active: bool = None) -> Iterable[PriorityCategory]:
    qs = PriorityCategory.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_priority_category_by_id(id: str) -> PriorityCategory:
    return PriorityCategory.objects.get(id=id)

def get_exam_types(*, is_active: bool = None) -> Iterable[ExamType]:
    qs = ExamType.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_exam_type_by_id(id: str) -> ExamType:
    return ExamType.objects.get(id=id)

def get_cohorts(*, is_active: bool = None) -> Iterable[Cohort]:
    qs = Cohort.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_cohort_by_id(id: str) -> Cohort:
    return Cohort.objects.get(id=id)

def get_academic_years(*, is_active: bool = None) -> Iterable[AcademicYear]:
    qs = AcademicYear.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_academic_year_by_id(id: str) -> AcademicYear:
    return AcademicYear.objects.get(id=id)

def get_semesters(*, is_active: bool = None) -> Iterable[Semester]:
    qs = Semester.objects.all()
    qs = qs.select_related('academic_year')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_semester_by_id(id: str) -> Semester:
    return Semester.objects.get(id=id)

def get_administrative_classs(*, is_active: bool = None) -> Iterable[AdministrativeClass]:
    qs = AdministrativeClass.objects.all()
    qs = qs.select_related('major')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_administrative_class_by_id(id: str) -> AdministrativeClass:
    return AdministrativeClass.objects.get(id=id)


def get_campuss(*, is_active: bool = None):
    qs = Campus.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_campus_by_id(id: str) -> Campus:
    return Campus.objects.get(id=id)

def get_buildings(*, is_active: bool = None):
    qs = Building.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_building_by_id(id: str) -> Building:
    return Building.objects.get(id=id)

def get_degrees(*, is_active: bool = None):
    qs = Degree.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_degree_by_id(id: str) -> Degree:
    return Degree.objects.get(id=id)

def get_academictitles(*, is_active: bool = None):
    qs = AcademicTitle.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_academictitle_by_id(id: str) -> AcademicTitle:
    return AcademicTitle.objects.get(id=id)

def get_admissiontypes(*, is_active: bool = None):
    qs = AdmissionType.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_admissiontype_by_id(id: str) -> AdmissionType:
    return AdmissionType.objects.get(id=id)

def get_ethnicities(*, is_active: bool = None):
    qs = Ethnicity.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_ethnicity_by_id(id: str) -> Ethnicity:
    return Ethnicity.objects.get(id=id)

def get_religions(*, is_active: bool = None):
    qs = Religion.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_religion_by_id(id: str) -> Religion:
    return Religion.objects.get(id=id)

def get_nationalities(*, is_active: bool = None):
    qs = Nationality.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_nationality_by_id(id: str) -> Nationality:
    return Nationality.objects.get(id=id)
