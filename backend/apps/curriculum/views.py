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

from . import filters
from rest_framework.decorators import action

class TrainingPlanViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        qs = selectors.get_training_plans()
        filterset = filters.TrainingPlanFilter(request.query_params, queryset=qs)
        qs = filterset.qs
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.TrainingPlanReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.TrainingPlanWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_training_plan(**serializer.validated_data)
        return Response(serializers.TrainingPlanReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_training_plan_by_id(pk)
        return Response(serializers.TrainingPlanReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_training_plan_by_id(pk)
        serializer = serializers.TrainingPlanWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_training_plan(obj, **serializer.validated_data)
        return Response(serializers.TrainingPlanReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_training_plan_by_id(pk)
        services.delete_training_plan(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        plan = selectors.get_training_plan_by_id(pk)
        new_semester_id = request.data.get('new_semester_id')
        new_name = request.data.get('new_name')
        if not new_semester_id or not new_name:
            return Response({"detail": "Thiếu new_semester_id hoặc new_name"}, status=status.HTTP_400_BAD_REQUEST)
        new_plan = services.duplicate_training_plan(plan, new_semester_id, new_name, request.user)
        return Response(serializers.TrainingPlanReadSerializer(new_plan).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        plan = selectors.get_training_plan_by_id(pk)
        new_status = request.data.get('status')
        updated_plan = services.approve_training_plan(plan, request.user, new_status)
        return Response(serializers.TrainingPlanReadSerializer(updated_plan).data)


class CourseOfferingViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        qs = selectors.get_course_offerings()
        filterset = filters.CourseOfferingFilter(request.query_params, queryset=qs)
        qs = filterset.qs
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.CourseOfferingReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.CourseOfferingWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_course_offering(**serializer.validated_data)
        return Response(serializers.CourseOfferingReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_course_offering_by_id(pk)
        return Response(serializers.CourseOfferingReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_course_offering_by_id(pk)
        serializer = serializers.CourseOfferingWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_course_offering(obj, **serializer.validated_data)
        return Response(serializers.CourseOfferingReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_course_offering_by_id(pk)
        services.delete_course_offering(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScheduleViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        qs = selectors.get_schedules()
        filterset = filters.ScheduleFilter(request.query_params, queryset=qs)
        qs = filterset.qs
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.ScheduleReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.ScheduleWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Lấy course_offering instance
        course_offering_id = serializer.validated_data.pop('course_offering', None)
        if not course_offering_id:
            return Response({"detail": "Thiếu course_offering"}, status=status.HTTP_400_BAD_REQUEST)
        
        # CourseOffering is already resolved by serializer if PrimaryKeyRelatedField, wait, DRF ModelSerializer resolves ForeignKey to instance.
        # So serializer.validated_data['course_offering'] is the instance!
        # Let me correct that.
        
        course_offering = serializer.validated_data.pop('course_offering')
        
        from django.core.exceptions import ValidationError as DjangoValidationError
        try:
            obj = services.create_schedule(course_offering=course_offering, **serializer.validated_data)
            return Response(serializers.ScheduleReadSerializer(obj).data, status=status.HTTP_201_CREATED)
        except DjangoValidationError as e:
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        obj = selectors.get_schedule_by_id(pk)
        return Response(serializers.ScheduleReadSerializer(obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_schedule_by_id(pk)
        services.delete_schedule(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
