"""
Affairs Services
"""
from django.db import transaction
from .models import RewardDisciplineCategory

@transaction.atomic
def create_reward_discipline_category(**data) -> RewardDisciplineCategory:
    obj = RewardDisciplineCategory(**data)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def update_reward_discipline_category(obj: RewardDisciplineCategory, **data) -> RewardDisciplineCategory:
    for key, value in data.items():
        setattr(obj, key, value)
    obj.full_clean()
    obj.save()
    return obj

@transaction.atomic
def delete_reward_discipline_category(obj: RewardDisciplineCategory):
    obj.is_active = False
    obj.save(update_fields=['is_active'])

