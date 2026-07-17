"""
Affairs Selectors
=================
Truy vấn DB cho Module CTSV.
"""
from django.db.models import QuerySet
from .models import RewardDisciplineCategory

class RewardDisciplineCategorySelector:
    @staticmethod
    def get_categories() -> QuerySet[RewardDisciplineCategory]:
        """Lấy toàn bộ danh sách Khen thưởng / Kỷ luật."""
        return RewardDisciplineCategory.objects.all()
