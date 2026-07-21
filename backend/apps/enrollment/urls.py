from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.enrollment.views import StudentEnrollmentViewSet, CourseOfferingEnrollmentViewSet

router = DefaultRouter()
router.register(r'my-enrollments', StudentEnrollmentViewSet, basename='my-enrollments')
router.register(r'classes', CourseOfferingEnrollmentViewSet, basename='enrollment-classes')

urlpatterns = [
    path('', include(router.urls)),
]
