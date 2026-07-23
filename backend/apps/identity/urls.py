"""
Module Identity URLs
Định tuyến các Endpoint API cho phân hệ Identity (Authentication, Users, Roles, Configs).
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserViewSet, CustomTokenObtainPairView, CustomTokenRefreshView, RoleViewSet, 

    LoginSessionViewSet,
    request_otp, verify_otp, logout_view, reset_password, request_password_reset_otp
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')

router.register(r'auth/sessions', LoginSessionViewSet, basename='loginsession')

urlpatterns = [
    # Auth endpoints
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/request-otp/', request_otp, name='request_otp'),
    path('auth/verify-otp/', verify_otp, name='verify_otp'),
    path('auth/password-reset/request-otp/', request_password_reset_otp, name='request_password_reset_otp'),
    path('auth/reset-password/', reset_password, name='reset_password'),
    
    # ViewSets
    path('', include(router.urls)),
]
