from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.identity.permissions import require_permission
from apps.identity.services import log_audit

from .serializers import SystemConfigSerializer, AuditLogSerializer
from .selectors import SystemConfigSelector, AuditLogSelector
from .services import SystemConfigService, AuditLogService

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')

class SystemConfigViewSet(viewsets.ModelViewSet):
    """
    API ViewSet cho SystemConfig.
    """
    serializer_class = SystemConfigSerializer

    def get_queryset(self):
        return SystemConfigSelector.get_configs()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [require_permission('SYSTEM_VIEW')()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [require_permission('SYSTEM_UPDATE')()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        config = SystemConfigService.create_config(
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(SystemConfigSerializer(config).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        config = SystemConfigService.update_config(
            instance,
            serializer.validated_data,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(SystemConfigSerializer(config).data)

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet cho AuditLog. Chỉ đọc.
    """
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user__email', 'action', 'module']
    search_fields = ['user__email', 'action', 'module', 'payload']

    def get_queryset(self):
        return AuditLogSelector.get_logs()

    def get_permissions(self):
        return [require_permission('AUDIT_VIEW')()]

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        log_audit(
            request.user.id, 'EXPORT_EXCEL', 'AuditLog', None,
            get_client_ip(request), get_user_agent(request)
        )

        wb, error = AuditLogService.export_to_excel(queryset)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="audit_logs.xlsx"'
        wb.save(response)
        return response

from .models import SystemBackup
from .serializers import SystemBackupSerializer
from .services import BackupService
import os

class SystemBackupViewSet(viewsets.ModelViewSet):
    """
    API ViewSet cho SystemBackup.
    Chỉ cho phép: list, retrieve, create, destroy, restore
    """
    queryset = SystemBackup.objects.all()
    serializer_class = SystemBackupSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status']
    search_fields = ['file_name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'download']:
            return [require_permission('SYSTEM_VIEW')()]
        elif self.action in ['create', 'destroy', 'restore']:
            return [require_permission('SYSTEM_UPDATE')()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        backup = BackupService.create_backup(
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        return Response(SystemBackupSerializer(backup).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        backup_name, error = BackupService.delete_backup(
            pk,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        if error:
            return Response({'error': error}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        backup, error = BackupService.restore_backup(
            pk,
            request.user.id,
            get_client_ip(request),
            get_user_agent(request)
        )
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Phục hồi dữ liệu thành công'})

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        try:
            backup = self.get_object()
        except SystemBackup.DoesNotExist:
            return Response({'error': 'Bản sao lưu không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        if not os.path.exists(backup.file_path):
            return Response({'error': 'File không tồn tại trên hệ thống'}, status=status.HTTP_404_NOT_FOUND)

        with open(backup.file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/sql')
            response['Content-Disposition'] = f'attachment; filename="{backup.file_name}"'
            return response
