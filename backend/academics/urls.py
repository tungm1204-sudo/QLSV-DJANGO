from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SemesterViewSet, GradeViewSet, CourseViewSet, 
    ClassroomViewSet, CourseAssignmentViewSet, 
    AttendanceViewSet, ExamTypeViewSet, ExamResultViewSet
)

# Khởi tạo DefaultRouter từ DRF để tự động tạo ra các URL cho các viewset
router = DefaultRouter()

# Đăng ký các route cho các API CRUD cơ bản
router.register(r"semesters", SemesterViewSet)        # API quản lý Học kỳ (GET, POST, PUT, DELETE)
router.register(r"grades", GradeViewSet)              # API quản lý Khóa/Năm học
router.register(r"courses", CourseViewSet)            # API quản lý Môn học
router.register(r"classrooms", ClassroomViewSet)      # API quản lý Lớp học
router.register(r"assignments", CourseAssignmentViewSet) # API phân công giảng viên dạy môn
router.register(r"attendances", AttendanceViewSet)    # API điểm danh
router.register(r"exam-types", ExamTypeViewSet)       # API quản lý Loại kỳ thi (giữa kỳ, cuối kỳ)
router.register(r"exam-results", ExamResultViewSet)   # API lưu trữ và quản lý điểm thi

urlpatterns = [
    # Include tất cả các route đã đăng ký vào path gốc của app
    path("", include(router.urls)),
]
