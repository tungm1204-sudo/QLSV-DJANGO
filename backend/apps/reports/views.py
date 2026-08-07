from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import CustomReportTemplate, DataExportHistory
from .serializers import (
    CustomReportTemplateSerializer,
    DataExportHistorySerializer,
    ReportFilterSerializer,
    DashboardOverviewSerializer
)
from .services import (
    get_dashboard_stats,
    get_training_reports,
    get_academic_reports,
    get_finance_reports,
    get_hr_reports,
    get_exam_reports,
    export_report_to_excel,
    export_report_to_pdf_html,
)

REPORT_TITLES = {
    'training': 'Báo cáo Đào tạo',
    'academic': 'Báo cáo Học tập',
    'finance': 'Báo cáo Tài chính',
    'hr': 'Báo cáo Nhân sự',
    'exams': 'Báo cáo Khảo thí',
}


def _resolve_report_data(report_type: str, filters: dict):
    """Helper: map report_type → service function."""
    mapping = {
        'training': get_training_reports,
        'academic': get_academic_reports,
        'finance': get_finance_reports,
        'hr': get_hr_reports,
        'exams': get_exam_reports,
    }
    fn = mapping.get(report_type)
    if not fn:
        return None
    return fn(filters)

class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        stats = get_dashboard_stats(request.user)
        serializer = DashboardOverviewSerializer(stats)
        return Response(serializer.data)

class ReportAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, report_type):
        filter_serializer = ReportFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        data = _resolve_report_data(report_type, filters)
        if data is None:
            return Response({'detail': 'Loại báo cáo không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class ExportReportAPIView(views.APIView):
    """
    GET /api/v1/reports/export-excel/<report_type>/
    Xuất báo cáo ra file Excel và lưu lịch sử xuất.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, report_type):
        filter_serializer = ReportFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        data = _resolve_report_data(report_type, filters)
        if data is None:
            return Response({'detail': 'Loại báo cáo không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

        excel_file = export_report_to_excel(data, report_type)

        # Lưu lịch sử xuất
        DataExportHistory.objects.create(
            user=request.user,
            export_type=report_type,
            format='EXCEL',
            filters_applied=filters,
            status='COMPLETED'
        )

        response = HttpResponse(
            excel_file,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename={report_type}_report.xlsx'
        return response


class ExportPDFAPIView(views.APIView):
    """
    GET /api/v1/reports/export-pdf/<report_type>/
    Xuất báo cáo dạng HTML (in-browser PDF).
    Frontend mở trong tab mới và dùng window.print() để in/lưu PDF.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, report_type):
        filter_serializer = ReportFilterSerializer(data=request.query_params)
        filter_serializer.is_valid(raise_exception=True)
        filters = filter_serializer.validated_data

        data = _resolve_report_data(report_type, filters)
        if data is None:
            return Response({'detail': 'Loại báo cáo không hợp lệ.'}, status=status.HTTP_400_BAD_REQUEST)

        title = REPORT_TITLES.get(report_type, report_type.title())
        html_content = export_report_to_pdf_html(data, report_type, title=title)

        # Lưu lịch sử xuất
        DataExportHistory.objects.create(
            user=request.user,
            export_type=report_type,
            format='PDF',
            filters_applied=filters,
            status='COMPLETED'
        )

        return HttpResponse(html_content, content_type='text/html; charset=utf-8')


class CustomReportTemplateViewSet(viewsets.ModelViewSet):
    """CRUD mẫu báo cáo tùy chỉnh — cho phép lưu lại bộ cấu hình để dùng lại."""
    queryset = CustomReportTemplate.objects.all()
    serializer_class = CustomReportTemplateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DataExportHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Xem lịch sử xuất dữ liệu của user hiện tại (read-only)."""
    serializer_class = DataExportHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DataExportHistory.objects.filter(user=self.request.user)
