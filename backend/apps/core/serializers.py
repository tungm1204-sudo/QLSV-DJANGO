from rest_framework import serializers
from .models import SystemConfig, AuditLog

class SystemConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfig
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'user_email', 'action', 'module', 'payload', 'ip_address', 'user_agent', 'created_at']
        read_only_fields = fields
