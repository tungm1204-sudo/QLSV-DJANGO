"""
Curriculum Selectors
"""
from typing import Iterable
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, TrainingPlan, CourseOffering, Schedule

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

def get_training_plans() -> Iterable[TrainingPlan]:
    return TrainingPlan.objects.all().select_related('semester', 'department', 'created_by', 'approved_by')

def get_training_plan_by_id(id: str) -> TrainingPlan:
    return TrainingPlan.objects.select_related('semester', 'department', 'created_by', 'approved_by').get(id=id)

def get_course_offerings() -> Iterable[CourseOffering]:
    return CourseOffering.objects.all().select_related('training_plan', 'course', 'semester', 'lecturer')

def get_course_offering_by_id(id: str) -> CourseOffering:
    return CourseOffering.objects.select_related('training_plan', 'course', 'semester', 'lecturer').get(id=id)

def get_schedules() -> Iterable[Schedule]:
    return Schedule.objects.all().select_related('course_offering', 'room')

def get_schedule_by_id(id: str) -> Schedule:
    return Schedule.objects.select_related('course_offering', 'room').get(id=id)
