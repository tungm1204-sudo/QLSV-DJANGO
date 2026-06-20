from django.urls import path
from .views import LoginView, LogoutView, MeView, ChangePasswordView, CookieTokenRefreshView

# Tất cả các URL xác thực đều được mount dưới prefix /api/auth/ (xem qlsv/urls.py)
urlpatterns = [
    path("login/", LoginView.as_view(), name="auth-login"),                    # Đăng nhập, lấy access + refresh token
    path("logout/", LogoutView.as_view(), name="auth-logout"),                  # Đăng xuất (blacklist token)
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="auth-token-refresh"), # Làm mới access token bằng HttpOnly Cookie
    path("me/", MeView.as_view(), name="auth-me"),                              # Xem / cập nhật thông tin bản thân
    path("change-password/", ChangePasswordView.as_view(), name="auth-change-password"), # Đổi mật khẩu
]
