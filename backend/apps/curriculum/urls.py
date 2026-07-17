"""
Curriculum URLs
===============
Định tuyến URL cho Module Đào tạo.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, TrainingProgramViewSet, PrerequisiteViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'training-programs', TrainingProgramViewSet, basename='training-program')
router.register(r'prerequisites', PrerequisiteViewSet, basename='prerequisite')

urlpatterns = [
    path('', include(router.urls)),
]
