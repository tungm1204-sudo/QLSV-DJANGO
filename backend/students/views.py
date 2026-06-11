from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Parent, StudentProfile
from .serializers import ParentSerializer, StudentProfileSerializer, StudentCreateSerializer
from .utils import export_students_to_excel, import_students_from_excel


class ParentViewSet(viewsets.ModelViewSet):
    """API CRUD cho Phụ huynh / Người liên hệ khẩn cấp."""
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentProfileViewSet(viewsets.ModelViewSet):
    """
    API CRUD cho Hồ sơ Sinh viên.
    Business logic:
    - Dùng `lookup_field = 'mssv'` thay vì ID để URL thân thiện hơn (VD: /api/students/profiles/SV001/).
    - Phân biệt serializer: Khi tạo mới dùng StudentCreateSerializer (có thêm user fields),
      còn lại dùng StudentProfileSerializer để trả về dữ liệu đầy đủ.
    """
    queryset = StudentProfile.objects.all().select_related("user", "parent")
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "mssv"  # Tìm kiếm qua MSSV thay vì ID

    def get_serializer_class(self):
        """
        Chức năng: Chọn serializer phù hợp theo action hiện tại.
        Input: self.action - tên hành động (create, list, retrieve...).
        Output: Class Serializer tương ứng.
        """
        if self.action == "create":
            return StudentCreateSerializer
        return StudentProfileSerializer

    @action(detail=False, methods=["GET"])
    def export_excel(self, request):
        """
        GET /api/students/profiles/export_excel/
        Chức năng: Xuất toàn bộ danh sách sinh viên ra file Excel để tải về.
        Output: File .xlsx dưới dạng HTTP attachment.
        Lưu ý: Dùng `filter_queryset` để tôn trọng các bộ lọc (filter/search) đang được áp dụng.
        """
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
        """
        POST /api/students/profiles/import_excel/
        Chức năng: Import hàng loạt sinh viên từ file Excel.
        Input: request.FILES["file"] - file Excel đúng format template.
        Output: { success: "...", errors: [...] } - thống kê kết quả import.
        Lưu ý: Trả về 400 nếu không có file, 201 nếu có ít nhất 1 bản ghi thành công.
        """
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        success_count, errors = import_students_from_excel(file_obj)
        return Response({
            "success": f"Đã nhập thành công {success_count} sinh viên",
            "errors": errors
        }, status=status.HTTP_201_CREATED if success_count > 0 else status.HTTP_400_BAD_REQUEST)
