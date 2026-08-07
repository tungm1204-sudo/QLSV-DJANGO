from rest_framework import serializers
from apps.finance.models import TuitionRule, TuitionExemption, TuitionExtension, StudentDebt, Receipt

class TuitionRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuitionRule
        fields = '__all__'

class TuitionExemptionSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = TuitionExemption
        fields = '__all__'
        read_only_fields = ('status',)

class TuitionExtensionSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)

    class Meta:
        model = TuitionExtension
        fields = '__all__'
        read_only_fields = ('status', 'approved_by')

class StudentDebtSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    semester_name = serializers.CharField(source='semester.code', read_only=True)
    
    class Meta:
        model = StudentDebt
        fields = '__all__'
        read_only_fields = (
            'student', 'semester', 'total_credits', 'tuition_fee', 
            'discount_amount', 'final_amount', 'paid_amount', 'status'
        )

class ReceiptSerializer(serializers.ModelSerializer):
    student_code = serializers.CharField(source='student.student_code', read_only=True)
    student_name = serializers.CharField(source='student.user.full_name', read_only=True)
    
    class Meta:
        model = Receipt
        fields = '__all__'
        read_only_fields = ('status', 'created_by')
