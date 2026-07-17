"""
Master Data URLs
================
Định tuyến URL cho Module Danh mục Master Data.
Dùng DefaultRouter để tự sinh ra các RESTful endpoints chuẩn.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet, MajorViewSet, RoomViewSet, PriorityCategoryViewSet,
    ExamTypeViewSet, CohortViewSet, SemesterViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'majors', MajorViewSet, basename='major')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'priority-categories', PriorityCategoryViewSet, basename='priority-category')
router.register(r'exam-types', ExamTypeViewSet, basename='exam-type')
router.register(r'cohorts', CohortViewSet, basename='cohort')
router.register(r'semesters', SemesterViewSet, basename='semester')

urlpatterns = [
    path('', include(router.urls)),
]

from rest_framework import viewsets
from .serializers import SpecializationSerializer, EducationSystemSerializer, AcademicYearSerializer
from .selectors import SpecializationSelector, EducationSystemSelector, AcademicYearSelector

class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = SpecializationSelector.get_specializations()
    serializer_class = SpecializationSerializer

class EducationSystemViewSet(viewsets.ModelViewSet):
    queryset = EducationSystemSelector.get_education_systems()
    serializer_class = EducationSystemSerializer

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYearSelector.get_academic_years()
    serializer_class = AcademicYearSerializer

router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'education-systems', EducationSystemViewSet, basename='education-system')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')
