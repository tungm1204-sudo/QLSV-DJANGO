from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.exams.views import (
    ExamSessionViewSet, ExamRoomViewSet, GradeReviewViewSet,
    GradeHistoryViewSet, StudentAcademicRecordViewSet, GradingViewSet
)

router = DefaultRouter()
router.register(r'sessions', ExamSessionViewSet, basename='exam-session')
router.register(r'rooms', ExamRoomViewSet, basename='exam-room')
router.register(r'grade-reviews', GradeReviewViewSet, basename='grade-review')
router.register(r'grade-histories', GradeHistoryViewSet, basename='grade-history')
router.register(r'academic-records', StudentAcademicRecordViewSet, basename='academic-record')
router.register(r'grading', GradingViewSet, basename='grading')

urlpatterns = [
    path('', include(router.urls)),
]
