from rest_framework import serializers
from ..models import Semester, Grade, Course

class SemesterSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho Học kỳ — trả về tất cả trường."""
    class Meta:
        model = Semester
        fields = "__all__"

class GradeSerializer(serializers.ModelSerializer):
    """Serializer đơn giản cho Khóa/Năm học."""
    class Meta:
        model = Grade
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    # `grade_name` là trường chỉ đọc, được gắn thêm để frontend hiển thị tên khối
    grade_name = serializers.CharField(source="grade.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "code", "description", "credits", "grade", "grade_name"]
