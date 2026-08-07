"""
Affairs URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reward-discipline-category', views.RewardDisciplineCategoryViewSet, basename='reward_discipline_category')
router.register(r'student-reward-disciplines', views.StudentRewardDisciplineViewSet, basename='student_reward_discipline')
router.register(r'training-scores', views.TrainingScoreViewSet, basename='training_score')
router.register(r'scholarships', views.ScholarshipViewSet, basename='scholarship')
router.register(r'advising-sessions', views.AdvisingSessionViewSet, basename='advising_session')
router.register(r'health-insurances', views.HealthInsuranceViewSet, basename='health_insurance')
router.register(r'surveys', views.SurveyViewSet, basename='survey')
router.register(r'survey-questions', views.SurveyQuestionViewSet, basename='survey_question')
router.register(r'survey-responses', views.SurveyResponseViewSet, basename='survey_response')
urlpatterns = [
    path("", include(router.urls)),
]
