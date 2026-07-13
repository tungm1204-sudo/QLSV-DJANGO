from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LoginSession, Role, SystemConfig, OTPToken, AuditLog, Notification
from .services import AuthService

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
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'avatar', 'status', 'is_active', 'role']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        
        # Check lockout before attempting auth
        is_locked, lock_reason = AuthService.check_lockout(email)
        if is_locked:
            raise serializers.ValidationError({
                "detail": lock_reason,
                "code": "account_locked"
            })

        try:
            data = super().validate(attrs)
        except Exception as e:
            # Login failed
            if email:
                AuthService.handle_failed_login(email)
            raise e

        # Login success
        user = self.user
        AuthService.clear_lockout(user)

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
