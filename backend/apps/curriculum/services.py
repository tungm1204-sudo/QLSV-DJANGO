"""
Curriculum Services
"""
from django.db import transaction
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse

@transaction.atomic
def create_course(**data) -> Course:
    obj = Course(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_course(obj: Course, **data) -> Course:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_course(obj: Course):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_training_program(**data) -> TrainingProgram:
    obj = TrainingProgram(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_training_program(obj: TrainingProgram, **data) -> TrainingProgram:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_training_program(obj: TrainingProgram):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

@transaction.atomic
def create_prerequisite(**data) -> Prerequisite:
    obj = Prerequisite(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_prerequisite(obj: Prerequisite, **data) -> Prerequisite:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_prerequisite(obj: Prerequisite):
    obj.delete()

@transaction.atomic
def create_equivalent_course(**data) -> EquivalentCourse:
    obj = EquivalentCourse(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_equivalent_course(obj: EquivalentCourse, **data) -> EquivalentCourse:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_equivalent_course(obj: EquivalentCourse):
    obj.delete()

