from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls), # Trang quản trị mặc định của Django
    path('accounts/', include('django.contrib.auth.urls')), # Các URL xác thực (login, logout, password reset...)
    path('', include(('core.urls', 'core'), namespace='core')), # App Core (Trang chủ)
    path('students/', include(('students.urls', 'students'), namespace='students')), # App Students
    path('teachers/', include(('teachers.urls', 'teachers'), namespace='teachers')), # App Teachers
    path('academics/', include(('academics.urls', 'academics'), namespace='academics')), # App Academics
]
