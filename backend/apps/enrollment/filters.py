import django_filters
from .models import Enrollment

class EnrollmentFilter(django_filters.FilterSet):
    student_id = django_filters.UUIDFilter(field_name='student_id')
    semester_id = django_filters.UUIDFilter(field_name='course_offering__semester_id')
    status = django_filters.ChoiceFilter(choices=Enrollment.EnrollmentStatusChoices.choices)

    class Meta:
        model = Enrollment
        fields = ['student_id', 'semester_id', 'status']
