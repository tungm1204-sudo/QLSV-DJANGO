from rest_framework import serializers
from apps.exams.models import ExamSession, ExamRoom, GradeReview, GradeHistory, StudentAcademicRecord
from apps.enrollment.models import Enrollment
from apps.curriculum.serializers import CourseOfferingReadSerializer
from apps.hr.serializers import StudentSerializer, StaffSerializer

class ExamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = '__all__'

class ExamRoomReadSerializer(serializers.ModelSerializer):
    exam_session = ExamSessionSerializer(read_only=True)
    course_offering = CourseOfferingReadSerializer(read_only=True)
    supervisor = StaffSerializer(read_only=True)
    
    class Meta:
        model = ExamRoom
        fields = '__all__'

class ExamRoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRoom
        fields = '__all__'

class GradeReviewReadSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    reviewed_by = StaffSerializer(read_only=True)
    
    class Meta:
        model = GradeReview
        fields = '__all__'

class GradeReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeReview
        fields = ['enrollment', 'student', 'reason']

class GradeReviewApproveSerializer(serializers.Serializer):
    new_score = serializers.DecimalField(max_digits=4, decimal_places=2)
    staff_id = serializers.UUIDField()

class GradeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeHistory
        fields = '__all__'

class StudentAcademicRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAcademicRecord
        fields = '__all__'

class EnrollmentGradeUpdateSerializer(serializers.Serializer):
    attendance_score = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    midterm_score = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    final_score = serializers.DecimalField(max_digits=4, decimal_places=2, required=False, allow_null=True)
    reason = serializers.CharField(required=False, allow_blank=True, default="Cập nhật điểm")

class ImportGradesSerializer(serializers.Serializer):
    file = serializers.FileField()
