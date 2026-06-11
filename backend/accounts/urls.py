from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, MeView, ChangePasswordView

# Tất cả các URL xác thực đều được mount dưới prefix /api/auth/ (xem qlsv/urls.py)
urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),                    # Đăng nhập, lấy access + refresh token
    path("logout/", LogoutView.as_view(), name="auth-logout"),                  # Đăng xuất (blacklist token)
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"), # Làm mới access token khi hết hạn
    path("me/", MeView.as_view(), name="auth-me"),                              # Xem / cập nhật thông tin bản thân
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"), # Đổi mật khẩu
]
