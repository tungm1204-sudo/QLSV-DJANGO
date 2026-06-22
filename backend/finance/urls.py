from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TuitionFeeViewSet

router = DefaultRouter()
router.register(r'tuition', TuitionFeeViewSet, basename='tuition')

urlpatterns = [
    path('', include(router.urls)),
]
