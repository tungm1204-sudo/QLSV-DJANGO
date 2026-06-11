from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register(r"parents", ParentViewSet, basename="parent")     # API quản lý Phụ huynh
router.register(r"profiles", StudentProfileViewSet, basename="student")  # API quản lý Hồ sơ sinh viên (lookup theo mssv)

urlpatterns = [
    path("", include(router.urls)),
]
