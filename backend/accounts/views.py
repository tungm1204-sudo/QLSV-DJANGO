from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer, UserSerializer, ChangePasswordSerializer
from .models import User


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Mục đích: Xác thực người dùng và trả về cặp JWT (access + refresh token).
    Input: { username, password }
    Output: { access, refresh, user: { id, username, email, role, ... } }
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny] # Endpoint công khai, không cần xác thực trước


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Mục đích: Đăng xuất người dùng bằng cách blacklist refresh token, vô hiệu hoá phiên đăng nhập hiện tại.
    Input: { refresh: "<refresh_token>" }
    Output: { detail: "Đăng xuất thành công." }
    Lưu ý: Cần bật SIMPLE_JWT blacklist app trong INSTALLED_APPS để tính năng này hoạt động.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Input: request.data phải chứa key "refresh" là chuỗi refresh token hợp lệ.
        Các trường hợp đặc biệt: Trả về 400 nếu token không hợp lệ hoặc đã hết hạn.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Đăng xuất thành công."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Token không hợp lệ hoặc đã hết hạn."}, status=status.HTTP_400_BAD_REQUEST)


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
