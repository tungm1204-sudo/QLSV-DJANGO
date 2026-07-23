import logging
from django.db import transaction
import openpyxl
from apps.core.models import SystemConfig, AuditLog

logger = logging.getLogger(__name__)

def log_audit(user_id, action_name: str, module: str, payload: dict = None, ip_address: str = None, user_agent: str = None, record_id: str = None):
    """
    Hàm tiện ích ghi lại vết hệ thống (Audit Log).
    """
    AuditLog.objects.create(
        user_id=user_id,
        action=action_name,
        module=module,
        payload=payload,
        record_id=record_id,
        ip_address=ip_address,
        user_agent=user_agent
    )

class SystemConfigService:
    @staticmethod
    @transaction.atomic
    def create_config(validated_data, actor_id, ip_address=None, user_agent=None):
        config = SystemConfig.objects.create(**validated_data)
        log_audit(actor_id, 'CREATE', 'SystemConfig', {'key': config.key}, ip_address, user_agent)
        return config

    @staticmethod
    @transaction.atomic
    def update_config(config, validated_data, actor_id, ip_address=None, user_agent=None):
        for key, value in validated_data.items():
            setattr(config, key, value)
        config.save()
        log_audit(actor_id, 'UPDATE', 'SystemConfig', {'key': config.key}, ip_address, user_agent)
        return config

class AuditLogService:
    @staticmethod
    def export_to_excel(queryset):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Audit Logs"
        headers = ["ID", "User", "Action", "Module", "IP Address", "Created At"]
        ws.append(headers)
        for log in queryset:
            user_str = log.user.email if log.user else "System"
            ws.append([str(log.id), user_str, log.action, log.module, log.ip_address, str(log.created_at)])
        return wb, None
