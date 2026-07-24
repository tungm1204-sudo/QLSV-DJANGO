"""
Affairs Views
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.core.pagination import CustomPagination
from apps.core.permissions import IsAdminOrReadOnly
from . import selectors, services, serializers

class RewardDisciplineCategoryViewSet(viewsets.ViewSet):
    pagination_class = CustomPagination
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request):
        is_active = request.query_params.get('is_active')
        if is_active is not None:
            is_active = str(is_active).lower() == 'true'
        qs = selectors.get_reward_discipline_categorys(is_active=is_active)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)
        serializer = serializers.RewardDisciplineCategoryReadSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = serializers.RewardDisciplineCategoryWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = services.create_reward_discipline_category(**serializer.validated_data)
        return Response(serializers.RewardDisciplineCategoryReadSerializer(obj).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        obj = selectors.get_reward_discipline_category_by_id(pk)
        return Response(serializers.RewardDisciplineCategoryReadSerializer(obj).data)

    def update(self, request, pk=None):
        obj = selectors.get_reward_discipline_category_by_id(pk)
        serializer = serializers.RewardDisciplineCategoryWriteSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_obj = services.update_reward_discipline_category(obj, **serializer.validated_data)
        return Response(serializers.RewardDisciplineCategoryReadSerializer(updated_obj).data)

    def destroy(self, request, pk=None):
        obj = selectors.get_reward_discipline_category_by_id(pk)
        services.delete_reward_discipline_category(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


