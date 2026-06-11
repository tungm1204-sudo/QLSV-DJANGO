from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Class: CustomTokenObtainPairSerializer
    Mục đích: Tùy biến JWT token để nhúng thêm thông tin người dùng vào payload.
    Business logic: 
    - Ghi thêm `role`, `full_name`, `email` trực tiếp vào token payload để frontend
      decode ra dùng ngay mà không cần thêm request `/api/auth/me/`.
    - Đây là kỹ thuật stateless: mọi thông tin cần thiết đều nằm trong token.
    """

    @classmethod
    def get_token(cls, user):
        """
        Chức năng: Tạo JWT token và nhúng thêm custom claims.
        Input: user - instance User đã xác thực thành công.
        Output: Token object chứa các claims mặc định + role, full_name, email.
        """
        token = super().get_token(user)
        token["role"] = user.role
        token["full_name"] = user.get_full_name()
        token["email"] = user.email
        return token

    def validate(self, attrs):
        """
        Chức năng: Xác thực thông tin đăng nhập và bổ sung dữ liệu user vào response body.
        Input: attrs - dict chứa username/password từ request.
        Output: dict gồm access token, refresh token, và thông tin user cơ bản.
        Lý do: Giúp frontend lưu thông tin profile sau khi login mà không cần gọi thêm API.
        """
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "full_name": self.user.get_full_name(),
            "role": self.user.role,
            "avatar": self.user.avatar.url if self.user.avatar else None,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để xem và cập nhật thông tin cá nhân của user hiện tại.
    `username` và `id` là read_only vì không được phép đổi sau khi tạo tài khoản.
    """
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone", "avatar", "is_active"]
        read_only_fields = ["id", "username"]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer để xử lý đổi mật khẩu người dùng.
    Business logic: Yêu cầu xác nhận mật khẩu mới (`confirm_password`) để tránh lỗi gõ sai.
    Tất cả trường đều là write_only để tránh lộ mật khẩu trong response.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Chức năng: Kiểm tra mật khẩu xác nhận khớp với mật khẩu mới.
        Input: data - dict chứa old_password, new_password, confirm_password.
        Output: data nếu hợp lệ, raise ValidationError nếu không khớp.
        """
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Mật khẩu xác nhận không khớp.")
        return data
