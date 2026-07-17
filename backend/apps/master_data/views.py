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

from .models import Department, Major, Room, PriorityCategory, ExamType, Cohort, Semester
from .selectors import (
    DepartmentSelector, MajorSelector, RoomSelector, PriorityCategorySelector, 
    ExamTypeSelector, CohortSelector, SemesterSelector
)
from .services import (
    DepartmentService, MajorService, RoomService, PriorityCategoryService, 
    ExamTypeService, CohortService, SemesterService
)
from .serializers import (
    DepartmentSerializer, MajorSerializer, RoomSerializer, PriorityCategorySerializer, 
    ExamTypeSerializer, CohortSerializer, SemesterSerializer
)

class DepartmentViewSet(viewsets.ModelViewSet):
    """API endpoint xử lý CRUD cho Khoa/Bộ môn"""
    queryset = DepartmentSelector.get_departments()
    serializer_class = DepartmentSerializer

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

class ExamTypeViewSet(viewsets.ModelViewSet):
    """API endpoint cho Hình thức thi"""
    queryset = ExamTypeSelector.get_exam_types()
    serializer_class = ExamTypeSerializer

class CohortViewSet(viewsets.ModelViewSet):
    """API endpoint cho Khóa học"""
    queryset = CohortSelector.get_cohorts()
    serializer_class = CohortSerializer

class SemesterViewSet(viewsets.ModelViewSet):
    """API endpoint cho Học kỳ"""
    queryset = SemesterSelector.get_semesters()
    serializer_class = SemesterSerializer
