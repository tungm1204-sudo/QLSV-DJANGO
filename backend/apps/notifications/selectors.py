from .models import Notification

class NotificationSelector:
    @staticmethod
    def get_user_notifications(user):
        return Notification.objects.select_related('user', 'content_type').filter(user=user).order_by('-created_at')
