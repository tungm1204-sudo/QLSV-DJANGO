"""
Master Data Views
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly
from . import selectors, services, serializers

class EducationSystemViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_education_systems(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.EducationSystemReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.EducationSystemWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_education_system(**serializer.validated_data)
        return Response(serializers.EducationSystemReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_education_system_by_id(pk)
        return Response(serializers.EducationSystemReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_education_system_by_id(pk)
        serializer = serializers.EducationSystemWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_education_system(obj, **serializer.validated_data)
        return Response(serializers.EducationSystemReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_education_system_by_id(pk)
        services.delete_education_system(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class DepartmentViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_departments(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.DepartmentReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.DepartmentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_department(**serializer.validated_data)
        return Response(serializers.DepartmentReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_department_by_id(pk)
        return Response(serializers.DepartmentReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_department_by_id(pk)
        serializer = serializers.DepartmentWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_department(obj, **serializer.validated_data)
        return Response(serializers.DepartmentReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_department_by_id(pk)
        services.delete_department(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MajorViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_majors(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.MajorReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.MajorWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_major(**serializer.validated_data)
        return Response(serializers.MajorReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_major_by_id(pk)
        return Response(serializers.MajorReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_major_by_id(pk)
        serializer = serializers.MajorWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_major(obj, **serializer.validated_data)
        return Response(serializers.MajorReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_major_by_id(pk)
        services.delete_major(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SpecializationViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_specializations(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.SpecializationReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.SpecializationWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_specialization(**serializer.validated_data)
        return Response(serializers.SpecializationReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_specialization_by_id(pk)
        return Response(serializers.SpecializationReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_specialization_by_id(pk)
        serializer = serializers.SpecializationWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_specialization(obj, **serializer.validated_data)
        return Response(serializers.SpecializationReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_specialization_by_id(pk)
        services.delete_specialization(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_rooms(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.RoomReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.RoomWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_room(**serializer.validated_data)
        return Response(serializers.RoomReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_room_by_id(pk)
        return Response(serializers.RoomReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_room_by_id(pk)
        serializer = serializers.RoomWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_room(obj, **serializer.validated_data)
        return Response(serializers.RoomReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_room_by_id(pk)
        services.delete_room(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class PriorityCategoryViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_priority_categorys(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.PriorityCategoryReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.PriorityCategoryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_priority_category(**serializer.validated_data)
        return Response(serializers.PriorityCategoryReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_priority_category_by_id(pk)
        return Response(serializers.PriorityCategoryReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_priority_category_by_id(pk)
        serializer = serializers.PriorityCategoryWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_priority_category(obj, **serializer.validated_data)
        return Response(serializers.PriorityCategoryReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_priority_category_by_id(pk)
        services.delete_priority_category(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExamTypeViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_exam_types(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.ExamTypeReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.ExamTypeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_exam_type(**serializer.validated_data)
        return Response(serializers.ExamTypeReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_exam_type_by_id(pk)
        return Response(serializers.ExamTypeReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_exam_type_by_id(pk)
        serializer = serializers.ExamTypeWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_exam_type(obj, **serializer.validated_data)
        return Response(serializers.ExamTypeReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_exam_type_by_id(pk)
        services.delete_exam_type(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CohortViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_cohorts(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.CohortReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.CohortWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_cohort(**serializer.validated_data)
        return Response(serializers.CohortReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_cohort_by_id(pk)
        return Response(serializers.CohortReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_cohort_by_id(pk)
        serializer = serializers.CohortWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_cohort(obj, **serializer.validated_data)
        return Response(serializers.CohortReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_cohort_by_id(pk)
        services.delete_cohort(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AcademicYearViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_academic_years(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.AcademicYearReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.AcademicYearWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_academic_year(**serializer.validated_data)
        return Response(serializers.AcademicYearReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_academic_year_by_id(pk)
        return Response(serializers.AcademicYearReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_academic_year_by_id(pk)
        serializer = serializers.AcademicYearWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_academic_year(obj, **serializer.validated_data)
        return Response(serializers.AcademicYearReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_academic_year_by_id(pk)
        services.delete_academic_year(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SemesterViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_semesters(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.SemesterReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.SemesterWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_semester(**serializer.validated_data)
        return Response(serializers.SemesterReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_semester_by_id(pk)
        return Response(serializers.SemesterReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_semester_by_id(pk)
        serializer = serializers.SemesterWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_semester(obj, **serializer.validated_data)
        return Response(serializers.SemesterReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_semester_by_id(pk)
        services.delete_semester(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdministrativeClassViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_administrative_classs(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.AdministrativeClassReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.AdministrativeClassWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_administrative_class(**serializer.validated_data)
        return Response(serializers.AdministrativeClassReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_administrative_class_by_id(pk)
        return Response(serializers.AdministrativeClassReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_administrative_class_by_id(pk)
        serializer = serializers.AdministrativeClassWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_administrative_class(obj, **serializer.validated_data)
        return Response(serializers.AdministrativeClassReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_administrative_class_by_id(pk)
        services.delete_administrative_class(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


