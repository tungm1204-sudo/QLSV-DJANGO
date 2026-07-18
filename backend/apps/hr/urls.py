"""
HR URLs
=======
Định tuyến URL cho Module Quản lý Nhân sự (Student, Lecturer, Staff).
Dùng DefaultRouter để tự sinh ra các RESTful endpoints chuẩn.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, LecturerViewSet, StaffViewSet


router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'lecturers', LecturerViewSet, basename='lecturer')
router.register(r'staffs', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]
