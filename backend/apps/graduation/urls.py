from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GraduationConditionViewSet, GraduationSessionViewSet, 
    GraduationCandidateViewSet, DiplomaViewSet, 
    DefenseCouncilViewSet, ThesisViewSet
)

router = DefaultRouter()
router.register(r'conditions', GraduationConditionViewSet, basename='graduation-condition')
router.register(r'sessions', GraduationSessionViewSet, basename='graduation-session')
router.register(r'candidates', GraduationCandidateViewSet, basename='graduation-candidate')
router.register(r'diplomas', DiplomaViewSet, basename='diploma')
router.register(r'councils', DefenseCouncilViewSet, basename='defense-council')
router.register(r'theses', ThesisViewSet, basename='thesis')

urlpatterns = [
    path('', include(router.urls)),
]
