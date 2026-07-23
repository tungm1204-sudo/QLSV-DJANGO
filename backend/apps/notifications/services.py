class NotificationService:
    @staticmethod
    def mark_as_read(notification):
        notification.is_read = True
        notification.save(update_fields=['is_read'])
