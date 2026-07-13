"""
Module Identity Serializers
Định nghĩa quy tắc chuyển đổi dữ liệu (từ Object sang JSON và ngược lại) cho phân hệ Identity.
Lý do: Đảm bảo dữ liệu đầu vào (Input) được validate đúng format trước khi chuyển cho Service xử lý, và dữ liệu đầu ra (Output) không bị rò rỉ các trường nhạy cảm (như mật khẩu). Tuyệt đối KHÔNG chứa business logic ở đây.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import LoginSession, Role, SystemConfig, AuditLog, Notification

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'avatar', 'status', 'is_active', 'created_at', 'role', 'role_id']
        read_only_fields = ['id', 'created_at']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Fix #4: Serializer chỉ khai báo field và validate format dữ liệu.
    Tuyệt đối không có create/update method — logic đó thuộc về UserService.
    """
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'avatar', 'status', 'is_active', 'role']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Fix #4: Serializer chỉ nhận token, KHÔNG chứa logic lockout.
    Logic lockout được xử lý hoàn toàn trong View (CustomTokenObtainPairView).
    """
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['user'] = {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'status': user.status,
            'avatar': user.avatar,
            'role': user.role.name if user.role else None,
            'permissions': user.role.permissions if user.role else []
        }
        return data


class LoginSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginSession
        fields = '__all__'


class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'
