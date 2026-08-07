"""
apps/notifications/views.py
-----------------------------
View layer cho module Thông báo.
- NotificationViewSet: CRUD + mark_as_read, mark_all_read, send.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from apps.core.pagination import CustomPagination

from .serializers import NotificationSerializer, SendNotificationSerializer
from .selectors import NotificationSelector
from .services import NotificationService


class NotificationViewSet(viewsets.ModelViewSet):
    """
    CRUD Notification + các action đặc biệt.
    - GET    /notifications/           → danh sách của user hiện tại
    - POST   /notifications/send/      → gửi thông báo thủ công (admin)
    - POST   /notifications/{id}/mark_as_read/ → đánh dấu đã đọc
    - POST   /notifications/mark_all_read/     → đánh dấu tất cả đã đọc
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read', 'type']
    pagination_class = CustomPagination

    def get_queryset(self):
        return NotificationSelector.get_user_notifications(self.request.user)

    @action(detail=True, methods=['post'], url_path='mark_as_read')
    def mark_as_read(self, request, pk=None):
        """Đánh dấu 1 notification đã đọc."""
        notification = self.get_object()
        NotificationService.mark_as_read(notification)
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['post'], url_path='mark_all_read')
    def mark_all_read(self, request):
        """Đánh dấu tất cả notification của user hiện tại là đã đọc."""
        updated = self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': 'ok', 'updated': updated})

    @action(
        detail=False, methods=['post'], url_path='send',
        permission_classes=[permissions.IsAdminUser],
    )
    def send(self, request):
        """
        [Admin only] Gửi thông báo thủ công cho:
          - Danh sách user cụ thể (user_ids)
          - Toàn bộ user thuộc role (role_names)
          - Toàn bộ hệ thống (broadcast=true)
        """
        serializer = SendNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        count = NotificationService.send_bulk(
            title=data['title'],
            message=data['message'],
            notif_type=data['type'],
            user_ids=data.get('user_ids') or [],
            role_names=data.get('role_names') or [],
            broadcast=data.get('broadcast', False),
        )
        return Response(
            {'status': 'sent', 'notifications_created': count},
            status=status.HTTP_201_CREATED
        )
