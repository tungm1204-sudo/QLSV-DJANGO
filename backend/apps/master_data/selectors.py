"""
Master Data Selectors
======================
Tầng Selector: Chứa toàn bộ logic Query (đọc dữ liệu) cho module Master Data.
Tuân thủ quy tắc:
  - Luôn dùng select_related() / prefetch_related() cho bất kỳ QuerySet nào có FK.
  - Không chứa Business Logic. Chỉ trả về QuerySet hoặc object.
"""
from typing import Iterable, Optional

from .models import (
    EducationSystem, Department, Major, Specialization,
    Campus, Building, Room,
    PriorityCategory, ExamType,
    Cohort, AcademicYear, Semester, AdministrativeClass,
    Degree, AcademicTitle, AdmissionType,
    Ethnicity, Religion, Nationality,
    CourseType, Position,
)


# ─────────────────────────────────────────────────────────────
# EducationSystem
# ─────────────────────────────────────────────────────────────

def get_education_systems(*, is_active: Optional[bool] = None) -> Iterable[EducationSystem]:
    qs = EducationSystem.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_education_system_by_id(id: str) -> EducationSystem:
    return EducationSystem.objects.get(id=id)


# ─────────────────────────────────────────────────────────────
# Department
# ─────────────────────────────────────────────────────────────

def get_departments(*, is_active: Optional[bool] = None) -> Iterable[Department]:
    # select_related: parent (tự tham chiếu), manager (FK -> User)
    qs = Department.objects.select_related('parent', 'manager').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_department_by_id(id: str) -> Department:
    return Department.objects.select_related('parent', 'manager').get(id=id)


# ─────────────────────────────────────────────────────────────
# Major & Specialization
# ─────────────────────────────────────────────────────────────

def get_majors(*, is_active: Optional[bool] = None) -> Iterable[Major]:
    # select_related: department (FK -> Department)
    qs = Major.objects.select_related('department').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_major_by_id(id: str) -> Major:
    return Major.objects.select_related('department').get(id=id)

def get_specializations(*, is_active: Optional[bool] = None) -> Iterable[Specialization]:
    # select_related: major (FK -> Major)
    qs = Specialization.objects.select_related('major').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_specialization_by_id(id: str) -> Specialization:
    return Specialization.objects.select_related('major').get(id=id)


# ─────────────────────────────────────────────────────────────
# Campus, Building, Room
# ─────────────────────────────────────────────────────────────

def get_campuss(*, is_active: Optional[bool] = None) -> Iterable[Campus]:
    qs = Campus.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_campus_by_id(id: str) -> Campus:
    return Campus.objects.get(id=id)

def get_buildings(*, is_active: Optional[bool] = None) -> Iterable[Building]:
    # select_related: campus (FK -> Campus)
    qs = Building.objects.select_related('campus').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_building_by_id(id: str) -> Building:
    return Building.objects.select_related('campus').get(id=id)

def get_rooms(*, is_active: Optional[bool] = None) -> Iterable[Room]:
    # select_related: building -> campus (chuỗi FK 2 cấp)
    qs = Room.objects.select_related('building__campus').order_by('-created_at')
    if is_active is not None:
        if is_active:
            qs = qs.filter(status=Room.StatusChoices.ACTIVE)
        else:
            qs = qs.filter(status=Room.StatusChoices.MAINTENANCE)
    return qs

def get_room_by_id(id: str) -> Room:
    return Room.objects.select_related('building__campus').get(id=id)


# ─────────────────────────────────────────────────────────────
# PriorityCategory, ExamType
# ─────────────────────────────────────────────────────────────

def get_priority_categorys(*, is_active: Optional[bool] = None) -> Iterable[PriorityCategory]:
    qs = PriorityCategory.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_priority_category_by_id(id: str) -> PriorityCategory:
    return PriorityCategory.objects.get(id=id)

def get_exam_types(*, is_active: Optional[bool] = None) -> Iterable[ExamType]:
    qs = ExamType.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_exam_type_by_id(id: str) -> ExamType:
    return ExamType.objects.get(id=id)


# ─────────────────────────────────────────────────────────────
# Cohort, AcademicYear, Semester, AdministrativeClass
# ─────────────────────────────────────────────────────────────

def get_cohorts(*, is_active: Optional[bool] = None) -> Iterable[Cohort]:
    qs = Cohort.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_cohort_by_id(id: str) -> Cohort:
    return Cohort.objects.get(id=id)

def get_academic_years(*, is_active: Optional[bool] = None) -> Iterable[AcademicYear]:
    qs = AcademicYear.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_academic_year_by_id(id: str) -> AcademicYear:
    return AcademicYear.objects.get(id=id)

def get_semesters(*, is_active: Optional[bool] = None) -> Iterable[Semester]:
    # select_related: academic_year (FK -> AcademicYear)
    qs = Semester.objects.select_related('academic_year').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_current=is_active)
    return qs

def get_semester_by_id(id: str) -> Semester:
    return Semester.objects.select_related('academic_year').get(id=id)

def get_administrative_classs(*, is_active: Optional[bool] = None) -> Iterable[AdministrativeClass]:
    # select_related: major, cohort, education_system, advisor
    qs = AdministrativeClass.objects.select_related('major', 'cohort', 'education_system', 'advisor__user').order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_administrative_class_by_id(id: str) -> AdministrativeClass:
    return AdministrativeClass.objects.select_related('major', 'cohort', 'education_system').get(id=id)


# ─────────────────────────────────────────────────────────────
# Degree, AcademicTitle, AdmissionType
# ─────────────────────────────────────────────────────────────

def get_degrees(*, is_active: Optional[bool] = None) -> Iterable[Degree]:
    qs = Degree.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_degree_by_id(id: str) -> Degree:
    return Degree.objects.get(id=id)

def get_academictitles(*, is_active: Optional[bool] = None) -> Iterable[AcademicTitle]:
    qs = AcademicTitle.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_academictitle_by_id(id: str) -> AcademicTitle:
    return AcademicTitle.objects.get(id=id)

def get_admissiontypes(*, is_active: Optional[bool] = None) -> Iterable[AdmissionType]:
    qs = AdmissionType.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_admissiontype_by_id(id: str) -> AdmissionType:
    return AdmissionType.objects.get(id=id)


# ─────────────────────────────────────────────────────────────
# Ethnicity, Religion, Nationality
# ─────────────────────────────────────────────────────────────

def get_ethnicities(*, is_active: Optional[bool] = None) -> Iterable[Ethnicity]:
    qs = Ethnicity.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_ethnicity_by_id(id: str) -> Ethnicity:
    return Ethnicity.objects.get(id=id)

def get_religions(*, is_active: Optional[bool] = None) -> Iterable[Religion]:
    qs = Religion.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_religion_by_id(id: str) -> Religion:
    return Religion.objects.get(id=id)

def get_nationalities(*, is_active: Optional[bool] = None) -> Iterable[Nationality]:
    qs = Nationality.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_nationality_by_id(id: str) -> Nationality:
    return Nationality.objects.get(id=id)


# ─────────────────────────────────────────────────────────────
# CourseType, Position (bảng mới)
# ─────────────────────────────────────────────────────────────

def get_coursetypes(*, is_active: Optional[bool] = None) -> Iterable[CourseType]:
    qs = CourseType.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_course_type_by_id(id: str) -> CourseType:
    return CourseType.objects.get(id=id)

def get_positions(*, is_active: Optional[bool] = None) -> Iterable[Position]:
    qs = Position.objects.all().order_by('-created_at')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_position_by_id(id: str) -> Position:
    return Position.objects.get(id=id)
