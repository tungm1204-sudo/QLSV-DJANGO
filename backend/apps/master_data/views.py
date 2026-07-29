"""
Master Data Views
=================
ViewSet CRUD cho toàn bộ 21 danh mục gốc (Master Data).
Mỗi ViewSet tuân thủ Service Layer: View → Selector → Service, không query DB trực tiếp.
Tích hợp DjangoFilterBackend và SearchFilter thông qua FilterMixin để hỗ trợ ?search= và ?field=.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly
from . import selectors, services, serializers, filters


class FilterMixin:
    """
    Mixin cung cấp khả năng Filter và Search cho ViewSet.
    Tích hợp DjangoFilterBackend (lọc theo field cụ thể) và SearchFilter (tìm kiếm full-text).
    """
    filter_backends = [DjangoFilterBackend, SearchFilter]

    def filter_queryset(self, queryset):
        # Áp dụng lần lượt từng backend lên queryset
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset


# ─────────────────────────────────────────────────────────────
# NHÓM 1: HỆ ĐÀO TẠO & CẤU TRÚC TỔ CHỨC
# ─────────────────────────────────────────────────────────────

class EducationSystemViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_education_systems()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.EducationSystemReadSerializer(page, many=True).data)

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


class DepartmentViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.DepartmentFilter
    search_fields = ['code', 'name', 'phone', 'email']

    def list(self, request):
        qs = selectors.get_departments()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.DepartmentReadSerializer(page, many=True).data)

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


class MajorViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.MajorFilter
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_majors()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.MajorReadSerializer(page, many=True).data)

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


class SpecializationViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.SpecializationFilter
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_specializations()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.SpecializationReadSerializer(page, many=True).data)

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


# ─────────────────────────────────────────────────────────────
# NHÓM 2: CƠ SỞ VẬT CHẤT
# ─────────────────────────────────────────────────────────────

class CampusViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name', 'address']

    def list(self, request):
        qs = selectors.get_campuss()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.CampusReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.CampusWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_campus(**serializer.validated_data)
        return Response(serializers.CampusReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_campus_by_id(pk)
        return Response(serializers.CampusReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_campus_by_id(pk)
        serializer = serializers.CampusWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_campus(obj, **serializer.validated_data)
        return Response(serializers.CampusReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_campus_by_id(pk)
        services.delete_campus(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BuildingViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.BuildingFilter
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_buildings()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.BuildingReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.BuildingWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_building(**serializer.validated_data)
        return Response(serializers.BuildingReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_building_by_id(pk)
        return Response(serializers.BuildingReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_building_by_id(pk)
        serializer = serializers.BuildingWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_building(obj, **serializer.validated_data)
        return Response(serializers.BuildingReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_building_by_id(pk)
        services.delete_building(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoomViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.RoomFilter
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_rooms()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.RoomReadSerializer(page, many=True).data)

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


# ─────────────────────────────────────────────────────────────
# NHÓM 3: THỜI GIAN ĐÀO TẠO
# ─────────────────────────────────────────────────────────────

class CohortViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_cohorts()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.CohortReadSerializer(page, many=True).data)

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


class AcademicYearViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_academic_years()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.AcademicYearReadSerializer(page, many=True).data)

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


class SemesterViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.SemesterFilter
    search_fields = ['code']

    def list(self, request):
        qs = selectors.get_semesters()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.SemesterReadSerializer(page, many=True).data)

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


class AdministrativeClassViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = filters.AdministrativeClassFilter
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_administrative_classs()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.AdministrativeClassReadSerializer(page, many=True).data)

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


# ─────────────────────────────────────────────────────────────
# NHÓM 4: KHẢO THÍ & ƯU TIÊN
# ─────────────────────────────────────────────────────────────

class PriorityCategoryViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_priority_categorys()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.PriorityCategoryReadSerializer(page, many=True).data)

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


class ExamTypeViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_exam_types()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.ExamTypeReadSerializer(page, many=True).data)

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


# ─────────────────────────────────────────────────────────────
# NHÓM 5: NHÂN KHẨU HỌC
# ─────────────────────────────────────────────────────────────

class EthnicityViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_ethnicities()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.EthnicityReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.EthnicityWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_ethnicity(**serializer.validated_data)
        return Response(serializers.EthnicityReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_ethnicity_by_id(pk)
        return Response(serializers.EthnicityReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_ethnicity_by_id(pk)
        serializer = serializers.EthnicityWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_ethnicity(obj, **serializer.validated_data)
        return Response(serializers.EthnicityReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_ethnicity_by_id(pk)
        services.delete_ethnicity(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReligionViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_religions()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.ReligionReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.ReligionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_religion(**serializer.validated_data)
        return Response(serializers.ReligionReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_religion_by_id(pk)
        return Response(serializers.ReligionReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_religion_by_id(pk)
        serializer = serializers.ReligionWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_religion(obj, **serializer.validated_data)
        return Response(serializers.ReligionReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_religion_by_id(pk)
        services.delete_religion(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NationalityViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_nationalities()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.NationalityReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.NationalityWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_nationality(**serializer.validated_data)
        return Response(serializers.NationalityReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_nationality_by_id(pk)
        return Response(serializers.NationalityReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_nationality_by_id(pk)
        serializer = serializers.NationalityWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_nationality(obj, **serializer.validated_data)
        return Response(serializers.NationalityReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_nationality_by_id(pk)
        services.delete_nationality(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────────────────────
# NHÓM 6: NHÂN SỰ - HỌC VỊ, HỌC HÀM, TUYỂN SINH, CHỨC VỤ
# ─────────────────────────────────────────────────────────────

class DegreeViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_degrees()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.DegreeReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.DegreeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_degree(**serializer.validated_data)
        return Response(serializers.DegreeReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_degree_by_id(pk)
        return Response(serializers.DegreeReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_degree_by_id(pk)
        serializer = serializers.DegreeWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_degree(obj, **serializer.validated_data)
        return Response(serializers.DegreeReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_degree_by_id(pk)
        services.delete_degree(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcademicTitleViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_academictitles()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.AcademicTitleReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.AcademicTitleWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_academictitle(**serializer.validated_data)
        return Response(serializers.AcademicTitleReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_academictitle_by_id(pk)
        return Response(serializers.AcademicTitleReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_academictitle_by_id(pk)
        serializer = serializers.AcademicTitleWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_academictitle(obj, **serializer.validated_data)
        return Response(serializers.AcademicTitleReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_academictitle_by_id(pk)
        services.delete_academictitle(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdmissionTypeViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_admissiontypes()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.AdmissionTypeReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.AdmissionTypeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_admissiontype(**serializer.validated_data)
        return Response(serializers.AdmissionTypeReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_admissiontype_by_id(pk)
        return Response(serializers.AdmissionTypeReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_admissiontype_by_id(pk)
        serializer = serializers.AdmissionTypeWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_admissiontype(obj, **serializer.validated_data)
        return Response(serializers.AdmissionTypeReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_admissiontype_by_id(pk)
        services.delete_admissiontype(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PositionViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_positions()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.PositionReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.PositionWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_position(**serializer.validated_data)
        return Response(serializers.PositionReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_position_by_id(pk)
        return Response(serializers.PositionReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_position_by_id(pk)
        serializer = serializers.PositionWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_position(obj, **serializer.validated_data)
        return Response(serializers.PositionReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_position_by_id(pk)
        services.delete_position(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ─────────────────────────────────────────────────────────────
# NHÓM 7: LOẠI HỌC PHẦN
# ─────────────────────────────────────────────────────────────

class CourseTypeViewSet(FilterMixin, viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['code', 'name']

    def list(self, request):
        qs = selectors.get_coursetypes()
        qs = self.filter_queryset(qs)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        return paginator.get_paginated_response(serializers.CourseTypeReadSerializer(page, many=True).data)

    def create(self, request):
        serializer = serializers.CourseTypeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_course_type(**serializer.validated_data)
        return Response(serializers.CourseTypeReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_course_type_by_id(pk)
        return Response(serializers.CourseTypeReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_course_type_by_id(pk)
        serializer = serializers.CourseTypeWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_course_type(obj, **serializer.validated_data)
        return Response(serializers.CourseTypeReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_course_type_by_id(pk)
        services.delete_course_type(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
