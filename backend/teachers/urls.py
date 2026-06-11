from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, TeacherProfileViewSet

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="department")  # API quản lý Khoa / Bộ môn
router.register(r"profiles", TeacherProfileViewSet, basename="teacher")    # API quản lý Hồ sơ giảng viên (lookup theo mgv)

urlpatterns = [
    path("", include(router.urls)),
]
