from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include(('core.urls', 'core'), namespace='core')),
    path('students/', include(('students.urls', 'students'), namespace='students')),
    path('teachers/', include(('teachers.urls', 'teachers'), namespace='teachers')),
    path('academics/', include(('academics.urls', 'academics'), namespace='academics')),
]
