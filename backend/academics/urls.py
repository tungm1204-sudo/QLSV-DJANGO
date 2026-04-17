from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SemesterViewSet, GradeViewSet, CourseViewSet, 
    ClassroomViewSet, CourseAssignmentViewSet, 
    AttendanceViewSet, ExamTypeViewSet, ExamResultViewSet
)

router = DefaultRouter()
router.register(r"semesters", SemesterViewSet)
router.register(r"grades", GradeViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"classrooms", ClassroomViewSet)
router.register(r"assignments", CourseAssignmentViewSet)
router.register(r"attendances", AttendanceViewSet)
router.register(r"exam-types", ExamTypeViewSet)
router.register(r"exam-results", ExamResultViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
