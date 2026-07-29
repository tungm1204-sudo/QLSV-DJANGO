"""
Master Data URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'education-system', views.EducationSystemViewSet, basename='education_system')
router.register(r'department', views.DepartmentViewSet, basename='department')
router.register(r'major', views.MajorViewSet, basename='major')
router.register(r'specialization', views.SpecializationViewSet, basename='specialization')
router.register(r'campus', views.CampusViewSet, basename='campus')
router.register(r'building', views.BuildingViewSet, basename='building')
router.register(r'room', views.RoomViewSet, basename='room')
router.register(r'priority-category', views.PriorityCategoryViewSet, basename='priority_category')
router.register(r'exam-type', views.ExamTypeViewSet, basename='exam_type')
router.register(r'cohort', views.CohortViewSet, basename='cohort')
router.register(r'academic-year', views.AcademicYearViewSet, basename='academic_year')
router.register(r'semester', views.SemesterViewSet, basename='semester')
router.register(r'administrative-class', views.AdministrativeClassViewSet, basename='administrative_class')
router.register(r'degree', views.DegreeViewSet, basename='degree')
router.register(r'academic-title', views.AcademicTitleViewSet, basename='academic_title')
router.register(r'admission-type', views.AdmissionTypeViewSet, basename='admission_type')
router.register(r'ethnicity', views.EthnicityViewSet, basename='ethnicity')
router.register(r'religion', views.ReligionViewSet, basename='religion')
router.register(r'nationality', views.NationalityViewSet, basename='nationality')
router.register(r'course-type', views.CourseTypeViewSet, basename='course_type')
router.register(r'position', views.PositionViewSet, basename='position')

urlpatterns = [
    path("", include(router.urls)),
]
