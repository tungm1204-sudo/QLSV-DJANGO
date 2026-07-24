"""
Curriculum URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'training-program', views.TrainingProgramViewSet, basename='training_program')
router.register(r'prerequisite', views.PrerequisiteViewSet, basename='prerequisite')
router.register(r'equivalent-course', views.EquivalentCourseViewSet, basename='equivalent_course')

urlpatterns = [
    path("", include(router.urls)),
]
