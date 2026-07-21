"""
URL Configuration
=================
Định tuyến API chính của toàn bộ dự án.
Mỗi app có file urls.py riêng và được include vào đây.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/identity/', include('apps.identity.urls')),
    path('api/v1/master-data/', include('apps.master_data.urls')),
    path('api/v1/hr/', include('apps.hr.urls')),
    path('api/v1/curriculum/', include('apps.curriculum.urls')),
    path('api/v1/affairs/', include('apps.affairs.urls')),
    path('api/v1/enrollment/', include('apps.enrollment.urls')),
]
