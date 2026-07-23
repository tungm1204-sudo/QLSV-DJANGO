from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemConfigViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'system-configs', SystemConfigViewSet, basename='systemconfig')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
]
