"""
Master Data Views
=================
Tầng Giao tiếp HTTP. Rất mỏng, chỉ nhận Request, gọi Service Layer và trả Response.
Tuyệt đối không query DB hay cập nhật Data trực tiếp ở đây.
"""
from typing import Any, Tuple
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester,
    Specialization, EducationSystem, AcademicYear, AdministrativeClass
)
from .selectors import (
    DepartmentSelector, MajorSelector, RoomSelector, PriorityCategorySelector,
    ExamTypeSelector, CohortSelector, SemesterSelector,
    SpecializationSelector, EducationSystemSelector, AcademicYearSelector,
    AdministrativeClassSelector
)
from .services import (
    DepartmentService, MajorService, RoomService, PriorityCategoryService,
    ExamTypeService, CohortService, SemesterService
)
from .serializers import (
    DepartmentSerializer, MajorSerializer, RoomSerializer, PriorityCategorySerializer,
    ExamTypeSerializer, CohortSerializer, SemesterSerializer,
    SpecializationSerializer, EducationSystemSerializer, AcademicYearSerializer,
    AdministrativeClassSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    """API endpoint xử lý CRUD cho Khoa/Bộ môn"""
    queryset = DepartmentSelector.get_departments()
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['type', 'is_active', 'parent_id']

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        """
        Ghi đè hàm xóa (DELETE) để gọi qua Service Layer.
        Why: Đảm bảo mọi quy tắc Business (validate ràng buộc trước khi xóa) đều được thực thi.
        """
        department = self.get_object()
        try:
            DepartmentService.delete_department(department)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))

class MajorViewSet(viewsets.ModelViewSet):
    """API endpoint xử lý CRUD cho Ngành học"""
    queryset = MajorSelector.get_majors()
    serializer_class = MajorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['department_id']

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        major = self.get_object()
        try:
            MajorService.delete_major(major)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))

class RoomViewSet(viewsets.ModelViewSet):
    """API endpoint xử lý CRUD cho Phòng học"""
    queryset = RoomSelector.get_rooms()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name', 'type']
    filterset_fields = ['status', 'type']

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        room = self.get_object()
        try:
            RoomService.delete_room(room)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))

class PriorityCategoryViewSet(viewsets.ModelViewSet):
    """API endpoint cho Đối tượng ưu tiên"""
    queryset = PriorityCategorySelector.get_categories()
    serializer_class = PriorityCategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['is_active']

class ExamTypeViewSet(viewsets.ModelViewSet):
    """API endpoint cho Hình thức thi"""
    queryset = ExamTypeSelector.get_exam_types()
    serializer_class = ExamTypeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['is_active']

class CohortViewSet(viewsets.ModelViewSet):
    """API endpoint cho Khóa học"""
    queryset = CohortSelector.get_cohorts()
    serializer_class = CohortSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['is_active', 'admission_year']

class SemesterViewSet(viewsets.ModelViewSet):
    """API endpoint cho Học kỳ"""
    queryset = SemesterSelector.get_semesters()
    serializer_class = SemesterSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['academic_year_id', 'is_current', 'season']

class SpecializationViewSet(viewsets.ModelViewSet):
    """API endpoint cho Chuyên ngành"""
    queryset = SpecializationSelector.get_specializations()
    serializer_class = SpecializationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['major_id', 'is_active']

class EducationSystemViewSet(viewsets.ModelViewSet):
    """API endpoint cho Hệ đào tạo"""
    queryset = EducationSystemSelector.get_education_systems()
    serializer_class = EducationSystemSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['is_active']

class AcademicYearViewSet(viewsets.ModelViewSet):
    """API endpoint cho Năm học"""
    queryset = AcademicYearSelector.get_academic_years()
    serializer_class = AcademicYearSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['is_active', 'is_current']

class AdministrativeClassViewSet(viewsets.ModelViewSet):
    """API endpoint cho Lớp hành chính"""
    queryset = AdministrativeClassSelector.get_administrative_classes()
    serializer_class = AdministrativeClassSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['code', 'name']
    filterset_fields = ['major_id', 'cohort_id', 'is_active']
