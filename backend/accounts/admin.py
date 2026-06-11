from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Cấu hình hiển thị User trên Django Admin.
    Hỗ trợ lọc theo vai trò và tìm kiếm nhanh theo username, email, tên.
    """
    list_display = ["username", "email", "get_full_name", "role", "is_active"]
    list_filter = ["role", "is_active"]   # Sidebar bộ lọc theo role và trạng thái kích hoạt
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering = ["username"]
