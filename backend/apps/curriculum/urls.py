"""
Curriculum URLs
===============
Định tuyến URL cho Module Đào tạo.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, TrainingProgramViewSet, PrerequisiteViewSet, EquivalentCourseViewSet,
    TrainingPlanViewSet, CourseOfferingViewSet, ScheduleViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'training-programs', TrainingProgramViewSet, basename='training-program')
router.register(r'prerequisites', PrerequisiteViewSet, basename='prerequisite')
router.register(r'equivalent-courses', EquivalentCourseViewSet, basename='equivalent-course')
router.register(r'training-plans', TrainingPlanViewSet, basename='training-plan')
router.register(r'course-offerings', CourseOfferingViewSet, basename='course-offering')
router.register(r'schedules', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(router.urls)),
]
