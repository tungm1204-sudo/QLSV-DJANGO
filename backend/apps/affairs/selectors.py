"""
Affairs Selectors
"""
from typing import Iterable
from .models import RewardDisciplineCategory

def get_reward_discipline_categorys(*, is_active: bool = None) -> Iterable[RewardDisciplineCategory]:
    qs = RewardDisciplineCategory.objects.all()
    if is_active is not None:
        qs = qs.filter(is_active=is_active)
    return qs

def get_reward_discipline_category_by_id(id: str) -> RewardDisciplineCategory:
    return RewardDisciplineCategory.objects.get(id=id)

