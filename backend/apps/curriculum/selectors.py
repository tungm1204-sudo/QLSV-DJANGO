"""
Curriculum Selectors
"""
from typing import Iterable
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse

def get_courses(*, is_active: bool = None) -> Iterable[Course]:
    qs = Course.objects.all()
    qs = qs.select_related('major')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_course_by_id(id: str) -> Course:
    return Course.objects.get(id=id)

def get_training_programs(*, is_active: bool = None) -> Iterable[TrainingProgram]:
    qs = TrainingProgram.objects.all()
    qs = qs.select_related('major')
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_training_program_by_id(id: str) -> TrainingProgram:
    return TrainingProgram.objects.get(id=id)

def get_prerequisites(*, is_active: bool = None) -> Iterable[Prerequisite]:
    qs = Prerequisite.objects.all()
    qs = qs.select_related('course', 'required_course')
    return qs

def get_prerequisite_by_id(id: str) -> Prerequisite:
    return Prerequisite.objects.get(id=id)

def get_equivalent_courses(*, is_active: bool = None) -> Iterable[EquivalentCourse]:
    qs = EquivalentCourse.objects.all()
    qs = qs.select_related('course', 'equivalent_course')
    return qs

def get_equivalent_course_by_id(id: str) -> EquivalentCourse:
    return EquivalentCourse.objects.get(id=id)

