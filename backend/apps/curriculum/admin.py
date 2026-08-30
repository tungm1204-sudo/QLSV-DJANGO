from django.contrib import admin
from .models import Course, TrainingProgram, Prerequisite, EquivalentCourse, TrainingPlan, CourseOffering, Schedule

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'department', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('department', 'is_active')

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'major', 'total_credits', 'is_active')
    search_fields = ('code', 'name')
    list_filter = ('major', 'is_active')

@admin.register(Prerequisite)
class PrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('course', 'required_course')
    search_fields = ('course__code', 'required_course__code')

@admin.register(EquivalentCourse)
class EquivalentCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'equivalent_course')
    search_fields = ('course__code', 'equivalent_course__code')

@admin.register(TrainingPlan)
class TrainingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'semester', 'department', 'status')
    list_filter = ('status', 'semester', 'department')
    search_fields = ('name',)

@admin.register(CourseOffering)
class CourseOfferingAdmin(admin.ModelAdmin):
    list_display = ('course', 'semester', 'lecturer', 'status', 'current_enrollment', 'max_capacity')
    list_filter = ('status', 'semester', 'training_plan')
    search_fields = ('course__code', 'course__name')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course_offering', 'day_of_week', 'start_period', 'end_period', 'room')
    list_filter = ('day_of_week', 'room')
