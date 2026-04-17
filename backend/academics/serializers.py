from rest_framework import serializers
from .models import (
    Semester, Grade, Course, Classroom, CourseAssignment,
    Attendance, ExamType, ExamResult
)
from teachers.serializers import TeacherProfileSerializer


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(source="grade.name", read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "code", "description", "credits", "grade", "grade_name"]


class ClassroomSerializer(serializers.ModelSerializer):
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


class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = "__all__"


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    class Meta:
        model = Attendance
        fields = "__all__"


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = "__all__"


class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.get_full_name", read_only=True)
    course_name = serializers.CharField(source="course.name", read_only=True)
    class Meta:
        model = ExamResult
        fields = "__all__"
