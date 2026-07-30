import django_filters
from .models import Course, CourseOffering, TrainingPlan, Schedule

class CourseFilter(django_filters.FilterSet):
    major_id = django_filters.UUIDFilter(field_name='major_id')
    course_type_id = django_filters.UUIDFilter(field_name='course_type_id')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Course
        fields = ['major_id', 'course_type_id', 'is_active']

    def filter_search(self, queryset, name, value):
        from django.db.models import Q
        return queryset.filter(Q(code__icontains=value) | Q(name__icontains=value))

class TrainingPlanFilter(django_filters.FilterSet):
    semester_id = django_filters.UUIDFilter(field_name='semester_id')
    department_id = django_filters.UUIDFilter(field_name='department_id')
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = TrainingPlan
        fields = ['semester_id', 'department_id', 'status']

    def filter_search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)

class CourseOfferingFilter(django_filters.FilterSet):
    training_plan_id = django_filters.UUIDFilter(field_name='training_plan_id')
    semester_id = django_filters.UUIDFilter(field_name='semester_id')
    course_id = django_filters.UUIDFilter(field_name='course_id')
    lecturer_id = django_filters.UUIDFilter(field_name='lecturer_id')

    class Meta:
        model = CourseOffering
        fields = ['training_plan_id', 'semester_id', 'course_id', 'lecturer_id', 'status']

class ScheduleFilter(django_filters.FilterSet):
    course_offering_id = django_filters.UUIDFilter(field_name='course_offering_id')
    room_id = django_filters.UUIDFilter(field_name='room_id')
    day_of_week = django_filters.CharFilter(field_name='day_of_week')

    class Meta:
        model = Schedule
        fields = ['course_offering_id', 'room_id', 'day_of_week']
