"""
apps/notifications/services.py
--------------------------------
Service layer cho module Thông báo.
Chứa logic tạo & gửi notification cho cá nhân, theo vai trò, hoặc broadcast.
Không nhận request object — chỉ nhận dữ liệu thuần.
"""
import logging
from django.contrib.auth import get_user_model
from .models import Notification

logger = logging.getLogger(__name__)
User = get_user_model()


class NotificationService:
    """
    Service xử lý toàn bộ logic liên quan đến Notification.
    """

    @staticmethod
    def mark_as_read(notification: Notification) -> None:
        """Đánh dấu 1 notification là đã đọc."""
        notification.is_read = True
        notification.save(update_fields=['is_read'])

    @staticmethod
    def create_notification(
        user,          # User instance hoặc None (broadcast)
        title: str,
        message: str,
        notif_type: str = Notification.TypeChoices.INFO,
        content_object=None,
    ) -> Notification:
        """
        Tạo 1 notification cho 1 user cụ thể.
        Nếu user=None → broadcast cho toàn hệ thống.
        """
        kwargs = {
            'user': user,
            'title': title,
            'message': message,
            'type': notif_type,
        }
        if content_object is not None:
            from django.contrib.contenttypes.models import ContentType
            kwargs['content_type'] = ContentType.objects.get_for_model(content_object)
            kwargs['object_id'] = str(content_object.pk)

        notif = Notification.objects.create(**kwargs)
        logger.info(
            "Notification created: user=%s, title='%s'",
            getattr(user, 'id', 'broadcast'),
            title,
        )
        return notif

    @staticmethod
    def send_bulk(
        title: str,
        message: str,
        notif_type: str = Notification.TypeChoices.INFO,
        user_ids: list = None,
        role_names: list = None,
        broadcast: bool = False,
    ) -> int:
        """
        Gửi thông báo hàng loạt.
        Trả về số lượng notification đã tạo.

        Thứ tự ưu tiên:
          1. broadcast=True  → gửi cho tất cả (1 bản ghi user=None).
          2. role_names       → gửi cho toàn bộ user thuộc role đó.
          3. user_ids         → gửi cho từng user_id cụ thể.
        """
        if broadcast:
            # 1 bản ghi user=None đại diện broadcast
            Notification.objects.create(
                user=None, title=title, message=message, type=notif_type
            )
            logger.info("Broadcast notification sent: title='%s'", title)
            return 1

        # Gom danh sách user cần gửi
        target_users = []

        if role_names:
            from apps.identity.models import Role
            roles = Role.objects.filter(name__in=role_names)
            role_users = User.objects.filter(role__in=roles, is_active=True)
            target_users.extend(role_users)

        if user_ids:
            specific_users = User.objects.filter(id__in=user_ids, is_active=True)
            # Tránh gửi trùng nếu user đã nằm trong role
            existing_ids = {u.id for u in target_users}
            target_users.extend(u for u in specific_users if u.id not in existing_ids)

        # Bulk create để tránh N queries
        notifications = [
            Notification(user=u, title=title, message=message, type=notif_type)
            for u in target_users
        ]
        Notification.objects.bulk_create(notifications)
        count = len(notifications)
        logger.info("Bulk notification sent to %d users, title='%s'", count, title)
        return count
