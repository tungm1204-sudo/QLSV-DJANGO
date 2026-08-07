from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.curriculum.models import CourseOffering
from apps.enrollment.models import Enrollment
from apps.finance.services import refund_tuition_for_cancelled_course

@receiver(post_save, sender=CourseOffering)
def handle_course_offering_cancellation(sender, instance, created, **kwargs):
    if not created and instance.status == 'CANCELLED':
        # Tìm tất cả sinh viên đã đăng ký lớp này
        enrollments = Enrollment.objects.filter(course_offering=instance)
        for enrollment in enrollments:
            refund_tuition_for_cancelled_course(enrollment.student_id, instance)
