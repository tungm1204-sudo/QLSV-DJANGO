from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LoginHistory, Role, SystemConfig, OTPToken, AuditLog, Notification

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

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
        
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # We need to manually check if user exists and is locked before attempting auth
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
            if user.locked_until and user.locked_until > timezone.now():
                raise serializers.ValidationError({
                    "detail": f"Account is locked until {user.locked_until.strftime('%Y-%m-%d %H:%M:%S')} UTC.",
                    "code": "account_locked"
                })
        except User.DoesNotExist:
            pass # Super will handle invalid credentials

        try:
            data = super().validate(attrs)
        except Exception as e:
            # Login failed
            if email:
                try:
                    user = User.objects.get(email=email)
                    user.failed_login_attempts += 1
                    
                    # Hardcoded logic, should get from SystemConfig, but for safety keep hardcoded fallback
                    max_attempts = 5
                    try:
                        config = SystemConfig.objects.get(key='MAX_LOGIN_ATTEMPTS')
                        max_attempts = int(config.value)
                    except (SystemConfig.DoesNotExist, ValueError):
                        pass

                    if user.failed_login_attempts >= max_attempts:
                        user.locked_until = timezone.now() + timezone.timedelta(minutes=15)
                    user.save(update_fields=['failed_login_attempts', 'locked_until'])
                except User.DoesNotExist:
                    pass
            raise e

        # Login success
        user = self.user
        user.failed_login_attempts = 0
        user.locked_until = None
        user.save(update_fields=['failed_login_attempts', 'locked_until'])

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

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
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
