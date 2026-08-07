from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardViewSet,
    ReportAPIView,
    ExportReportAPIView,
    ExportPDFAPIView,
    CustomReportTemplateViewSet,
    DataExportHistoryViewSet,
)

router = DefaultRouter()
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'templates', CustomReportTemplateViewSet, basename='report-templates')
router.register(r'export-history', DataExportHistoryViewSet, basename='export-history')

urlpatterns = [
    path('', include(router.urls)),
    path('data/<str:report_type>/', ReportAPIView.as_view(), name='report-data'),
    path('export/<str:report_type>/', ExportReportAPIView.as_view(), name='report-export-excel'),
    path('export-pdf/<str:report_type>/', ExportPDFAPIView.as_view(), name='report-export-pdf'),
]
