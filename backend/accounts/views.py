from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
from .models import User
import os

# Có thể check ENV để set secure=True trên production
IS_SECURE_COOKIE = os.environ.get("ENV") == "production"

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Mục đích: Xác thực người dùng và trả về cặp JWT.
    Refresh token sẽ được set vào HttpOnly Cookie để bảo mật.
    Output JSON chỉ chứa access token và user info.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            if refresh_token:
                response.set_cookie(
                    key='refresh_token',
                    value=refresh_token,
                    httponly=True,
                    secure=IS_SECURE_COOKIE,
                    samesite='Lax',
                    max_age=15 * 24 * 60 * 60 # 15 ngày
                )
                del response.data['refresh']
        return response

class CookieTokenRefreshView(TokenRefreshView):
    """
    POST /api/auth/token/refresh/
    Lấy refresh_token từ Cookie thay vì body request.
    """
    def post(self, request, *args, **kwargs):
        # Lấy từ cookie hoặc fallback qua body (phòng hờ)
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        
        if refresh_token:
            # Gắn vào data để parent class xử lý
            if not getattr(request, '_full_data_loaded', False):
                # Copy request data mutable nếu cần
                from django.http import QueryDict
                if isinstance(request.data, QueryDict):
                    request.data._mutable = True
            request.data['refresh'] = refresh_token
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            new_refresh_token = response.data.get('refresh')
            if new_refresh_token:
                response.set_cookie(
                    key='refresh_token',
                    value=new_refresh_token,
                    httponly=True,
                    secure=IS_SECURE_COOKIE,
                    samesite='Lax',
                    max_age=15 * 24 * 60 * 60
                )
                del response.data['refresh']
        return response

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Đăng xuất: Blacklist token và xoá Cookie.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token') or request.data.get('refresh')
        response = Response({"detail": "Đăng xuất thành công."}, status=status.HTTP_200_OK)
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass # Bỏ qua nếu token đã hết hạn hoặc bị lỗi
                
        response.delete_cookie('refresh_token')
        return response


class MeView(generics.RetrieveUpdateAPIView):
    """
    GET /api/auth/me/ — Lấy thông tin tài khoản của người dùng đang đăng nhập.
    PATCH /api/auth/me/ — Cập nhật thông tin cá nhân (không bao gồm mật khẩu).
    Output: Thông tin user hiện tại theo UserSerializer.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Trả về chính user đang thực hiện request, không cần truyền pk."""
        return self.request.user


class ChangePasswordView(APIView):
    """
    POST /api/auth/change-password/
    Mục đích: Cho phép người dùng đổi mật khẩu sau khi đã đăng nhập.
    Input: { old_password, new_password, confirm_password }
    Output: { detail: "Đổi mật khẩu thành công." } hoặc lỗi validation.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Luồng xử lý:
        1. Validate dữ liệu đầu vào (mật khẩu mới phải khớp xác nhận).
        2. Kiểm tra mật khẩu cũ có đúng không bằng check_password().
        3. Nếu đúng, gọi set_password() để hash mật khẩu mới và lưu.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Mật khẩu cũ không đúng."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"detail": "Đổi mật khẩu thành công."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
