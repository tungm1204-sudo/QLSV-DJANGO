from rest_framework import serializers
from ..models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    # `student_name` là trường bổ sung để hiển thị tên sinh viên trực tiếp trong response
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    class Meta:
        model = Attendance
        fields = "__all__"

class BulkAttendanceSerializer(serializers.Serializer):
    """
    Serializer dành riêng để nhận danh sách nhiều bản ghi điểm danh cùng lúc.
    Dùng cho API bulk-update thay vì gọi API điểm danh từng lượt.
    """
    attendances = AttendanceSerializer(many=True)
