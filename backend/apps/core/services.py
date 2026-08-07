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

import os
import time
from datetime import datetime
from django.conf import settings
from apps.core.models import SystemBackup

class BackupService:
    @staticmethod
    def create_backup(actor_id, ip_address=None, user_agent=None):
        """
        Thực hiện sao lưu Database.
        """
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"backup_{timestamp}.sql"
        file_path = os.path.join(backup_dir, file_name)

        # Ghi một file mock SQL để mô phỏng backup
        with open(file_path, 'w') as f:
            f.write(f"-- PostgreSQL database dump mock at {timestamp}\\n")
            f.write("-- Database: qlsv_django\\n")

        file_size = os.path.getsize(file_path)

        backup = SystemBackup.objects.create(
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            created_by_id=actor_id,
            status='SUCCESS'
        )

        log_audit(actor_id, 'CREATE', 'SystemBackup', {'file_name': file_name}, ip_address, user_agent)
        return backup

    @staticmethod
    def restore_backup(backup_id, actor_id, ip_address=None, user_agent=None):
        """
        Thực hiện phục hồi Database.
        """
        try:
            backup = SystemBackup.objects.get(id=backup_id)
        except SystemBackup.DoesNotExist:
            return None, "Bản sao lưu không tồn tại."

        if not os.path.exists(backup.file_path):
            return None, "File sao lưu không tồn tại trên hệ thống."

        # Mô phỏng quá trình restore (sleep 1 giây)
        time.sleep(1)

        log_audit(actor_id, 'RESTORE', 'SystemBackup', {'file_name': backup.file_name}, ip_address, user_agent)
        return backup, None

    @staticmethod
    def delete_backup(backup_id, actor_id, ip_address=None, user_agent=None):
        """
        Xóa bản sao lưu.
        """
        try:
            backup = SystemBackup.objects.get(id=backup_id)
        except SystemBackup.DoesNotExist:
            return None, "Bản sao lưu không tồn tại."

        if os.path.exists(backup.file_path):
            os.remove(backup.file_path)

        backup_name = backup.file_name
        backup.delete()

        log_audit(actor_id, 'DELETE', 'SystemBackup', {'file_name': backup_name}, ip_address, user_agent)
        return backup_name, None
