from rest_framework import serializers
from .models import (
    Semester, Grade, Course, Classroom, CourseAssignment,
    Attendance, ExamType, ExamResult
)
from teachers.serializers import TeacherProfileSerializer


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
    # thay vì phải gọi API riêng để resolve FK
    grade_name = serializers.CharField(source="grade.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "code", "description", "credits", "grade", "grade_name"]


class ClassroomSerializer(serializers.ModelSerializer):
    # Thêm các trường read_only để trả về tên thay vì chỉ ID -> giảm số lượng request từ frontend
    grade_name = serializers.CharField(source="grade.name", read_only=True)
    semester_name = serializers.CharField(source="semester.name", read_only=True)
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            "id", "name", "grade", "grade_name", "semester", "semester_name",
            "homeroom_teacher", "teacher_name", "max_students", "status", "remarks"
        ]

    def get_teacher_name(self, obj):
        """
        Chức năng: Trả về tên đầy đủ của giảng viên chủ nhiệm.
        Input: obj - instance Classroom.
        Output: (str) Tên giảng viên hoặc 'Chưa phân công' nếu chưa có.
        """
        if obj.homeroom_teacher:
            return obj.homeroom_teacher.user.get_full_name()
        return "Chưa phân công"


class CourseAssignmentSerializer(serializers.ModelSerializer):
    """Serializer cho phân công giảng dạy — trả về tất cả trường."""
    class Meta:
        model = CourseAssignment
        fields = "__all__"


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
