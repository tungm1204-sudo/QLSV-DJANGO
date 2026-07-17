"""
Curriculum Views
================
Controller điều hướng API REST cho Module Đào tạo.
Mỏng nhất có thể.
"""
from typing import Any, Tuple
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError

from .models import Course, TrainingProgram, Prerequisite
from .selectors import CourseSelector, TrainingProgramSelector, PrerequisiteSelector
from .services import CourseService, TrainingProgramService, PrerequisiteService
from .serializers import CourseSerializer, TrainingProgramSerializer, PrerequisiteSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """API Endpoint Quản lý Môn học"""
    queryset = CourseSelector.get_courses()
    serializer_class = CourseSerializer

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        """Ghi đè DELETE để chạy logic trong Service Layer."""
        course = self.get_object()
        try:
            CourseService.delete_course(course)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))

class TrainingProgramViewSet(viewsets.ModelViewSet):
    """API Endpoint Quản lý Khung Chương trình đào tạo"""
    queryset = TrainingProgramSelector.get_training_programs()
    serializer_class = TrainingProgramSerializer

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        program = self.get_object()
        try:
            TrainingProgramService.delete_training_program(program)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))

class PrerequisiteViewSet(viewsets.ModelViewSet):
    """API Endpoint Quản lý Môn tiên quyết"""
    queryset = PrerequisiteSelector.get_prerequisites()
    serializer_class = PrerequisiteSerializer

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        prerequisite = self.get_object()
        try:
            PrerequisiteService.delete_prerequisite(prerequisite)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))
