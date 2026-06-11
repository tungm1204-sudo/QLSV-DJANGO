from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Root URL configuration — điểm vào của toàn bộ hệ thống routing
# Mỗi app có file urls.py riêng, được include tại đây với prefix tương ứng
urlpatterns = [
    # Giao diện quản trị Django — chỉ dành cho superuser
    path("admin/", admin.site.urls),

    # API Xác thực (Login, Logout, Refresh Token, đổi mật khẩu)
    path("api/auth/", include("accounts.urls")),
    
    # API nghiệp vụ — mỗi app quản lý router riêng
    path("api/students/", include("students.urls")),
    path("api/teachers/", include("teachers.urls")),
    path("api/academics/", include("academics.urls")),

    # API Documentation (drf-spectacular)
    # /api/schema/ — trả về file OpenAPI schema dạng YAML
    # /api/docs/ — giao diện Swagger UI để test API trực tiếp trên trình duyệt
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

# Chỉ phục vụ file media (ảnh avatar...) khi chạy ở môi trường DEBUG
# Trong production, việc này phải được xử lý bởi Nginx hoặc CDN
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
