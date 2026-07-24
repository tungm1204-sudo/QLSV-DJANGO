"""
Master Data Services
"""
from django.db import transaction
from .models import EducationSystem, Department, Major, Specialization, Room, PriorityCategory, ExamType, Cohort, AcademicYear, Semester, AdministrativeClass

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

