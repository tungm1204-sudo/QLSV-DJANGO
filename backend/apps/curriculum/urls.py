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

from rest_framework import viewsets
from .serializers import EquivalentCourseSerializer
from .selectors import EquivalentCourseSelector

class EquivalentCourseViewSet(viewsets.ModelViewSet):
    queryset = EquivalentCourseSelector.get_equivalent_courses()
    serializer_class = EquivalentCourseSerializer

router.register(r'equivalent-courses', EquivalentCourseViewSet, basename='equivalent-course')
