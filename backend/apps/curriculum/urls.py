"""
Curriculum URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'training-program', views.TrainingProgramViewSet, basename='training_program')
router.register(r'knowledge-block', views.KnowledgeBlockViewSet, basename='knowledge_block')
router.register(r'training-program-course', views.TrainingProgramCourseViewSet, basename='training_program_course')
router.register(r'prerequisite', views.PrerequisiteViewSet, basename='prerequisite')
router.register(r'equivalent-course', views.EquivalentCourseViewSet, basename='equivalent_course')
router.register(r'training-plan', views.TrainingPlanViewSet, basename='training_plan')
router.register(r'course-offering', views.CourseOfferingViewSet, basename='course_offering')
router.register(r'schedule', views.ScheduleViewSet, basename='schedule')
urlpatterns = [
    path("", include(router.urls)),
]
