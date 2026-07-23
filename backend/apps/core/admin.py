from django.contrib import admin

from .models import SystemConfig, AuditLog

@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'updated_at')
    search_fields = ('key', 'description')

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'module', 'created_at')
    list_filter = ('action', 'module')
    search_fields = ('user__email', 'record_id', 'payload')
