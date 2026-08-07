"""
apps/notifications/serializers.py
----------------------------------
Định nghĩa các Serializer cho module Thông báo.
- NotificationSerializer: đọc/ghi 1 notification.
- SendNotificationSerializer: validate payload gửi thông báo thủ công.
"""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer đọc notification cho người dùng."""
    class Meta:
        model = Notification
        fields = '__all__'


class SendNotificationSerializer(serializers.Serializer):
    """
    Validate payload khi admin/staff gửi thông báo thủ công.
    - user_ids: danh sách UUID cụ thể (có thể rỗng nếu gửi theo role/all).
    - role_names: danh sách tên Role để gửi toàn bộ user thuộc role đó.
    - broadcast: True = gửi cho tất cả mọi người (null user trên Notification).
    - title, message, type: nội dung thông báo.
    """
    user_ids = serializers.ListField(
        child=serializers.UUIDField(), required=False, default=list
    )
    role_names = serializers.ListField(
        child=serializers.CharField(), required=False, default=list
    )
    broadcast = serializers.BooleanField(default=False)
    title = serializers.CharField(max_length=255)
    message = serializers.CharField()
    type = serializers.ChoiceField(
        choices=Notification.TypeChoices.choices,
        default=Notification.TypeChoices.INFO
    )

    def validate(self, data):
        # Ít nhất 1 trong 3 phải có: user_ids, role_names, broadcast
        if not data.get('user_ids') and not data.get('role_names') and not data.get('broadcast'):
            raise serializers.ValidationError(
                "Phải chỉ định ít nhất 1 trong 3: user_ids, role_names, hoặc broadcast=true."
            )
        return data
