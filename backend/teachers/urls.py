from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, TeacherProfileViewSet

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"profiles", TeacherProfileViewSet, basename="teacher")

urlpatterns = [
    path("", include(router.urls)),
]
