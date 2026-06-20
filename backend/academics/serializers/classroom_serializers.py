from rest_framework import serializers
from ..models import Classroom, ClassroomStudent, CourseAssignment
from teachers.serializers import TeacherProfileSerializer

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
        if obj.homeroom_teacher:
            return obj.homeroom_teacher.user.get_full_name()
        return "Chưa phân công"

class ClassroomStudentSerializer(serializers.ModelSerializer):
    """Serializer cho bảng trung gian Enrollment (Sinh viên - Lớp học)."""
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    student_email = serializers.CharField(source="student.email", read_only=True)
    mssv = serializers.CharField(source="student.student_profile.mssv", read_only=True, default="")
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)

    class Meta:
        model = ClassroomStudent
        fields = ["id", "classroom", "classroom_name", "student", "student_name", "student_email", "mssv", "enrolled_at"]
        read_only_fields = ["enrolled_at"]

class CourseAssignmentSerializer(serializers.ModelSerializer):
    """Serializer cho phân công giảng dạy."""
    classroom_name = serializers.CharField(source="classroom.name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    teacher_name = serializers.CharField(source="teacher.user.get_full_name", read_only=True)

    class Meta:
        model = CourseAssignment
        fields = ["id", "classroom", "classroom_name", "course", "course_name", "teacher", "teacher_name"]
