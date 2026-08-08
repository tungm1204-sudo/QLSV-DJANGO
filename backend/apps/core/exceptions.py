from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db.models import ProtectedError, RestrictedError

def custom_exception_handler(exc, context):
    # Gọi handler mặc định của DRF trước để lấy response tiêu chuẩn
    response = exception_handler(exc, context)

    # Bắt lỗi ràng buộc khóa ngoại (Foreign Key Constraints)
    if isinstance(exc, (ProtectedError, RestrictedError)):
        return Response(
            {
                "error": "Lỗi dữ liệu liên kết",
                "detail": "Không thể xóa dữ liệu này vì đang được sử dụng ở bảng khác. Vui lòng kiểm tra lại."
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
