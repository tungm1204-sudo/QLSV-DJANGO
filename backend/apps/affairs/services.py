"""
Affairs Services
================
Business Logic cho Module CTSV.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import RewardDisciplineCategory

class RewardDisciplineCategoryService:
    @staticmethod
    @transaction.atomic
    def delete_category(category: RewardDisciplineCategory) -> None:
        """Xóa danh mục khen thưởng / kỷ luật."""
        category.delete()
