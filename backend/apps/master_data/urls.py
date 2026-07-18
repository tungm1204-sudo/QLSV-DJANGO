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
    ExamTypeViewSet, CohortViewSet, SemesterViewSet,
    SpecializationViewSet, EducationSystemViewSet, AcademicYearViewSet
)

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'majors', MajorViewSet, basename='major')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'priority-categories', PriorityCategoryViewSet, basename='priority-category')
router.register(r'exam-types', ExamTypeViewSet, basename='exam-type')
router.register(r'cohorts', CohortViewSet, basename='cohort')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'specializations', SpecializationViewSet, basename='specialization')
router.register(r'education-systems', EducationSystemViewSet, basename='education-system')
router.register(r'academic-years', AcademicYearViewSet, basename='academic-year')

urlpatterns = [
    path('', include(router.urls)),
]
