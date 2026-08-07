from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemConfigViewSet, AuditLogViewSet, SystemBackupViewSet

router = DefaultRouter()
router.register(r'system-configs', SystemConfigViewSet, basename='systemconfig')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')
router.register(r'backups', SystemBackupViewSet, basename='systembackup')

urlpatterns = [
    path('', include(router.urls)),
]
