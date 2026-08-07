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

from apps.core.models import SystemBackup

class SystemBackupSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source='created_by.email', read_only=True)
    
    class Meta:
        model = SystemBackup
        fields = '__all__'
        read_only_fields = ['id', 'file_name', 'file_path', 'file_size', 'created_by', 'status', 'error_message', 'created_at']
