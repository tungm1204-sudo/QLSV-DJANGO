"""
Affairs Views
=============
REST API Controllers cho Module CTSV.
"""
from typing import Any, Tuple
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError

from .models import RewardDisciplineCategory
from .selectors import RewardDisciplineCategorySelector
from .services import RewardDisciplineCategoryService
from .serializers import RewardDisciplineCategorySerializer

class RewardDisciplineCategoryViewSet(viewsets.ModelViewSet):
    """API Endpoint cho Danh mục Khen thưởng / Kỷ luật"""
    queryset = RewardDisciplineCategorySelector.get_categories()
    serializer_class = RewardDisciplineCategorySerializer

    def destroy(self, request: Request, *args: Tuple[Any], **kwargs: dict[str, Any]) -> Response:
        """Xóa bằng cách gọi Service."""
        category = self.get_object()
        try:
            RewardDisciplineCategoryService.delete_category(category)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            raise DRFValidationError(detail=str(e.message))
