from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Parent, StudentProfile
from .serializers import ParentSerializer, StudentProfileSerializer, StudentCreateSerializer
from .utils import export_students_to_excel, import_students_from_excel


class ParentViewSet(viewsets.ModelViewSet):
    """API CRUD cho Phụ huynh"""
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentProfileViewSet(viewsets.ModelViewSet):
    """API CRUD cho Sinh viên"""
    queryset = StudentProfile.objects.all().select_related("user", "parent")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "mssv"  # Tìm kiếm qua MSSV thay vì ID

    def get_serializer_class(self):
        if self.action == "create":
            return StudentCreateSerializer
        return StudentProfileSerializer

    @action(detail=False, methods=["GET"])
    def export_excel(self, request):
        """Xuất danh sách sinh viên ra Excel."""
        current_queryset = self.filter_queryset(self.get_queryset())
        excel_file = export_students_to_excel(current_queryset)
        
        response = HttpResponse(
            excel_file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=students.xlsx"
        return response

    @action(detail=False, methods=["POST"])
    def import_excel(self, request):
        """Import sinh viên từ file Excel."""
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        success_count, errors = import_students_from_excel(file_obj)
        return Response({
            "success": f"Đã nhập thành công {success_count} sinh viên",
            "errors": errors
        }, status=status.HTTP_201_CREATED if success_count > 0 else status.HTTP_400_BAD_REQUEST)
