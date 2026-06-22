from rest_framework import serializers
from .models import TuitionConfig, TuitionFee, TuitionFeeDetail

class TuitionConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionConfig
        fields = '__all__'

class TuitionFeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionFeeDetail
        fields = ['id', 'course_name', 'course_code', 'credits', 'amount']

class TuitionFeeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.get_full_name', read_only=True)
    mssv = serializers.CharField(source='student.mssv', read_only=True)
    details = TuitionFeeDetailSerializer(many=True, read_only=True)

    class Meta:
        model = TuitionFee
        fields = ['id', 'student', 'student_name', 'mssv', 'semester', 'total_credits', 'total_amount', 'status', 'due_date', 'details', 'created_at', 'updated_at']
        read_only_fields = ['total_amount', 'created_at', 'updated_at']
