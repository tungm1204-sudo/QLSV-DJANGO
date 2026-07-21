from rest_framework import serializers
from apps.enrollment.models import Enrollment
from apps.curriculum.serializers import CourseOfferingSerializer
from apps.hr.serializers import StudentSerializer

class EnrollmentReadSerializer(serializers.ModelSerializer):
    """
    Serializer dùng để đọc thông tin Đăng ký học phần.
    Sử dụng nested serializers để lấy đầy đủ thông tin hiển thị.
    """
    student = StudentSerializer(read_only=True)
    course_offering = CourseOfferingSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'course_offering', 'enrollment_type', 'status',
            'attendance_score', 'midterm_score', 'final_score', 'total_score',
            'is_locked', 'created_at', 'updated_at'
        ]

class EnrollmentWriteSerializer(serializers.Serializer):
    """
    Serializer dùng để validate request body khi sinh viên đăng ký lớp.
    Không dùng ModelSerializer.save() chứa logic, chỉ validate format theo Rules.
    """
    course_offering_id = serializers.UUIDField()
    enrollment_type = serializers.ChoiceField(
        choices=Enrollment.EnrollmentTypeChoices.choices, 
        default=Enrollment.EnrollmentTypeChoices.NORMAL
    )
    bypass_prerequisite = serializers.BooleanField(default=False)

class ChangeCourseOfferingSerializer(serializers.Serializer):
    """
    Serializer validate request body khi sinh viên muốn đổi lớp.
    """
    new_course_offering_id = serializers.UUIDField()
    bypass_prerequisite = serializers.BooleanField(default=False)

class ApproveEnrollmentSerializer(serializers.Serializer):
    """
    Serializer dùng cho API duyệt đăng ký đặc biệt.
    """
    is_approved = serializers.BooleanField()
