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
        fields = ['id', 'name', 'description', 'permissions']


class UserSerializer(serializers.ModelSerializer):
    # Dùng RoleSerializer để hiện full thông tin Role (tên, danh sách quyền) khi trả về Response (GET).
    role = RoleSerializer(read_only=True)
    
    # Chỉ dùng role_id để hứng ID từ Frontend gửi lên khi tạo/sửa User (POST/PUT/PATCH).
    # source='role' sẽ map dữ liệu ID này vào cột 'role' trong Database.
    # Lý do tách biệt: Frontend chỉ gửi gửi ID cho nhẹ, nhưng cần nhận về nguyên cả Object Role để hiển thị giao diện.
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'avatar', 'status', 'is_active', 'created_at', 'role', 'role_id', 'locked_until']
        read_only_fields = ['id', 'created_at', 'locked_until']


class UserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Fix #4: Serializer chỉ khai báo field và validate format dữ liệu.
    Tuyệt đối không có create/update method — logic đó thuộc về UserService.
    """
    # Gắn cờ write_only=True cho password.
    # Lý do: Đảm bảo bảo mật. Password chỉ được nhận từ Request, nhưng tuyệt đối không bao giờ xuất hiện trong Response.
    password = serializers.CharField(write_only=True, required=False)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'avatar', 'status', 'is_active', 'role_id']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Fix #4: Serializer chỉ nhận token, KHÔNG chứa logic lockout.
    Logic lockout được xử lý hoàn toàn trong View (CustomTokenObtainPairView).
    """
    def validate(self, attrs):
        # Gọi validate() của thư viện gốc để kiểm tra email/pass và sinh ra token (access, refresh).
        data = super().validate(attrs)

        user = self.user
        
        # Bổ sung thêm thông tin user profile vào chung Response.
        # Lý do: Giúp Frontend tiết kiệm được 1 lần gọi API /me. Vừa login xong là có luôn thông tin để vẽ giao diện (avatar, phân quyền).
        # FIX: role phải là object đầy đủ (id, name, permissions) để nhất quán với response /me/
        data['user'] = {
            'id': str(user.id),
            'email': user.email,
            'full_name': user.full_name,
            'status': user.status,
            'avatar': user.avatar,
            'role': {
                'id': str(user.role.id),
                'name': user.role.name,
                'permissions': user.role.permissions,
            } if user.role else None,
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
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'
