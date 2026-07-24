"""
Curriculum Views
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly
from . import selectors, services, serializers

class CourseViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_courses(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.CourseReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.CourseWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_course(**serializer.validated_data)
        return Response(serializers.CourseReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_course_by_id(pk)
        return Response(serializers.CourseReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_course_by_id(pk)
        serializer = serializers.CourseWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_course(obj, **serializer.validated_data)
        return Response(serializers.CourseReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_course_by_id(pk)
        services.delete_course(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class TrainingProgramViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_training_programs(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.TrainingProgramReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.TrainingProgramWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_training_program(**serializer.validated_data)
        return Response(serializers.TrainingProgramReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_training_program_by_id(pk)
        return Response(serializers.TrainingProgramReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_training_program_by_id(pk)
        serializer = serializers.TrainingProgramWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_training_program(obj, **serializer.validated_data)
        return Response(serializers.TrainingProgramReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_training_program_by_id(pk)
        services.delete_training_program(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PrerequisiteViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_prerequisites(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.PrerequisiteReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.PrerequisiteWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_prerequisite(**serializer.validated_data)
        return Response(serializers.PrerequisiteReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_prerequisite_by_id(pk)
        return Response(serializers.PrerequisiteReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_prerequisite_by_id(pk)
        serializer = serializers.PrerequisiteWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_prerequisite(obj, **serializer.validated_data)
        return Response(serializers.PrerequisiteReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_prerequisite_by_id(pk)
        services.delete_prerequisite(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class EquivalentCourseViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_equivalent_courses(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.EquivalentCourseReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.EquivalentCourseWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_equivalent_course(**serializer.validated_data)
        return Response(serializers.EquivalentCourseReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_equivalent_course_by_id(pk)
        return Response(serializers.EquivalentCourseReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_equivalent_course_by_id(pk)
        serializer = serializers.EquivalentCourseWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_equivalent_course(obj, **serializer.validated_data)
        return Response(serializers.EquivalentCourseReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_equivalent_course_by_id(pk)
        services.delete_equivalent_course(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


