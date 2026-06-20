from rest_framework import serializers
from ..models import ExamType, ExamResult

class ExamTypeSerializer(serializers.ModelSerializer):
    """Serializer cho Loại kỳ thi (Giữa kỳ, Cuối kỳ...)."""
    class Meta:
        model = ExamType
        fields = "__all__"

class ExamResultSerializer(serializers.ModelSerializer):
    # Gắn thêm tên sinh viên và tên môn để frontend không cần gọi API join thêm
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    class Meta:
        model = ExamResult
        fields = "__all__"

class BulkExamResultSerializer(serializers.Serializer):
    """
    Serializer dành riêng để nhận danh sách nhiều bản ghi điểm cùng lúc.
    Dùng cho API bulk-update.
    """
    results = ExamResultSerializer(many=True)
