from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, CustomTokenObtainPairView, RoleViewSet, 
    SystemConfigViewSet, NotificationViewSet, AuditLogViewSet,
    request_otp, verify_otp, logout, reset_password
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'system-configs', SystemConfigViewSet, basename='systemconfig')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    # Auth endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout, name='logout'),
    path('auth/request-otp/', request_otp, name='request_otp'),
    path('auth/verify-otp/', verify_otp, name='verify_otp'),
    path('auth/reset-password/', reset_password, name='reset_password'),
    
    # ViewSets
    path('', include(router.urls)),
]
