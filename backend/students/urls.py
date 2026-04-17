from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, StudentProfileViewSet

router = DefaultRouter()
router.register(r"parents", ParentViewSet, basename="parent")
router.register(r"profiles", StudentProfileViewSet, basename="student")

urlpatterns = [
    path("", include(router.urls)),
]
