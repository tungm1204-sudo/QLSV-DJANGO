"""
Affairs URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'reward-discipline-category', views.RewardDisciplineCategoryViewSet, basename='reward_discipline_category')

urlpatterns = [
    path("", include(router.urls)),
]
