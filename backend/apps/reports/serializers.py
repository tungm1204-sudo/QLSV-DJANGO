from rest_framework import serializers
from .models import CustomReportTemplate, DataExportHistory

class CustomReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomReportTemplate
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class DataExportHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DataExportHistory
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at']

class ReportFilterSerializer(serializers.Serializer):
    semester_id = serializers.UUIDField(required=False, allow_null=True)
    academic_year_id = serializers.UUIDField(required=False, allow_null=True)
    department_id = serializers.UUIDField(required=False, allow_null=True)
    major_id = serializers.UUIDField(required=False, allow_null=True)
    cohort_id = serializers.UUIDField(required=False, allow_null=True)
    from_date = serializers.DateField(required=False, allow_null=True)
    to_date = serializers.DateField(required=False, allow_null=True)

class DashboardOverviewSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
    total_lecturers = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, allow_null=True)
    total_debt = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, allow_null=True)
    active_classes = serializers.IntegerField()
    graduated_students = serializers.IntegerField()
    
    # Chart data
    chart_students_by_status = serializers.ListField(child=serializers.DictField(), required=False)
    chart_students_by_major = serializers.ListField(child=serializers.DictField(), required=False)
    chart_students_by_cohort = serializers.ListField(child=serializers.DictField(), required=False)
