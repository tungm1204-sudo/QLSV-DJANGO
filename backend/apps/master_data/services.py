"""
Master Data Services
"""
from django.db import transaction
from .models import EducationSystem, Department, Major, Specialization, Room, PriorityCategory, ExamType, Cohort, AcademicYear, Semester, AdministrativeClass, Campus, Building, Degree, AcademicTitle, AdmissionType, Ethnicity, Religion, Nationality, CourseType, Position

@transaction.atomic
def create_education_system(**data) -> EducationSystem:
    obj = EducationSystem(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_education_system(obj: EducationSystem, **data) -> EducationSystem:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_education_system(obj: EducationSystem):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_department(**data) -> Department:
    obj = Department(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_department(obj: Department, **data) -> Department:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_department(obj: Department):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_major(**data) -> Major:
    obj = Major(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_major(obj: Major, **data) -> Major:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_major(obj: Major):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_specialization(**data) -> Specialization:
    obj = Specialization(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_specialization(obj: Specialization, **data) -> Specialization:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_specialization(obj: Specialization):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_room(**data) -> Room:
    obj = Room(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_room(obj: Room, **data) -> Room:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_room(obj: Room):
    obj.status = Room.StatusChoices.MAINTENANCE
    obj.save(update_fields=['status'])

@transaction.atomic
def create_priority_category(**data) -> PriorityCategory:
    obj = PriorityCategory(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_priority_category(obj: PriorityCategory, **data) -> PriorityCategory:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_priority_category(obj: PriorityCategory):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_exam_type(**data) -> ExamType:
    obj = ExamType(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_exam_type(obj: ExamType, **data) -> ExamType:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_exam_type(obj: ExamType):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_cohort(**data) -> Cohort:
    obj = Cohort(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_cohort(obj: Cohort, **data) -> Cohort:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_cohort(obj: Cohort):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_academic_year(**data) -> AcademicYear:
    obj = AcademicYear(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_academic_year(obj: AcademicYear, **data) -> AcademicYear:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_academic_year(obj: AcademicYear):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_semester(**data) -> Semester:
    obj = Semester(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_semester(obj: Semester, **data) -> Semester:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_semester(obj: Semester):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_administrative_class(**data) -> AdministrativeClass:
    obj = AdministrativeClass(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_administrative_class(obj: AdministrativeClass, **data) -> AdministrativeClass:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_administrative_class(obj: AdministrativeClass):
    obj.is_active = False
    obj.save(update_fields=['is_active'])


def create_campus(**kwargs) -> Campus:
    return Campus.objects.create(**kwargs)

def update_campus(instance: Campus, **kwargs) -> Campus:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_campus(instance: Campus) -> None:
    instance.delete()

def create_building(**kwargs) -> Building:
    return Building.objects.create(**kwargs)

def update_building(instance: Building, **kwargs) -> Building:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_building(instance: Building) -> None:
    instance.delete()

def create_degree(**kwargs) -> Degree:
    return Degree.objects.create(**kwargs)

def update_degree(instance: Degree, **kwargs) -> Degree:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_degree(instance: Degree) -> None:
    instance.delete()

def create_academictitle(**kwargs) -> AcademicTitle:
    return AcademicTitle.objects.create(**kwargs)

def update_academictitle(instance: AcademicTitle, **kwargs) -> AcademicTitle:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_academictitle(instance: AcademicTitle) -> None:
    instance.delete()

def create_admissiontype(**kwargs) -> AdmissionType:
    return AdmissionType.objects.create(**kwargs)

def update_admissiontype(instance: AdmissionType, **kwargs) -> AdmissionType:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_admissiontype(instance: AdmissionType) -> None:
    instance.delete()

def create_ethnicity(**kwargs) -> Ethnicity:
    return Ethnicity.objects.create(**kwargs)

def update_ethnicity(instance: Ethnicity, **kwargs) -> Ethnicity:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_ethnicity(instance: Ethnicity) -> None:
    instance.delete()

def create_religion(**kwargs) -> Religion:
    return Religion.objects.create(**kwargs)

def update_religion(instance: Religion, **kwargs) -> Religion:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_religion(instance: Religion) -> None:
    instance.delete()

def create_nationality(**kwargs) -> Nationality:
    return Nationality.objects.create(**kwargs)

def update_nationality(instance: Nationality, **kwargs) -> Nationality:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_nationality(instance: Nationality) -> None:
    instance.delete()

def create_course_type(**kwargs) -> CourseType:
    return CourseType.objects.create(**kwargs)

def update_course_type(instance: CourseType, **kwargs) -> CourseType:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_course_type(instance: CourseType) -> None:
    instance.delete()

def create_position(**kwargs) -> Position:
    return Position.objects.create(**kwargs)

def update_position(instance: Position, **kwargs) -> Position:
    for k, v in kwargs.items():
        setattr(instance, k, v)
    instance.save()
    return instance

def delete_position(instance: Position) -> None:
    instance.delete()
