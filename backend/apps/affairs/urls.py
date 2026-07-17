"""
Affairs URLs
============
Định tuyến URL cho CTSV.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RewardDisciplineCategoryViewSet

router = DefaultRouter()
router.register(r'reward-discipline-categories', RewardDisciplineCategoryViewSet, basename='reward-discipline-category')

urlpatterns = [
    path('', include(router.urls)),
]
