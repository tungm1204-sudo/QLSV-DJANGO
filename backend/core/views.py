from django.http import JsonResponse

def home(request):
    """
    Chức năng: Endpoint kiểm tra trạng thái API (health check).
    Output: JSON thông báo API đang chạy và hướng dẫn xem tài liệu.
    Lưu ý: Hiện không được mount vào urls.py vì đã dùng frontend React riêng biệt.
    """
    return JsonResponse({"status": "API is running. See /api/docs/ for endpoints."})
